from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import tkinter as tk

AST = {
    "type": "FunctionDefinition",
    "children": [
        {"type": "Declaration", "children": []},
        {
            "type": "WhileStatement",
            "children": [
                {"type": "BinaryExpression", "children": []},
                {
                    "type": "Assignment",
                    "children": [
                        {"type": "Identifier", "children": []},
                        {"type": "BinaryExpression", "children": []}
                    ]
                }
            ]
        },
        {
            "type": "IfStatement",
            "children": [
                {"type": "BinaryExpression", "children": []},
                {"type": "FunctionCall", "children": []}
            ]
        }
    ]
}

NODE_SHAPES = {
    "FunctionDefinition": "rect",
    "Declaration": "rect",
    "Assignment": "rect",
    "BinaryExpression": "circle",
    "FunctionCall": "oval",
    "Identifier": "text",
    "IfStatement": "diamond",
    "WhileStatement": "oval"
}

def compute_width(node):
    if not node["children"]:
        return 1
    return sum(compute_width(c) for c in node["children"])

def draw_tree(canvas, node, x, y, width):
    shape = NODE_SHAPES.get(node["type"], "rect")
    draw_node(canvas, x, y, node["type"], shape)

    # Position children
    if not node["children"]:
        return

    step = width / len(node["children"])
    child_x = x - width/2 + step/2
    child_y = y + 120

    for child in node["children"]:
        child_width = compute_width(child) * 120

        canvas.create_line(x, y+40, child_x, child_y-40)

        draw_tree(canvas, child, child_x, child_y, child_width)
        child_x += child_width


def draw_node(canvas, x, y, text, shape):
    if shape == "rect":
        canvas.create_rectangle(x-50, y-25, x+50, y+25, fill="#aee")
    elif shape == "oval":
        canvas.create_oval(x-50, y-25, x+50, y+25, fill="#aea")
    elif shape == "circle":
        canvas.create_oval(x-30, y-30, x+30, y+30, fill="#fea")
    elif shape == "diamond":
        canvas.create_polygon(
            x, y-35,
            x+60, y,
            x, y+35,
            x-60, y,
            fill="#fc9"
        )
    canvas.create_text(x, y, text=text)

def openFile(file_text):
    filepath = filedialog.askopenfilename()
    if not filepath:
        return
    with open(filepath, 'r') as file:
        content = file.read()
    file_text.set(content)   

def clear_data():
    canvas.delete("all")
    file_content.set("")

# Main Tkinter window
root = tk.Tk()
file_content= tk.StringVar() 
mainframe = ttk.Frame(root, padding=(3, 3, 12, 12))
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))

tree_frame = ttk.Frame(mainframe, padding=(3, 3, 12, 12))
tree_frame.grid(column=1, row=0, sticky=(N, E, S))

input_file_frame = ttk.Frame(mainframe, padding=(3, 3, 12, 12))
input_file_frame.grid(column=0, row=0, sticky=(N, W, S))

canvas = tk.Canvas(tree_frame, width=1000, height=500, bg="white")
canvas.grid(column=0,row=1,sticky=(N,W,E,S))
tree_width = compute_width(AST) * 120
draw_tree(canvas, AST, 500, 80, tree_width)


choose_file_button = ttk.Button(input_file_frame,text="choose file", command= lambda: openFile(file_content),padding=(3))
choose_file_button.grid(column=0,row=0,sticky=(N,W))

clear_button = ttk.Button(input_file_frame,text="clear", command= lambda: clear_data(),padding=(3))
clear_button.grid(column=1,row=0,sticky=(N,E))

file_label = ttk.Label(input_file_frame, textvariable=file_content,background="white",padding=(3))
file_label.grid(column=0, row=1, sticky=(N, W, S))

root.mainloop()