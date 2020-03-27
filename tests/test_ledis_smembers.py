import pytest

from ledis import Ledis
from ledis.exceptions import InvalidType


ledis = Ledis()
ledis.sadd("set_type", 1, 2, 3)
ledis.set("str_type", "hello")


def test_smembers():
    assert ledis.smembers("set_type") == [1, 2, 3]


def test_smembers_not_exist():
    assert ledis.smembers("key_not_found") is None


def test_smembers_str_value():
    with pytest.raises(InvalidType):
        ledis.smembers("str_type")
