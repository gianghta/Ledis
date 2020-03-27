import pytest

from ledis import Ledis
from ledis.exceptions import InvalidType


ledis = Ledis()
ledis.set("hello", "world")
ledis.sadd("set_type", 1, 2, 3)


def test_get():
    assert ledis.get("hello") == "world"


def test_get_key_not_exist():
    assert ledis.get("key_not_found") is None


def test_get_key_set_type():
    with pytest.raises(InvalidType):
        ledis.get("set_type")
