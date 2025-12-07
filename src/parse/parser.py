from src.parse.syntax_tree import *
from src.parse.token_stream import *
from src.tinyerror.tiny_error import TinyError

# TODO: implement this.
class Parser:
    def __init__(self, token_stream: 'TokenStream'):
        self.token_stream = token_stream

    def match(self, expected_type: 'TokenType') -> bool:
        if self.token_stream.peek() is not None and self.token_stream.peek().type == expected_type:
            self.token_stream.consume()
            return True
        
        raise TinyError(self.token_stream.peek(), self.token_stream.position)
    

    def parse(self) -> 'SyntaxTreeNode':
        ...
    
    def parse_program(self) -> 'SyntaxTreeNode':
        ...

    def parse_statement_sequence(self) -> 'SyntaxTreeNode':
        ...
    
    def parse_statement(self) -> 'SyntaxTreeNode':
        ...