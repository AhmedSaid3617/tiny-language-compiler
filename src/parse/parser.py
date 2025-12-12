from src.parse.syntax_tree import *
from src.parse.token_stream import *
from src.tinyerror.tiny_error import TinyError

class Parser:
    """
    Recursive descent parser for TINY language.
    Implements the TINY grammar rules with EBNF conversion for left-recursive rules.
    """
    
    def __init__(self, token_stream: 'TokenStream'):
        self.token_stream = token_stream

    def match(self, expected_type: 'TokenType') -> Token:
        """Match and consume a token of expected type, or raise error."""
        current_token = self.token_stream.peek()
        if current_token is not None and current_token.type == expected_type:
            self.token_stream.consume()
            return current_token
        
        raise TinyError(current_token, self.token_stream.position)
    
    def parse(self) -> 'SyntaxTreeNode':
        """Parse the entire program and return the root of the syntax tree."""
        return self.parse_program()
    
    def parse_program(self) -> 'SyntaxTreeNode':
        """
        Grammar rule: program → stmt-sequence
        """
        return self.parse_statement_sequence()

    def parse_statement_sequence(self) -> 'StatementSequence':
        """
        Grammar rule: stmt-sequence → statement { ; statement }
        (EBNF conversion of: stmt-sequence → stmt-sequence ; statement | statement)
        """
        statements = []
        statements.append(self.parse_statement())
        
        while self.token_stream.peek() is not None and self.token_stream.peek().type == TokenType.SEMICOLON:
            self.match(TokenType.SEMICOLON)
            statements.append(self.parse_statement())
        
        return StatementSequence(statements)
    
    def parse_statement(self) -> 'StatementNode':
        """
        Grammar rule: statement → if-stmt | repeat-stmt | assign-stmt | read-stmt | write-stmt
        """
        current_token = self.token_stream.peek()
        
        if current_token is None:
            raise TinyError(current_token, self.token_stream.position)
        
        if current_token.type == TokenType.IF:
            return self.parse_if_stmt()
        elif current_token.type == TokenType.REPEAT:
            return self.parse_repeat_stmt()
        elif current_token.type == TokenType.READ:
            return self.parse_read_stmt()
        elif current_token.type == TokenType.WRITE:
            return self.parse_write_stmt()
        elif current_token.type == TokenType.IDENTIFIER:
            return self.parse_assign_stmt()
        else:
            raise TinyError(current_token, self.token_stream.position)
    
    def parse_if_stmt(self) -> 'IfStatementNode':
        """
        Grammar rule: if-stmt → if exp then stmt-sequence end
                              | if exp then stmt-sequence else stmt-sequence end
        """
        self.match(TokenType.IF)
        test = self.parse_exp()
        self.match(TokenType.THEN)
        then_part = self.parse_statement_sequence()
        
        else_part = None
        current_token = self.token_stream.peek()
        
        if current_token is not None and current_token.type == TokenType.ELSE:
            self.match(TokenType.ELSE)
            else_part = self.parse_statement_sequence()
        
        self.match(TokenType.END)
        return IfStatementNode(test, then_part, else_part)
    
    def parse_repeat_stmt(self) -> 'RepeatStatementNode':
        """
        Grammar rule: repeat-stmt → repeat stmt-sequence until exp
        """
        self.match(TokenType.REPEAT)
        body = self.parse_statement_sequence()
        self.match(TokenType.UNTIL)
        test = self.parse_exp()
        
        return RepeatStatementNode(body, test)
    
    def parse_assign_stmt(self) -> 'AssignmentStatementNode':
        """
        Grammar rule: assign-stmt → identifier := exp
        """
        identifier_token = self.match(TokenType.IDENTIFIER)
        self.match(TokenType.ASSIGN)
        expression = self.parse_exp()
        
        return AssignmentStatementNode(identifier_token.value, expression)
    
    def parse_read_stmt(self) -> 'ReadStatementNode':
        """
        Grammar rule: read-stmt → read identifier
        """
        self.match(TokenType.READ)
        identifier_token = self.match(TokenType.IDENTIFIER)
        
        return ReadStatementNode(identifier_token.value)
    
    def parse_write_stmt(self) -> 'WriteStatementNode':
        """
        Grammar rule: write-stmt → write exp
        """
        self.match(TokenType.WRITE)
        expression = self.parse_exp()
        
        return WriteStatementNode(expression)
    
    def parse_exp(self) -> 'ExpressionNode':
        """
        Grammar rule: exp → simple-exp comparison-op simple-exp | simple-exp
        """
        left = self.parse_simple_exp()
        
        current_token = self.token_stream.peek()
        if current_token is not None and current_token.type in [TokenType.LESSTHAN, TokenType.EQUAL, TokenType.GREATERTHAN]:
            op_token = self.token_stream.peek()
            self.token_stream.consume()
            right = self.parse_simple_exp()
            return OperatorNode(op_token.value, left, right)
        
        return left
    
    def parse_simple_exp(self) -> 'ExpressionNode':
        """
        Grammar rule: simple-exp → term { addop term }
        (EBNF conversion of: simple-exp → simple-exp addop term | term)
        """
        left = self.parse_term()
        
        while self.token_stream.peek() is not None and self.token_stream.peek().type in [TokenType.PLUS, TokenType.MINUS]:
            op_token = self.token_stream.peek()
            self.token_stream.consume()
            right = self.parse_term()
            left = OperatorNode(op_token.value, left, right)
        
        return left
    
    def parse_term(self) -> 'ExpressionNode':
        """
        Grammar rule: term → factor { mulop factor }
        (EBNF conversion of: term → term mulop factor | factor)
        """
        left = self.parse_factor()
        
        while self.token_stream.peek() is not None and self.token_stream.peek().type in [TokenType.MULT, TokenType.DIV]:
            op_token = self.token_stream.peek()
            self.token_stream.consume()
            right = self.parse_factor()
            left = OperatorNode(op_token.value, left, right)
        
        return left
    
    def parse_factor(self) -> 'ExpressionNode':
        """
        Grammar rule: factor → (exp) | number | identifier
        """
        current_token = self.token_stream.peek()
        
        if current_token is None:
            raise TinyError(current_token, self.token_stream.position)
        
        if current_token.type == TokenType.LPAREN:
            self.match(TokenType.LPAREN)
            exp = self.parse_exp()
            self.match(TokenType.RPAREN)
            return exp
        elif current_token.type == TokenType.NUMBER:
            number_token = self.match(TokenType.NUMBER)
            return ConstantNode(int(number_token.value))
        elif current_token.type == TokenType.IDENTIFIER:
            identifier_token = self.match(TokenType.IDENTIFIER)
            return IdentifierNode(identifier_token.value)
        else:
            raise TinyError(current_token, self.token_stream.position)
