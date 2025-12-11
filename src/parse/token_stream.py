from enum import Enum
from typing import Optional, Sequence


class TokenStream:
    def __init__(self, tokens: list['Token']):
        self.tokens = tokens
        self.position = 0

    def peek(self) -> Optional['Token']:
        if self.position < len(self.tokens):
            return self.tokens[self.position]
        else:
            return None
        
    def consume(self) -> None:
        if self.position < len(self.tokens):
            self.position += 1


class Token:
    def __init__(self, type_: 'TokenType', value: str):
        self.type = type_
        self.value = value

    def __repr__(self) -> str:
        return f"Token({self.type}, {self.value})"


class TokenType(Enum):
    READ = "READ"
    WRITE = "WRITE"
    IF = "IF"
    THEN = "THEN"
    ELSE = "ELSE"
    END = "END"
    REPEAT = "REPEAT"
    UNTIL = "UNTIL"
    ASSIGN = "ASSIGN"
    PLUS = "PLUS"
    MINUS = "MINUS"
    MULT = "MULT"  # Matches input file format
    DIV = "DIV"  # Matches input file format
    LESSTHAN = "LESSTHAN"  # Matches input file format
    GREATERTHAN = "GREATERTHAN"  # Matches input file format
    EQUAL = "EQUAL"
    IDENTIFIER = "IDENTIFIER"
    NUMBER = "NUMBER"
    SEMICOLON = "SEMICOLON"
    LPAREN = "LPAREN"
    RPAREN = "RPAREN"
    EOF = "EOF"