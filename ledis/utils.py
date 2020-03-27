from os import getcwd, mkdir, path
from time import time
from typing import Any

from ledis.config import SNAPSHOT_DIR, SNAPSHOT_FILENAME
from ledis.datastructures import BaseDataStructure
from ledis.exceptions import InvalidType


def convert_to_int(value: Any) -> int:
    try:
        return int(value)
    except ValueError:
        raise InvalidType("Value '{value}' is not a valid integer")


def check_type(val: BaseDataStructure, data_type: str):
    if val.type != data_type:
        raise InvalidType(
            f"The value is expected to be type <{data_type.value}>, "
            f"but <{val.type.value}> found"
        )


def file_exists(filename: str):
    return path.isfile(filename)


def mkdir_if_not_exists(directory: str) -> str:
    directory = path.join(getcwd(), directory)
    if not path.isdir(directory):
        try:
            mkdir(directory)
        except OSError:
            pass

    return directory


def get_snapshot_filepath(filename: str = None) -> str:
    filename = filename or SNAPSHOT_FILENAME
    directory = mkdir_if_not_exists(SNAPSHOT_DIR)
    return path.join(directory, filename)


def get_timestamp():
    return int(time())
