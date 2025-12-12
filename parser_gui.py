from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import tkinter as tk
import tkinter.font as tkFont
from src.parse.parser import Parser
from src.parse.syntax_tree import ReadStatementNode, IdentifierNode, ConstantNode, OperatorNode, AssignmentStatementNode, WriteStatementNode, StatementSequence
from src.parse.token_file_parser import TokenFileParser

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
    "statements": [ IF_AST, REPEAT_AST ,IF_AST]
}

# ################################### AST drawing ####################################
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

filepath = ""

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

def ast_depth(node):
    t = node.get("type")
    if t in ("Literal", "Identifier"):
        return 1
    elif t == "BinaryExpression":
        return 1 + max(ast_depth(node["left"]), ast_depth(node["right"]))
    elif t == "IfStatement":
        d = [ast_depth(node["test"]), ast_depth(node["then"])]
        if node.get("else"):
            d.append(ast_depth(node["else"]))
        return 1 + max(d)
    elif t == "RepeatStatement":
        return 1 + max(ast_depth(node["body"]), ast_depth(node["test"]))
    elif t == "Assignment":
        return 1 + ast_depth(node["value"])
    elif t == "Block":
        depths = [ast_depth(stmt) for stmt in node.get("statements", [])]
        return 1 + (max(depths) if depths else 0)
    else:
        return 1

def get_node_width_height(canvas, label, shape, scale=1.0):
    font = tkFont.Font(family="TkDefaultFont", size=int(12*scale))
    text_width = font.measure(label)
    text_height = font.metrics("linespace")
    pad_x = 20 * scale
    pad_y = 10 * scale
    w = text_width + pad_x * 2
    h = text_height + pad_y * 2
    return w, h, font

# --- draw a single node (shape + label) ---
def draw_node(canvas, x, y, label, shape, scale=1.0):
    w, h, font = get_node_width_height(canvas, label, shape, scale)
    if shape == "rect":
        canvas.create_rectangle(x - w/2, y - h/2, x + w/2, y + h/2,
                                fill="#cce", outline="black")
    else:
        canvas.create_oval(x - w/2, y - h/2, x + w/2, y + h/2,
                           fill="#cec", outline="black")

    canvas.create_text(x, y, text=label, font=font)
    return w, h

# --- main recursive AST drawing ---
def draw_ast(canvas, node, x, y, width, scale=1.0, vscale=1.0, parent_x=None, parent_y=None, parent_shape=None):
    t = node.get("type")

    # --- Block special handling ---
    if t == "Block":
        stmts = node.get("statements", [])
        if not stmts:
            return

        total = sum(subtree_size(s) for s in stmts)
        slot = width / total

        curr_x = x - width/2 + slot/2
        positions = []

        for stmt in stmts:
            w = subtree_size(stmt) * slot
            cx = curr_x + (w - slot)/2
            positions.append(cx)
            curr_x += w

        # Sibling arrows
        if len(positions) > 1:
            arrow_y = y + 100 * vscale
            for i in range(len(positions)-1):
                canvas.create_line(positions[i] + 65*scale, arrow_y,
                                   positions[i+1] - 65*scale, arrow_y, arrow=tk.LAST)

        child_y = y + 100 * vscale
        for i, stmt in enumerate(stmts):
            cx = positions[i]
            if parent_x is not None:
                canvas.create_line(parent_x, parent_y + 20*scale,
                                   cx, child_y - 20*scale, arrow=tk.LAST)

            draw_ast(canvas, stmt, cx, child_y,
                     subtree_size(stmt) * slot, scale, vscale)
        return

    # Node label
    if t == "BinaryExpression":
        label = f"op ({node.get('operator', 'op')})"
    elif t == "Literal":
        label = f"const ({node.get('value')})"
    elif t == "Identifier":
        label = f"id ({node.get('name')})"
    elif t == "Assignment":
        label = f"assign({node.get('identifier')})"
    elif t == "ReadStatement":
        label = f"read({node.get('identifier')})"
    elif t == "WriteStatement":
        # Always show 'write' as label, child will show the variable/expression
        label = "write"
    else:
        label = t

    shape = NODE_SHAPES.get(t, "rect")
    draw_node(canvas, x, y, label, shape, scale)

    # Parent → child arrow
    if parent_x is not None:
        canvas.create_line(parent_x, parent_y + 20*scale,
                           x, y - 20*scale, arrow=tk.LAST)

    # Children
    child_y = y + 100 * vscale

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
    elif t == "WriteStatement":
        children = [node["value"]]
    else:
        children = []

    if not children:
        return

    total = sum(subtree_size(c) for c in children)
    slot = width / total
    curr_x = x - width/2 + slot/2

    for child in children:
        w = subtree_size(child) * slot
        cx = curr_x + (w - slot)/2

        draw_ast(canvas, child, cx, child_y, w, scale, vscale,
                 parent_x=x, parent_y=y, parent_shape=shape)

        curr_x += w

