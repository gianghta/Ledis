from ledis import Ledis


def test_ttl():
    ledis = Ledis()
    ledis.set("str_type", "hello")
    assert ledis.storage["str_type"].expire_at is None

    ledis.expire("str_type", 10)
    assert ledis.ttl("str_type") == 10


def test_ttl_key_not_exist():
    ledis = Ledis()
    assert ledis.ttl("str_type") == -2


def test_ttl_not_set():
    ledis = Ledis()
    ledis.set("str_type", "hello")
    assert ledis.storage["str_type"].expire_at is None
    assert ledis.ttl("str_type") == -1
