from ledis import Ledis


def test_keys():
    ledis = Ledis()
    ledis.set("str_type", "hello")
    ledis.sadd("set_type", 1, 2, 3)

    assert ledis.keys() == ["str_type", "set_type"]


def test_keys_empty():
    ledis = Ledis()
    assert ledis.keys() == []
