from starlette.exceptions import HTTPException


class LedisException(HTTPException):
    def __init__(self, detail: str = None):
        super().__init__(status_code=200, detail=detail)


class InvalidType(LedisException):
    pass


class InvalidValue(LedisException):
    pass


class NoSnapshotFound(LedisException):
    pass


class InvalidUsage(LedisException):
    """
    This exception can be raised for:
        - Malformed request syntax.
        - Invalid request message parameters.
        - Deceptive request routing.
        etc.
    The client SHOULD NOT repeat the request without modifications.
    """
