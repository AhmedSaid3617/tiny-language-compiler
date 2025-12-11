#!/usr/bin/env python3
"""
Demo script to verify the TINY parser works correctly.
Shows parsing and tree structure without launching the GUI.
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.parse.token_file_parser import TokenFileParser
from src.parse.parser import Parser
from src.parse.syntax_tree import *


def print_tree(node, indent=0, prefix=""):
    """Print the syntax tree in a readable format."""
    indent_str = "  " * indent
    
    if isinstance(node, ReadStatementNode):
        print(f"{indent_str}{prefix}READ({node.identifier})")
    elif isinstance(node, WriteStatementNode):
        print(f"{indent_str}{prefix}WRITE")
        print_tree(node.expression, indent + 1, "expr: ")
    elif isinstance(node, AssignmentStatementNode):
        print(f"{indent_str}{prefix}ASSIGN({node.identifier})")
        print_tree(node.expression, indent + 1, "value: ")
    elif isinstance(node, IfStatementNode):
        print(f"{indent_str}{prefix}IF")
        print_tree(node.test, indent + 1, "test: ")
        print(f"{indent_str}  THEN:")
        print_tree(node.then_part, indent + 2)
        if node.else_part:
            print(f"{indent_str}  ELSE:")
            print_tree(node.else_part, indent + 2)
    elif isinstance(node, RepeatStatementNode):
        print(f"{indent_str}{prefix}REPEAT")
        print(f"{indent_str}  body:")
        print_tree(node.body, indent + 2)
        print(f"{indent_str}  UNTIL:")
        print_tree(node.test, indent + 2)
    elif isinstance(node, OperatorNode):
        print(f"{indent_str}{prefix}OP({node.operator})")
        print_tree(node.left, indent + 1, "left: ")
        print_tree(node.right, indent + 1, "right: ")
    elif isinstance(node, IdentifierNode):
        print(f"{indent_str}{prefix}ID({node.name})")
    elif isinstance(node, ConstantNode):
        print(f"{indent_str}{prefix}CONST({node.value})")
    elif isinstance(node, StatementSequence):
        if prefix:
            print(f"{indent_str}{prefix}STATEMENT-SEQUENCE")
        for i, stmt in enumerate(node.statements, 1):
            print_tree(stmt, indent, f"[{i}] ")


def demo():
    """Demonstrate the parser with the sample input."""
    print("=" * 70)
    print("TINY Language Parser - Demo")
    print("=" * 70)
    print()
    
    # Parse the sample input file
    print("📂 Loading token file: input_sample.txt")
    try:
        token_stream = TokenFileParser.parse_file('input_sample.txt')
        print(f"✓ Loaded {len(token_stream.tokens)} tokens\n")
    except FileNotFoundError:
        print("✗ Error: input_sample.txt not found")
        print("  Make sure to run this script from the project root directory")
        sys.exit(1)
    
    # Parse with TINY parser
    print("🔍 Parsing with TINY grammar...")
    try:
        parser = Parser(token_stream)
        syntax_tree = parser.parse()
        print("✓ Parse successful!\n")
    except Exception as e:
        print(f"✗ Parse error: {e}")
        sys.exit(1)
    
    # Display tree structure
    print("=" * 70)
    print("Abstract Syntax Tree Structure:")
    print("=" * 70)
    print()
    print_tree(syntax_tree)
    print()
    
    # Summary
    print("=" * 70)
    print("Summary:")
    print("=" * 70)
    print(f"✓ Root node: {type(syntax_tree).__name__}")
    print(f"✓ Top-level statements: {len(syntax_tree.statements)}")
    print(f"✓ Statement types:")
    for i, stmt in enumerate(syntax_tree.statements, 1):
        print(f"  {i}. {type(stmt).__name__}")
    print()
    print("🎉 Parser is working correctly!")
    print()
    print("To see the graphical syntax tree visualization, run:")
    print("  python main.py")
    print()


if __name__ == "__main__":
    demo()
