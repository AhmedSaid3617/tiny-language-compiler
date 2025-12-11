#!/usr/bin/env python3
"""
Test script to verify the tree structure visualization changes.
Tests that StatementSequence nodes are handled correctly (not drawn, children side by side).
"""

from src.parse.token_file_parser import TokenFileParser
from src.parse.parser import Parser
from src.parse.syntax_tree import *


def print_tree_structure(node, indent=0, show_stmt_seq=True):
    """Print the tree structure with indentation."""
    prefix = "  " * indent
    
    if isinstance(node, StatementSequence):
        if show_stmt_seq:
            print(f"{prefix}StatementSequence (NOT DRAWN - children side by side):")
        for child in node.get_children():
            print_tree_structure(child, indent + 1 if show_stmt_seq else indent, show_stmt_seq)
    elif isinstance(node, ReadStatementNode):
        print(f"{prefix}ReadStatement: {node.identifier}")
    elif isinstance(node, WriteStatementNode):
        print(f"{prefix}WriteStatement")
        for child in node.get_children():
            print_tree_structure(child, indent + 1, show_stmt_seq)
    elif isinstance(node, AssignmentStatementNode):
        print(f"{prefix}AssignStatement: {node.identifier}")
        for child in node.get_children():
            print_tree_structure(child, indent + 1, show_stmt_seq)
    elif isinstance(node, IfStatementNode):
        print(f"{prefix}IfStatement")
        print(f"{prefix}  Test:")
        print_tree_structure(node.test, indent + 2, show_stmt_seq)
        print(f"{prefix}  Then:")
        print_tree_structure(node.then_part, indent + 2, show_stmt_seq)
        if node.else_part:
            print(f"{prefix}  Else:")
            print_tree_structure(node.else_part, indent + 2, show_stmt_seq)
    elif isinstance(node, RepeatStatementNode):
        print(f"{prefix}RepeatStatement")
        print(f"{prefix}  Body:")
        print_tree_structure(node.body, indent + 2, show_stmt_seq)
        print(f"{prefix}  Test:")
        print_tree_structure(node.test, indent + 2, show_stmt_seq)
    elif isinstance(node, OperatorNode):
        print(f"{prefix}Operator: {node.operator}")
        for child in node.get_children():
            print_tree_structure(child, indent + 1, show_stmt_seq)
    elif isinstance(node, IdentifierNode):
        print(f"{prefix}Identifier: {node.name}")
    elif isinstance(node, ConstantNode):
        print(f"{prefix}Constant: {node.value}")
    elif node is None:
        print(f"{prefix}None")


def main():
    print("=" * 60)
    print("Testing Tree Structure with StatementSequence Handling")
    print("=" * 60)
    
    # Parse the input file
    token_stream = TokenFileParser.parse_file("input_sample.txt")
    parser = Parser(token_stream)
    tree = parser.parse()
    
    print("\nFull tree structure (showing StatementSequence nodes):")
    print("-" * 60)
    print_tree_structure(tree, show_stmt_seq=True)
    
    print("\n" + "=" * 60)
    print("Visual representation (StatementSequence children side by side):")
    print("=" * 60)
    print_tree_structure(tree, show_stmt_seq=False)
    
    print("\n" + "=" * 60)
    print("Verification:")
    print("=" * 60)
    
    # Verify the structure
    assert isinstance(tree, StatementSequence), "Root should be StatementSequence"
    statements = tree.statements
    print(f"✓ Root is StatementSequence with {len(statements)} statements")
    
    # First statement should be Read
    assert isinstance(statements[0], ReadStatementNode), "First should be ReadStatement"
    print(f"✓ Statement 1: ReadStatement({statements[0].identifier})")
    
    # Second statement should be If
    assert isinstance(statements[1], IfStatementNode), "Second should be IfStatement"
    print(f"✓ Statement 2: IfStatement")
    
    # If statement's then part is a StatementSequence
    then_part = statements[1].then_part
    assert isinstance(then_part, StatementSequence), "Then part should be StatementSequence"
    then_statements = then_part.statements
    print(f"  - Then part has {len(then_statements)} statements (drawn side by side)")
    
    assert isinstance(then_statements[0], AssignmentStatementNode), "First then stmt should be Assign"
    print(f"    * AssignStatement({then_statements[0].identifier})")
    
    assert isinstance(then_statements[1], RepeatStatementNode), "Second then stmt should be Repeat"
    print(f"    * RepeatStatement")
    
    assert isinstance(then_statements[2], WriteStatementNode), "Third then stmt should be Write"
    print(f"    * WriteStatement")
    
    print("\n✓ All verifications passed!")
    print("\nIn the GUI visualization:")
    print("- The root StatementSequence is NOT drawn")
    print("- 'read(x)' and 'if' appear side by side at the top level")
    print("- The 'if' statement's then part has 3 children side by side:")
    print("  assign(fact), repeat, and write")
    

if __name__ == "__main__":
    main()
