"""
Parser for TINY language token files.
Reads formatted token files and converts them to TokenStream objects.
"""

from src.parse.token_stream import Token, TokenStream, TokenType
from typing import List


class TokenFileParser:
    """Parses token files in the format:
    Token Value         Token Type
    ----------------------------------------
    read                READ
    x                   IDENTIFIER
    ...
    """
    
    def __init__(self):
        pass
    
    @staticmethod
    def parse_file(filepath: str) -> TokenStream:
        """Parse a token file and return a TokenStream."""
        tokens = []
        
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # Skip header lines
        started = False
        for line in lines:
            line = line.strip()
            
            # Skip empty lines and header
            if not line or line.startswith('TINY Language') or line.startswith('===') or line.startswith('Token Value'):
                continue
            
            # Skip separator line
            if line.startswith('---'):
                started = True
                continue
            
            # Skip total tokens line
            if line.startswith('Total tokens:'):
                break
            
            if started:
                # Parse token line
                parts = line.split()
                if len(parts) >= 2:
                    token_value = parts[0]
                    token_type_str = parts[-1]  # Last part is always token type
                    
                    # Convert token type string to TokenType enum
                    try:
                        token_type = TokenType[token_type_str]
                        tokens.append(Token(token_type, token_value))
                    except KeyError:
                        # Handle unknown token types
                        print(f"Warning: Unknown token type '{token_type_str}', skipping")
        
        return TokenStream(tokens)
