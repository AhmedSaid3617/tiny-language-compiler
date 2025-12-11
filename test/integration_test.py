"""
Comprehensive test for the TINY parser implementation.
Tests the complete pipeline from token file to syntax tree.
"""

import unittest
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.parse.token_file_parser import TokenFileParser
from src.parse.parser import Parser
from src.parse.syntax_tree import *
from src.tinyerror.tiny_error import TinyError


class TestTinyParserIntegration(unittest.TestCase):
    """Integration tests for the complete TINY parser."""
    
    def test_parse_input_sample(self):
        """Test parsing the factorial program from input_sample.txt"""
        # Parse the token file
        token_stream = TokenFileParser.parse_file('input_sample.txt')
        
        # Verify tokens were loaded
        self.assertEqual(len(token_stream.tokens), 32)
        
        # Parse with TINY parser
        parser = Parser(token_stream)
        syntax_tree = parser.parse()
        
        # Verify root is a statement sequence
        self.assertIsInstance(syntax_tree, StatementSequence)
        
        # Should have 2 top-level statements: read and if
        self.assertEqual(len(syntax_tree.statements), 2)
        
        # First statement should be read
        self.assertIsInstance(syntax_tree.statements[0], ReadStatementNode)
        self.assertEqual(syntax_tree.statements[0].identifier, "x")
        
        # Second statement should be if
        self.assertIsInstance(syntax_tree.statements[1], IfStatementNode)
        if_stmt = syntax_tree.statements[1]
        
        # If test should be a comparison: 0 < x
        self.assertIsInstance(if_stmt.test, OperatorNode)
        self.assertEqual(if_stmt.test.operator, "<")
        
        # If then-part should exist
        self.assertIsNotNone(if_stmt.then_part)
        self.assertIsInstance(if_stmt.then_part, StatementSequence)
        
        # Then-part should have 3 statements: assign, repeat, and write
        self.assertEqual(len(if_stmt.then_part.statements), 3)
        
        # First statement in then-part: fact := 1
        assign_stmt = if_stmt.then_part.statements[0]
        self.assertIsInstance(assign_stmt, AssignmentStatementNode)
        self.assertEqual(assign_stmt.identifier, "fact")
        
        # Second statement in then-part: repeat
        repeat_stmt = if_stmt.then_part.statements[1]
        self.assertIsInstance(repeat_stmt, RepeatStatementNode)
        
        # Repeat body should have 2 statements
        self.assertEqual(len(repeat_stmt.body.statements), 2)
        
        # First: fact := fact * x
        fact_assign = repeat_stmt.body.statements[0]
        self.assertIsInstance(fact_assign, AssignmentStatementNode)
        self.assertEqual(fact_assign.identifier, "fact")
        
        # Second: x := x - 1
        x_assign = repeat_stmt.body.statements[1]
        self.assertIsInstance(x_assign, AssignmentStatementNode)
        self.assertEqual(x_assign.identifier, "x")
        
        # Repeat test: x = 0
        self.assertIsInstance(repeat_stmt.test, OperatorNode)
        self.assertEqual(repeat_stmt.test.operator, "=")
        
        # Third statement in then-part: write fact
        write_stmt = if_stmt.then_part.statements[2]
        self.assertIsInstance(write_stmt, WriteStatementNode)
        
        # No else part for the if statement
        self.assertIsNone(if_stmt.else_part)
        
        print("\n✓ All structural tests passed!")
    
    def test_parse_simple_read(self):
        """Test parsing a simple read statement"""
        from src.parse.token_stream import Token, TokenStream, TokenType
        
        tokens = [
            Token(TokenType.READ, "read"),
            Token(TokenType.IDENTIFIER, "x")
        ]
        token_stream = TokenStream(tokens)
        parser = Parser(token_stream)
        
        tree = parser.parse()
        self.assertIsInstance(tree, StatementSequence)
        self.assertEqual(len(tree.statements), 1)
        self.assertIsInstance(tree.statements[0], ReadStatementNode)
        self.assertEqual(tree.statements[0].identifier, "x")
    
    def test_parse_simple_write(self):
        """Test parsing a simple write statement"""
        from src.parse.token_stream import Token, TokenStream, TokenType
        
        tokens = [
            Token(TokenType.WRITE, "write"),
            Token(TokenType.NUMBER, "42")
        ]
        token_stream = TokenStream(tokens)
        parser = Parser(token_stream)
        
        tree = parser.parse()
        self.assertIsInstance(tree, StatementSequence)
        self.assertEqual(len(tree.statements), 1)
        self.assertIsInstance(tree.statements[0], WriteStatementNode)
    
    def test_parse_assignment(self):
        """Test parsing an assignment statement"""
        from src.parse.token_stream import Token, TokenStream, TokenType
        
        tokens = [
            Token(TokenType.IDENTIFIER, "x"),
            Token(TokenType.ASSIGN, ":="),
            Token(TokenType.NUMBER, "10")
        ]
        token_stream = TokenStream(tokens)
        parser = Parser(token_stream)
        
        tree = parser.parse()
        self.assertIsInstance(tree, StatementSequence)
        stmt = tree.statements[0]
        self.assertIsInstance(stmt, AssignmentStatementNode)
        self.assertEqual(stmt.identifier, "x")
        self.assertIsInstance(stmt.expression, ConstantNode)
        self.assertEqual(stmt.expression.value, 10)
    
    def test_parse_arithmetic_expression(self):
        """Test parsing arithmetic expressions with correct precedence"""
        from src.parse.token_stream import Token, TokenStream, TokenType
        
        # x := 1 + 2 * 3
        tokens = [
            Token(TokenType.IDENTIFIER, "x"),
            Token(TokenType.ASSIGN, ":="),
            Token(TokenType.NUMBER, "1"),
            Token(TokenType.PLUS, "+"),
            Token(TokenType.NUMBER, "2"),
            Token(TokenType.MULT, "*"),
            Token(TokenType.NUMBER, "3")
        ]
        token_stream = TokenStream(tokens)
        parser = Parser(token_stream)
        
        tree = parser.parse()
        stmt = tree.statements[0]
        
        # The expression should be: + (1, * (2, 3))
        # Because * has higher precedence than +
        expr = stmt.expression
        self.assertIsInstance(expr, OperatorNode)
        self.assertEqual(expr.operator, "+")
        
        # Left should be 1
        self.assertIsInstance(expr.left, ConstantNode)
        self.assertEqual(expr.left.value, 1)
        
        # Right should be * (2, 3)
        self.assertIsInstance(expr.right, OperatorNode)
        self.assertEqual(expr.right.operator, "*")
    
    def test_parse_comparison(self):
        """Test parsing comparison expressions"""
        from src.parse.token_stream import Token, TokenStream, TokenType
        
        # write x < 10
        tokens = [
            Token(TokenType.WRITE, "write"),
            Token(TokenType.IDENTIFIER, "x"),
            Token(TokenType.LESSTHAN, "<"),
            Token(TokenType.NUMBER, "10")
        ]
        token_stream = TokenStream(tokens)
        parser = Parser(token_stream)
        
        tree = parser.parse()
        stmt = tree.statements[0]
        
        # Expression should be < (x, 10)
        expr = stmt.expression
        self.assertIsInstance(expr, OperatorNode)
        self.assertEqual(expr.operator, "<")
        self.assertIsInstance(expr.left, IdentifierNode)
        self.assertIsInstance(expr.right, ConstantNode)
    
    def test_invalid_syntax_raises_error(self):
        """Test that invalid syntax raises TinyError"""
        from src.parse.token_stream import Token, TokenStream, TokenType
        
        # Invalid: missing identifier after read
        tokens = [
            Token(TokenType.READ, "read"),
            Token(TokenType.NUMBER, "42")  # Should be identifier
        ]
        token_stream = TokenStream(tokens)
        parser = Parser(token_stream)
        
        with self.assertRaises(TinyError):
            parser.parse()


def run_integration_tests():
    """Run all integration tests."""
    print("=" * 70)
    print("TINY Parser Integration Tests")
    print("=" * 70)
    print()
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestTinyParserIntegration)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print()
    print("=" * 70)
    if result.wasSuccessful():
        print("✓ ALL TESTS PASSED!")
    else:
        print("✗ SOME TESTS FAILED")
    print("=" * 70)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_integration_tests()
    sys.exit(0 if success else 1)
