import pytest

from ledis import Ledis
from ledis.datastructures import Set
from ledis.exceptions import InvalidType


def test_sadd_empty():
    ledis = Ledis()
    ledis.sadd("set_type", 1, 2, 3)
    assert ledis.storage["set_type"] == Set({1, 2, 3})


def test_sadd_exist():
    ledis = Ledis()
    ledis.sadd("set_type", 1, 2, 3)
    ledis.sadd("set_type", 2, 3, 4)
    assert ledis.storage["set_type"] == Set({1, 2, 3, 4})


def test_sadd_str_value():
    ledis = Ledis()
    ledis.sadd("hello", "world")

    assert ledis.storage["hello"] == Set({"world"})


def test_sadd_to_str():
    ledis = Ledis()
    ledis.set("hello", "world")

    with pytest.raises(InvalidType):
        ledis.sadd("hello", {2, 3, 4})
