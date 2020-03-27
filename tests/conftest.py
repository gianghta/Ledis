from os import remove
import pytest

from ledis.utils import file_exists, get_snapshot_filepath


TEST_SNAPSHOT_FILENAME = "test_data"


@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    filename = f"{get_snapshot_filepath(TEST_SNAPSHOT_FILENAME)}.db"
    if file_exists(filename):
        remove(filename)

    # Run the tests
    yield

    # Post-cleanup
    if file_exists(filename):
        remove(filename)


@pytest.fixture
def test_snapshot_filename():
    return TEST_SNAPSHOT_FILENAME
