from tkinter import filedialog, END

def open_file(gui):
    filepath = filedialog.askopenfilename()
    if not filepath:
        return

    with open(filepath, "r") as f:
        content = f.read()

    gui.current_file_content = content
    gui.file_text.delete("1.0", END)
    gui.file_text.insert(END, content)

def clear_data(gui):
    gui.current_file_content = ""
    gui.canvas.delete("all")
    gui.file_text.delete("1.0", "end")
