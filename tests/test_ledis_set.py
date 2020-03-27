import pytest

from ledis import Ledis
from ledis.exceptions import InvalidType
from ledis.datastructures import String

ledis = Ledis()


def test_set():
    assert ledis.set("hello", "world") is None
    assert "hello" in ledis.storage
    assert ledis.storage["hello"] == String("world")


def test_set_using_set_type():
    with pytest.raises(InvalidType):
        ledis.set("set_type", {1, 2, 3})
