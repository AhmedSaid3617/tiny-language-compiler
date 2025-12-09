import re
from enum import Enum
from typing import Optional
from token_stream import TokenStream , Token , TokenType

KEYWORDS = {
    "read": TokenType.READ,
    "write": TokenType.WRITE,
    "if": TokenType.IF,
    "then": TokenType.THEN,
    "else": TokenType.ELSE,
    "end": TokenType.END,
    "repeat": TokenType.REPEAT,
    "until": TokenType.UNTIL,
}

SYMBOLS = {
    ";": TokenType.SEMICOLON,
    "+": TokenType.PLUS,
    "-": TokenType.MINUS,
    "*": TokenType.TIMES,
    "/": TokenType.DIVIDE,
    "<": TokenType.LESS_THAN,
    ">": TokenType.GREATER_THAN,
    "=": TokenType.EQUAL,
    ":=": TokenType.ASSIGN,
}


def tokenize_text(text: str):

    tokens = []

    # your file has one token per line
    lines = text.splitlines()

    for line in lines:
        part = line.strip()
        if not part:
            continue

        # keywords
        if part.lower() in KEYWORDS:
            tokens.append(Token(KEYWORDS[part.lower()], part))
            continue

        # :=
        if part == ":=":
            tokens.append(Token(TokenType.ASSIGN, part))
            continue

        # symbols
        if part in SYMBOLS:
            tokens.append(Token(SYMBOLS[part], part))
            continue

        # number
        if part.isdigit():
            tokens.append(Token(TokenType.NUMBER, part))
            continue

        # identifier
        if re.match(r"^[A-Za-z_]\w*$", part):
            tokens.append(Token(TokenType.IDENTIFIER, part))
            continue

        raise ValueError(f"Unknown token: {part}")

    tokens.append(Token(TokenType.EOF, ""))
    return tokens


def tokenize_file(path: str):
    with open(path, "r") as f:
        text = f.read()
    return tokenize_text(text)

# write path here 
tokens = tokenize_file(r"D:\joe.txt")
for t in tokens:
    print(t)
