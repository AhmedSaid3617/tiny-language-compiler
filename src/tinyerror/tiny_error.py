# TODO: implement this.

from src.parse.token_stream import Token

class TinyError(Exception):
    def __init__(self, token: 'Token', position: int) -> None:
        super().__init__("TinyError at position {}: unexpected token {}".format(position, token))