def fit_and_draw_ast(canvas, ast):
    canvas.delete("all")
    canvas.update_idletasks()
    c_width = canvas.winfo_width()
    c_height = canvas.winfo_height()

    if c_width < 10 or c_height < 10:
        c_width, c_height = 1000, 500

    padding_x = 40
    padding_y = 40

    ast_width = c_width - 2 * padding_x
    ast_height = c_height - 2 * padding_y

    n_leaves = subtree_size(ast)
    n_levels = ast_depth(ast)

    base_h_spacing = 150
    base_v_spacing = 100

    scale_x = ast_width / (n_leaves * base_h_spacing)
    scale_y = ast_height / (n_levels * base_v_spacing)

    scale = min(scale_x, 1.0)
    vscale = min(scale_y, 1.0)

    center_x = c_width // 2
    top_y = padding_y

    draw_ast(canvas, ast,
             center_x, top_y,
             n_leaves * base_h_spacing * scale,
             scale, vscale)



# -------------------- GLOBAL STORAGE ---------------------
current_file_content = ""

############################### Read input file and clear data #############################

def openFile(file_text):
    global current_file_conten
    global filepath
    filepath = filedialog.askopenfilename()
    if not filepath:
        return
    with open(filepath, 'r') as file:
        content = file.read()
    current_file_content = content
    file_text.delete("1.0", tk.END)
    file_text.insert(tk.END, content)

def clear_data():
    global current_file_content
    current_file_content = ""
    canvas.delete("all")
    file_text.delete("1.0", tk.END)

############################### Get the parse tree from src code ###########################

def get_parse_tree():

    # ast = from controller
    token_parser = TokenFileParser()
    token_stream = token_parser.parse_file(filepath=filepath)
    parser = Parser(token_stream)
    program = parser.parse()
    ast_json = program.to_json()
    fit_and_draw_ast(canvas, ast_json)


################################### Main Tkinter window ####################################
root = tk.Tk()
root.title("Tiny language parser") 
mainframe = ttk.Frame(root, padding=(3, 3, 12, 12))
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))

tree_frame = ttk.Frame(mainframe, padding=(3, 3, 12, 12))
tree_frame.grid(column=1, row=0, sticky=(N, E, W, S))
tree_frame.columnconfigure(0, weight=1)
tree_frame.rowconfigure(1, weight=1)

canvas = tk.Canvas(tree_frame, bg="white")
canvas.grid(column=0, row=1, sticky="nsew")

input_file_frame = ttk.Frame(mainframe, padding=(3, 3, 12, 12))
input_file_frame.grid(column=0, row=0, sticky=(N, E,W, S))

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
choose_file_button = ttk.Button(input_file_frame,text="choose file",
                                command=lambda: openFile(file_text),padding=(3))
choose_file_button.grid(column=0,row=0,sticky=(N,W), padx=(0,10))

clear_button = ttk.Button(input_file_frame,text="clear",
                          command=lambda: clear_data(),padding=(3))
clear_button.grid(column=1,row=0,sticky=(N,E))

draw_button = ttk.Button(input_file_frame,text="Draw Parse Tree",
                          command=lambda:get_parse_tree(),padding=(3))
draw_button.grid(column=0,row=2,columnspan=2, sticky="nsew", pady=(10,0))


# Build the StatementSequence as in the test
read_stmt = ReadStatementNode("x")
id_stmt = IdentifierNode("x")
const_stmt = ConstantNode(1)
opnode = OperatorNode("+", id_stmt, const_stmt)
assign_stmt = AssignmentStatementNode("x", opnode)
write_stmt = WriteStatementNode(IdentifierNode("x"))
program = StatementSequence([read_stmt, assign_stmt, write_stmt])

# Convert to JSON for the GUI
ast_to_draw = program.to_json()

def on_canvas_resize(event):
    fit_and_draw_ast(canvas, ast_to_draw)

canvas.bind("<Configure>", on_canvas_resize)

fit_and_draw_ast(canvas, ast_to_draw)

root.mainloop()
