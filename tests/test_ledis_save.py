from os import path

from ledis import Ledis
from ledis.config import SNAPSHOT_DIR
from ledis.utils import file_exists


def test_save(test_snapshot_filename):
    ledis = Ledis()
    ledis.set("hello", "world")
    ledis.save(test_snapshot_filename)

    assert file_exists(path.join(SNAPSHOT_DIR, f"{test_snapshot_filename}.db"))
