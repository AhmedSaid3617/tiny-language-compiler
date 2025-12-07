# TODO: implement this.

class TinyError(Exception):
    def __init__(self, token) -> None:
        super().__init__("The source code is incorrect.")
