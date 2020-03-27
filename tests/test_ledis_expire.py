from time import sleep
import pytest

from ledis import Ledis
from ledis.exceptions import InvalidValue


def test_expire_str():
    ledis = Ledis()
    ledis.set("str_type", "hello")
    assert ledis.expire("str_type", 1) == 1
    sleep(2)

    # The key will only be lazy-deleted
    # if the key is called in any operations
    assert "str_type" in ledis.storage
    assert ledis.get("str_type") is None
    assert "str_type" not in ledis.storage


def test_expire_set():
    ledis = Ledis()
    ledis.sadd("set_type", 1, 2, 3)
    assert ledis.expire("set_type", 1) == 1
    sleep(2)

    # The key will only be lazy-deleted
    # if the key is called in any operations
    assert "set_type" in ledis.storage
    assert ledis.get("set_type") is None
    assert "set_type" not in ledis.storage


def test_expire_invalid_seconds():
    ledis = Ledis()
    ledis.set("str_type", "hello")

    with pytest.raises(InvalidValue):
        ledis.expire("str_type", -1)

    with pytest.raises(InvalidValue):
        ledis.expire("str_type", 0)


def test_expire_key_not_exist():
    ledis = Ledis()
    assert ledis.expire("key_not_found", 1) == -1
