"""
Main GUI window for TINY language parser.
Allows user to select token file and displays the syntax tree.
"""

import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from src.parse.token_file_parser import TokenFileParser
from src.parse.parser import Parser
from src.gui.tree_visualizer import TreeVisualizer
from src.tinyerror.tiny_error import TinyError


class MainWindow:
    """Main application window for TINY parser GUI."""
    
    def __init__(self, root):
        self.root = root
        self.root.title("TINY Language Parser")
        self.root.geometry("1200x800")
        
        # Current file path
        self.current_file = None
        self.syntax_tree = None
        
        # Setup GUI components
        self._setup_ui()
    
    def _setup_ui(self):
        """Setup the user interface components."""
        # Top frame for controls
        top_frame = tk.Frame(self.root, bg="#f0f0f0", padx=10, pady=10)
        top_frame.pack(side=tk.TOP, fill=tk.X)
        
        # Title label
        title_label = tk.Label(
            top_frame,
            text="TINY Language Parser",
            font=("Arial", 16, "bold"),
            bg="#f0f0f0"
        )
        title_label.pack(side=tk.LEFT, padx=10)
        
        # Load file button
        self.load_button = tk.Button(
            top_frame,
            text="Load Token File",
            command=self.load_file,
            font=("Arial", 12),
            bg="#4CAF50",
            fg="white",
            padx=20,
            pady=5,
            cursor="hand2"
        )
        self.load_button.pack(side=tk.LEFT, padx=10)
        
        # Status label
        self.status_label = tk.Label(
            top_frame,
            text="No file loaded",
            font=("Arial", 10),
            bg="#f0f0f0",
            fg="gray"
        )
        self.status_label.pack(side=tk.LEFT, padx=10)
        
        # Main content area with canvas and scrollbars
        content_frame = tk.Frame(self.root)
        content_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create canvas with scrollbars
        self.canvas = tk.Canvas(content_frame, bg="white", highlightthickness=1, highlightbackground="gray")
        
        # Scrollbars
        v_scrollbar = tk.Scrollbar(content_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        h_scrollbar = tk.Scrollbar(content_frame, orient=tk.HORIZONTAL, command=self.canvas.xview)
        
        self.canvas.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Pack scrollbars and canvas
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Initialize tree visualizer
        self.visualizer = TreeVisualizer(self.canvas)
        
        # Welcome message on canvas
        self.canvas.create_text(
            400, 300,
            text="Load a token file to display the syntax tree",
            font=("Arial", 14),
            fill="gray",
            tags="welcome"
        )
    
    def load_file(self):
        """Load and parse a token file."""
        # Open file dialog
        filepath = filedialog.askopenfilename(
            title="Select Token File",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        
        if not filepath:
            return
        
        self.current_file = filepath
        
        try:
            # Parse token file
            self.status_label.config(text="Parsing token file...", fg="blue")
            self.root.update()
            
            token_stream = TokenFileParser.parse_file(filepath)
            
            # Parse with TINY parser
            parser = Parser(token_stream)
            self.syntax_tree = parser.parse()
            
            # Update status
            self.status_label.config(
                text=f"✓ Successfully parsed: {filepath.split('/')[-1]}",
                fg="green"
            )
            
            # Draw tree
            self.canvas.delete("welcome")
            self.visualizer.draw_tree(self.syntax_tree)
            
            # Show success message
            messagebox.showinfo(
                "Success",
                "The token file was successfully parsed!\n\n"
                "The syntax tree is displayed below."
            )
            
        except TinyError as e:
            # Parse error
            self.status_label.config(
                text=f"✗ Parse error in file",
                fg="red"
            )
            messagebox.showerror(
                "Parse Error",
                f"Failed to parse the token file:\n\n{str(e)}\n\n"
                "The input does not follow TINY language syntax."
            )
            
        except FileNotFoundError:
            self.status_label.config(text="✗ File not found", fg="red")
            messagebox.showerror("Error", f"File not found: {filepath}")
            
        except Exception as e:
            # Other errors
            self.status_label.config(text="✗ Error loading file", fg="red")
            messagebox.showerror(
                "Error",
                f"An error occurred while loading the file:\n\n{str(e)}"
            )


def launch_gui():
    """Launch the main GUI application."""
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()


if __name__ == "__main__":
    launch_gui()
