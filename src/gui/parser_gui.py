from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import tkinter as tk

# Example ASTs
IF_AST = {
    "type": "IfStatement",
    "test": {
        "type": "BinaryExpression",
        "operator": ">",
        "left": {"type": "Identifier", "name": "x"},
        "right": {"type": "Literal",  "value": 0}
    },
    "then": {
        "type": "Block",
        "statements": [
            {
                "type": "Assignment",
                "identifier": "y",
                "value": {
                    "type": "BinaryExpression",
                    "operator": "+",
                    "left": {"type": "Identifier", "name": "y"},
                    "right": {"type": "Literal", "value": 1}
                }
            }
        ]
    },
    "else": {
        "type": "Block",
        "statements": [
            {
                "type": "Assignment",
                "identifier": "y",
                "value": {"type": "Literal", "value": 0}
            }
        ]
    }
}

REPEAT_AST = {
    "type": "RepeatStatement",
    "body": {
        "type": "Block",
        "statements": [
            {
                "type": "Assignment",
                "identifier": "x",
                "value": {
                    "type": "BinaryExpression",
                    "operator": "-",
                    "left": {"type": "Identifier", "name": "x"},
                    "right": {"type": "Literal", "value": 1}
                }
            }
        ]
    },
    "test": {
        "type": "BinaryExpression",
        "operator": "==",
        "left": {"type": "Identifier", "name": "x"},
        "right": {"type": "Literal", "value": 0}
    }
}

AST = {
    "type": "Block",
    "statements": [ IF_AST, REPEAT_AST ]
}

################################### AST drawing ####################################
NODE_SHAPES = {
    "IfStatement": "rect",
    "RepeatStatement": "rect",
    "Assignment": "rect",
    "Block": "rect",
    "BinaryExpression": "oval",
    "Literal": "oval",
    "Identifier": "oval",
    "FunctionCall": "oval",
}

# --- compute subtree size (for layout) ---
def subtree_size(node):
    t = node.get("type")
    if t in ("Literal", "Identifier"):
        return 1
    elif t == "BinaryExpression":
        return subtree_size(node["left"]) + subtree_size(node["right"])
    elif t == "IfStatement":
        s = subtree_size(node["test"]) + subtree_size(node["then"])
        if node.get("else"):
            s += subtree_size(node["else"])
        return s
    elif t == "RepeatStatement":
        return subtree_size(node["body"]) + subtree_size(node["test"])
    elif t == "Assignment":
        return subtree_size(node["value"])
    elif t == "Block":
        total = 0
        for stmt in node.get("statements", []):
            total += subtree_size(stmt)
        return total or 1
    else:
        return 1

# --- draw a single node (shape + label) ---
def draw_node(canvas, x, y, label, shape):
    if shape == "rect":
        w, h = 160, 40
        canvas.create_rectangle(x - w/2, y - h/2, x + w/2, y + h/2,
                                fill="#cce", outline="black")
    elif shape == "oval":
        w, h = 80, 30
        canvas.create_oval(x - w/2, y - h/2, x + w/2, y + h/2,
                           fill="#cec", outline="black")
    else:
        w, h = 100, 40
        canvas.create_rectangle(x - w/2, y - h/2, x + w/2, y + h/2,
                                fill="#eee", outline="black")
    canvas.create_text(x, y, text=label)

