from enum import unique, Enum
from typing import Union


@unique
class DataType(Enum):
    STR = "str"
    SET = "set"


class BaseDataStructure:
    __slots__ = {"data", "type", "expire_at"}

    def __init__(self, data: Union[str, set]):
        self.data = data

        # This will raise an error if type is not supported
        self.type = DataType(type(data).__name__)

        # UTC expire timestamp, in seconds
        self.expire_at = None

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            # don't attempt to compare against unrelated types
            return NotImplemented

        return (
            self.data == other.data
            and self.expire_at == other.expire_at
            and self.type == other.type
        )


class String(BaseDataStructure):
    pass


class Set(BaseDataStructure):
    pass
