import unittest
from src.parse.syntax_tree import *
from src.parse.parser import Parser
from src.parse.token_stream import TokenStream, Token, TokenType
from src.tinyerror.tiny_error import TinyError


class TestParser(unittest.TestCase):
    
    def test_parser_initialization(self):
        """Test that parser can be initialized with a token stream"""
        tokens = [Token(TokenType.NUMBER, "42")]
        token_stream = TokenStream(tokens)
        parser = Parser(token_stream)
        
        self.assertIsNotNone(parser)
        self.assertEqual(parser.token_stream, token_stream)
    
    def test_match_success(self):
        """Test match function when token type matches"""
        tokens = [Token(TokenType.NUMBER, "42"), Token(TokenType.PLUS, "+")]
        token_stream = TokenStream(tokens)
        parser = Parser(token_stream)
        
        # Should match and consume the NUMBER token
        result = parser.match(TokenType.NUMBER)
        self.assertTrue(result)
        
        # Position should have advanced
        self.assertEqual(token_stream.position, 1)
        
        # Next token should be PLUS
        self.assertEqual(token_stream.peek().type, TokenType.PLUS)
    
    def test_match_failure(self):
        """Test match function when token type doesn't match"""
        tokens = [Token(TokenType.NUMBER, "42")]
        token_stream = TokenStream(tokens)
        parser = Parser(token_stream)
        
        # Should raise TinyError when trying to match wrong type
        with self.assertRaises(TinyError):
            parser.match(TokenType.PLUS)
    
    def test_match_at_end_of_stream(self):
        """Test match function when at end of token stream"""
        tokens = []
        token_stream = TokenStream(tokens)
        parser = Parser(token_stream)
        
        # Should raise TinyError when no tokens left
        with self.assertRaises(TinyError) as e:
            parser.match(TokenType.NUMBER)

        # Check the error message
        self.assertIn("TinyError at position 0", str(e.exception))
        self.assertIn("unexpected token None", str(e.exception))


if __name__ == '__main__':
    unittest.main()