# --- main recursive AST drawing ---
def draw_ast(canvas, node, x, y, width):
    t = node.get("type")

    if t == "Block":
        stmts = node.get("statements", [])
        if not stmts:
            return

        total = sum(subtree_size(s) for s in stmts)
        slot = width / total

        positions = []
        curr_x = x - width/2 + slot/2

        for stmt in stmts:
            w = subtree_size(stmt) * slot
            cx = curr_x + (w - slot)/2
            positions.append(cx)

            draw_ast(canvas, stmt, cx, y, w)
            curr_x += w

        # Draw sibling statements pointers
        if len(positions) > 1:
            arrow_y = y + 5  
            for i in range(len(positions)-1):
                x1 = positions[i]
                x2 = positions[i+1]
                canvas.create_line(x1 + 65, arrow_y, x2 - 65, arrow_y, arrow=tk.LAST)

        return

    if t == "BinaryExpression":
        label = node.get("operator", "op")
    elif t == "Literal":
        label = str(node.get("value"))
    elif t == "Identifier":
        label = node.get("name")
    elif t == "Assignment":
        label = f"assign({node.get('identifier')})"
    else:
        label = t

    shape = NODE_SHAPES.get(t, "rect")
    draw_node(canvas, x, y, label, shape)

    child_y = y + 100  # vertical offset for children

    # gather children according to type
    children = []
    if t == "IfStatement":
        children = [node["test"], node["then"]]
        if node.get("else"):
            children.append(node["else"])
    elif t == "RepeatStatement":
        children = [node["body"], node["test"]]
    elif t == "BinaryExpression":
        children = [node["left"], node["right"]]
    elif t == "Assignment":
        children = [node["value"]]
    else:
        children = []

    if not children:
        return

    total = sum(subtree_size(c) for c in children)
    slot = width / total

    curr_x = x - width/2 + slot/2
    positions = []

    for child in children:
        w = subtree_size(child) * slot
        cx = curr_x + (w - slot)/2
        positions.append(cx)

        # draw parent → child vertical line
        canvas.create_line(x, y + (20 if shape=="rect" else 15), cx, child_y - 20)

        draw_ast(canvas, child, cx, child_y, w)
        curr_x += w



def openFile(file_text):
    filepath = filedialog.askopenfilename()
    if not filepath:
        return
    with open(filepath, 'r') as file:
        content = file.read()
    file_text.delete("1.0", tk.END)
    file_text.insert(tk.END, content)

def clear_data():
    canvas.delete("all")
    file_text.delete("1.0", tk.END)


################################### Main Tkinter window ####################################
root = tk.Tk()
root.title("Tiny language parser") 
mainframe = ttk.Frame(root, padding=(3, 3, 12, 12))
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))

tree_frame = ttk.Frame(mainframe, padding=(3, 3, 12, 12))
tree_frame.grid(column=1, row=0, sticky=(N, E,W, S))

input_file_frame = ttk.Frame(mainframe, padding=(3, 3, 12, 12))
input_file_frame.grid(column=0, row=0, sticky=(N, E,W, S))

canvas = tk.Canvas(tree_frame, width=1000, height=500, bg="white")
canvas.grid(column=0,row=1,sticky="nsew")


root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

mainframe.columnconfigure(0, weight=1)  
mainframe.columnconfigure(1, weight=3)  
mainframe.rowconfigure(0, weight=1)


tree_frame.columnconfigure(0, weight=1)
tree_frame.rowconfigure(1, weight=1)


input_file_frame.columnconfigure(0, weight=1)
input_file_frame.columnconfigure(1, weight=1)
input_file_frame.rowconfigure(1, weight=1)


################# Input file content and scrollbar ########################
file_frame = ttk.Frame(input_file_frame)
file_frame.grid(column=0, row=1, columnspan=2, sticky="nsew", pady=(10,0))

file_text = tk.Text(file_frame, width=40, height=15, wrap="word")
file_text.pack(side="left", fill="both", expand=True)
scrollbar = ttk.Scrollbar(file_frame, orient="vertical", command=file_text.yview)
scrollbar.pack(side="right", fill="y")
file_text.config(yscrollcommand=scrollbar.set)


################################ Buttons ################################
choose_file_button = ttk.Button(input_file_frame,text="choose file", command= lambda: openFile(file_text),padding=(3))
choose_file_button.grid(column=0,row=0,sticky=(N,W), padx=(0,10))

clear_button = ttk.Button(input_file_frame,text="clear", command= lambda: clear_data(),padding=(3))
clear_button.grid(column=1,row=0,sticky=(N,E))

ast_to_draw = AST 

full_width = subtree_size(ast_to_draw) * 150
draw_ast(canvas, ast_to_draw, 500, 50, full_width)

root.mainloop()