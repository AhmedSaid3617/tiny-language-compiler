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
    TIMES = "TIMES"
    DIVIDE = "DIVIDE"
    LESS_THAN = "LESS_THAN"
    GREATER_THAN = "GREATER_THAN"
    EQUAL = "EQUAL"
    IDENTIFIER = "IDENTIFIER"
    NUMBER = "NUMBER"
    SEMICOLON = "SEMICOLON"
    EOF = "EOF"