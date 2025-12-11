"""
Tree visualizer for TINY language abstract syntax trees.
Uses Tkinter Canvas to render the AST graphically.
"""

from src.parse.syntax_tree import *
import tkinter as tk
from typing import Dict, Tuple, Optional, List


class TreeVisualizer:
    """Visualizes abstract syntax trees on a Tkinter Canvas."""
    
    def __init__(self, canvas: tk.Canvas):
        self.canvas = canvas
        self.node_spacing_x = 100  # Horizontal spacing between nodes
        self.node_spacing_y = 80  # Vertical spacing between levels
        self.node_positions: Dict[SyntaxTreeNode, Tuple[int, int]] = {}
        self.statement_sequences: List[StatementSequence] = []  # Track sequences for horizontal lines
        
    def draw_tree(self, root: SyntaxTreeNode):
        """Draw the complete syntax tree starting from root."""
        self.canvas.delete("all")  # Clear canvas
        self.node_positions.clear()
        self.statement_sequences.clear()
        
        if root is None:
            return
        
        # Calculate positions for all nodes
        self._calculate_positions(root, 0, 0)
        
        # Adjust positions to center the tree
        if self.node_positions:
            min_x = min(pos[0] for pos in self.node_positions.values())
            max_x = max(pos[0] for pos in self.node_positions.values())
            max_y = max(pos[1] for pos in self.node_positions.values())
            
            # Add margins
            margin = 50
            offset_x = margin - min_x
            offset_y = margin
            
            # Adjust all positions
            adjusted_positions = {}
            for node, (x, y) in self.node_positions.items():
                adjusted_positions[node] = (x + offset_x, y + offset_y)
            self.node_positions = adjusted_positions
            
            # Update canvas scroll region
            self.canvas.configure(scrollregion=(0, 0, max_x - min_x + 2 * margin, max_y + 2 * margin))
        
        # Draw edges first (so they appear behind nodes)
        self._draw_edges(root)
        
        # Draw horizontal lines for statement sequences
        self._draw_statement_sequence_lines()
        
        # Draw nodes
        self._draw_nodes(root)
    
    def _calculate_positions(self, node: SyntaxTreeNode, depth: int, offset: int) -> int:
        """
        Calculate positions for all nodes using a recursive layout algorithm.
        Returns the width occupied by this subtree.
        
        Special handling: StatementSequence nodes are not drawn; their children
        are positioned side by side at the same level.
        """
        if node is None:
            return 0
        
        # Special case: StatementSequence - don't draw it, just layout children side by side
        if isinstance(node, StatementSequence):
            self.statement_sequences.append(node)  # Track for horizontal lines
            child_offset = offset
            total_width = 0
            
            for child in node.get_children():
                if child is not None:
                    width = self._calculate_positions(child, depth, child_offset)
                    child_offset += width
                    total_width += width
            
            return max(total_width, self.node_spacing_x)
        
        children = [child for child in node.get_children() if child is not None]
        
        if not children:
            # Leaf node
            x = offset
            y = depth * self.node_spacing_y
            self.node_positions[node] = (x, y)
            return self.node_spacing_x
        
        # Calculate positions for children
        child_offset = offset
        total_width = 0
        
        for child in children:
            width = self._calculate_positions(child, depth + 1, child_offset)
            child_offset += width
            total_width += width
        
        # Position this node centered above its children
        # For StatementSequence children, we need to find their first and last grandchildren
        def get_leftmost_positioned_node(n):
            """Get the leftmost node that has a position."""
            if n in self.node_positions:
                return n
            if isinstance(n, StatementSequence):
                for child in n.get_children():
                    if child is not None:
                        result = get_leftmost_positioned_node(child)
                        if result:
                            return result
            return None
        
        def get_rightmost_positioned_node(n):
            """Get the rightmost node that has a position."""
            if n in self.node_positions:
                return n
            if isinstance(n, StatementSequence):
                for child in reversed(n.get_children()):
                    if child is not None:
                        result = get_rightmost_positioned_node(child)
                        if result:
                            return result
            return None
        
        leftmost = get_leftmost_positioned_node(children[0])
        rightmost = get_rightmost_positioned_node(children[-1])
        
        if leftmost and rightmost:
            first_child_x = self.node_positions[leftmost][0]
            last_child_x = self.node_positions[rightmost][0]
            x = (first_child_x + last_child_x) // 2
        else:
            x = offset
        
        y = depth * self.node_spacing_y
        self.node_positions[node] = (x, y)
        
        return max(total_width, self.node_spacing_x)
    
    def _draw_edges(self, node: SyntaxTreeNode):
        """Draw edges connecting nodes to their children.
        
        For StatementSequence children: connect parent to first child only,
        then horizontal lines connect siblings.
        """
        if node not in self.node_positions:
            # Node is not drawn (e.g., StatementSequence), but process its children
            if isinstance(node, StatementSequence):
                for child in node.get_children():
                    if child is not None:
                        self._draw_edges(child)
            return
        
        parent_x, parent_y = self.node_positions[node]
        
        for child in node.get_children():
            if child is None:
                continue
                
            # Special case: if child is a StatementSequence, connect to first child only
            if isinstance(child, StatementSequence):
                seq_children = [c for c in child.get_children() if c is not None and c in self.node_positions]
                if seq_children:
                    # Only connect to the first child in the sequence
                    first_child = seq_children[0]
                    first_x, first_y = self.node_positions[first_child]
                    
                    # Draw line from parent to first child
                    self.canvas.create_line(
                        parent_x, parent_y + 20,  # Bottom of parent node
                        first_x, first_y - 20,    # Top of first child
                        width=2,
                        fill="black"
                    )
                
                # Recursively process grandchildren
                for grandchild in child.get_children():
                    if grandchild is not None:
                        self._draw_edges(grandchild)
            elif child in self.node_positions:
                child_x, child_y = self.node_positions[child]
                
                # Draw line from parent to child
                self.canvas.create_line(
                    parent_x, parent_y + 20,  # Bottom of parent node
                    child_x, child_y - 20,    # Top of child node
                    width=2,
                    fill="black"
                )
                
                # Recursively draw edges for children
                self._draw_edges(child)
    
    def _draw_statement_sequence_lines(self):
        """Draw horizontal lines connecting statement sequence siblings."""
        for seq in self.statement_sequences:
            seq_children = [c for c in seq.get_children() if c is not None and c in self.node_positions]
            
            if len(seq_children) > 1:
                for i in range(len(seq_children) - 1):
                    left_child = seq_children[i]
                    right_child = seq_children[i + 1]
                    left_x, left_y = self.node_positions[left_child]
                    right_x, right_y = self.node_positions[right_child]
                    
                    # Draw horizontal line at the same level
                    mid_y = left_y  # Should be same as right_y
                    
                    # Draw line from right edge of left node to left edge of right node
                    self.canvas.create_line(
                        left_x + 40, mid_y,  # Right edge of left node
                        right_x - 40, mid_y,  # Left edge of right node
                        width=2,
                        fill="black"
                    )
    
    def _draw_nodes(self, node: SyntaxTreeNode):
        """Draw all nodes in the tree.
        
        Special handling: StatementSequence nodes are not drawn; only their children are drawn.
        """
        # Skip drawing StatementSequence nodes
        if isinstance(node, StatementSequence):
            for child in node.get_children():
                if child is not None:
                    self._draw_nodes(child)
            return
        
        if node not in self.node_positions:
            return
        
        x, y = self.node_positions[node]
        
        # Determine node shape and label based on node type
        is_oval = isinstance(node, (OperatorNode, IdentifierNode, ConstantNode))
        label = self._get_node_label(node)
        
        # Draw node shape
        if is_oval:
            # Oval for expressions and operators
            self.canvas.create_oval(
                x - 35, y - 20,
                x + 35, y + 20,
                fill="white",
                outline="black",
                width=2
            )
        else:
            # Rectangle for statements
            self.canvas.create_rectangle(
                x - 40, y - 20,
                x + 40, y + 20,
                fill="white",
                outline="black",
                width=2
            )
        
        # Draw label
        self.canvas.create_text(
            x, y,
            text=label,
            font=("Arial", 10, "bold")
        )
        
        # Recursively draw children
        for child in node.get_children():
            if child is not None:
                self._draw_nodes(child)
    
    def _get_node_label(self, node: SyntaxTreeNode) -> str:
        """Get the display label for a node."""
        if isinstance(node, ReadStatementNode):
            return f"read\n({node.identifier})"
        elif isinstance(node, WriteStatementNode):
            return "write"
        elif isinstance(node, AssignmentStatementNode):
            return f"assign\n({node.identifier})"
        elif isinstance(node, IfStatementNode):
            return "if"
        elif isinstance(node, RepeatStatementNode):
            return "repeat"
        elif isinstance(node, OperatorNode):
            return f"op\n({node.operator})"
        elif isinstance(node, IdentifierNode):
            return f"id\n({node.name})"
        elif isinstance(node, ConstantNode):
            return f"const\n({node.value})"
        elif isinstance(node, StatementSequence):
            return "stmt-seq"
        else:
            return "node"
