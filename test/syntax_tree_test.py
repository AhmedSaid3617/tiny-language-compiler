import unittest
from src.parse.syntax_tree import *

class TestSyntaxTreeNode(unittest.TestCase):
    def test_initialization(self):

        read_stmt = ReadStatementNode("x")
        self.assertEqual(read_stmt.identifier, "x")

        id_stmt = IdentifierNode("x")
        self.assertEqual(id_stmt.name, "x")

        const_stmt = ConstantNode(1)
        self.assertEqual(const_stmt.value, 1)

        opnode = OperatorNode("+", id_stmt, const_stmt)
        self.assertEqual(opnode.operator, "+")
        self.assertEqual(opnode.left, id_stmt)
        self.assertEqual(opnode.right, const_stmt)

        assign_stmt = AssignmentStatementNode("x", opnode)
        self.assertEqual(assign_stmt.identifier, "x")
        self.assertEqual(assign_stmt.expression, opnode)


        write_stmt = WriteStatementNode(opnode)
        self.assertEqual(write_stmt.expression, opnode)

        program = StatementSequence([read_stmt, assign_stmt, write_stmt])
        self.assertEqual(program.statements, [read_stmt, assign_stmt, write_stmt])

        print("All SyntaxTreeNode initialization tests passed.")