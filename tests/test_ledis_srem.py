import pytest

from ledis import Ledis
from ledis.exceptions import InvalidType
from ledis.datastructures import Set


def test_srem():
    ledis = Ledis()
    ledis.sadd("set_type", *{1, 2, 3})

    ledis.srem("set_type", *{2, 3})
    assert ledis.storage["set_type"].data == {1}


def test_srem_not_exist():
    ledis = Ledis()
    ledis.srem("set_type", *{1, 2, 3})


def test_srem_str_value():
    ledis = Ledis()
    ledis.sadd("hello", 1, 2, 3)
    ledis.srem("hello", "world")

    assert ledis.storage["hello"] == Set({1, 2, 3})


def test_srem_to_str():
    ledis = Ledis()
    ledis.set("hello", "world")

    with pytest.raises(InvalidType):
        ledis.srem("hello", {2, 3, 4})
