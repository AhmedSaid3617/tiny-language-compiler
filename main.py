#!/usr/bin/env python3
"""
TINY Language Parser - Main Entry Point

This is a recursive descent parser for the TINY programming language.
It reads token streams from files and generates abstract syntax trees (AST).

Usage:
    python main.py

This will launch a GUI application where you can:
1. Load a token file (like input_sample.txt)
2. View the generated syntax tree
3. Check if the input is syntactically correct
"""

import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.gui.main_window import launch_gui


def main():
    """Main entry point for the TINY parser application."""
    print("=" * 60)
    print("TINY Language Parser")
    print("=" * 60)
    print("\nLaunching GUI application...")
    print("Load a token file to see the syntax tree visualization.\n")
    
    try:
        launch_gui()
    except KeyboardInterrupt:
        print("\n\nApplication closed by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n\nError: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
