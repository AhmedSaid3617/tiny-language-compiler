class TinyError(Exception):
    def __init__(self, message, token) -> None:
        super().__init__(message)
