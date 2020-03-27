from ledis import Ledis


def test_delete_str():
    ledis = Ledis()
    ledis.set("str_type", "hello")
    ledis.delete("str_type")
    assert "str_type" not in ledis.storage


def test_delete_set():
    ledis = Ledis()
    ledis.sadd("set_type", 1, 2, 3)
    ledis.delete("set_type")
    assert "set_type" not in ledis.storage


def test_delete_non_exist():
    ledis = Ledis()
    ledis.delete("key_not_found")
