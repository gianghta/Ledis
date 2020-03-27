import pytest

from ledis import Ledis
from ledis.exceptions import NoSnapshotFound


def test_restore(test_snapshot_filename):
    ledis = Ledis()
    ledis.set("hello", "world")
    ledis.sadd("set_type", 1, 2, 3)
    ledis.save(test_snapshot_filename)

    # Clear current state
    ledis.storage = {}
    assert ledis.get("hello") is None
    assert ledis.get("set_type") is None

    # Restore from persistent data
    ledis.restore(test_snapshot_filename)
    assert ledis.get("hello") == "world"
    assert ledis.smembers("set_type") == [1, 2, 3]


def test_restore_without_snapshot():
    ledis = Ledis()
    with pytest.raises(NoSnapshotFound):
        ledis.restore("snapshot_not_found")
