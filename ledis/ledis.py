import shelve
from typing import Any, List, Union

from ledis.datastructures import DataType, Set, String
from ledis.exceptions import InvalidValue, NoSnapshotFound
from ledis.utils import (
    convert_to_int,
    check_type,
    file_exists,
    get_snapshot_filepath,
    get_timestamp,
)


class Ledis:
    __slots__ = {"storage"}

    def __init__(self):
        self.storage = {}

    def __get_key(self, key: str, *, default_missing=None):
        """
        Return the value of a key, or `default_missing` if the key doesn't exist.

        If the key exists and has expired, it will be removed from the storage
        and the returned value will be `default_missing`.
        """
        val = self.storage.get(key)
        current_time = get_timestamp()

        if val is None:
            return default_missing

        # Expired key
        if val.expire_at is not None and current_time > val.expire_at:
            del self.storage[key]
            return default_missing

        return val

    def set(self, key: str, value: str) -> None:
        """
        Set key to hold the string value.

        If key already holds a value, it is overwritten, regardless of its type,
        and any previous TTL associated with the key is discarded.
        """
        new_val = String(value)
        check_type(new_val, DataType.STR)
        self.storage[key] = new_val

    def get(self, key: str) -> Union[str, set, None]:
        """
        Get the value of key.
        If the key does not exist, None is returned.

        An error is raised if the value stored at key is not a string,
        because GET only handles string values.
        """
        val = self.__get_key(key)
        if val is None:
            return val

        check_type(val, DataType.STR)
        return val.data

    def sadd(self, key: str, *args) -> None:
        """
        Add the specified members to the set stored at key.
        Specified members that are already a member of this set are ignored.
        If key does not exist, a new set is created before adding the specified members.

        An error is raised when the value stored at key is not a set.
        """
        cur_val = self.__get_key(key)
        if cur_val is None:
            self.storage[key] = Set(set(args))
            return

        check_type(cur_val, DataType.SET)

        # Add the values to the set
        self.storage[key].data.update(args)

    def srem(self, key: str, *args) -> None:
        """
        Remove the specified members from the set stored at key.
        Specified members that are not a member of this set are ignored.
        If key does not exist, it is treated as an empty set.

        An error is raised when the value stored at key is not a set.
        """

        prev_set = self.__get_key(key)

        # Ignore if the key is not found
        if prev_set is None:
            return

        check_type(prev_set, DataType.SET)

        # Remove the values
        for value in args:
            prev_set.data.discard(value)

        self.storage[key] = prev_set

    def smembers(self, key: str) -> Union[List[Any], None]:
        """
        Returns all the members of the set value stored at key.

        An error is raised when the value stored at key is not a set.
        """
        val = self.__get_key(key)
        if val is None:
            return None

        check_type(val, DataType.SET)
        return list(val.data)

    def sinter(self, *args) -> List[Any]:
        """
        Returns the members of the set resulting from the intersection of all the given sets.

        Keys that do not exist are considered to be empty sets.
        With one of the keys being an empty set, the resulting set is also empty
        (since set intersection with an empty set always results in an empty set).
        """
        commons = None
        for key in args:
            val = self.__get_key(key)
            if val is not None:
                check_type(val, DataType.SET)
                if commons is None:
                    commons = val.data
                else:
                    commons = commons.intersection(val.data)
        return list(commons)

    def keys(self) -> List[str]:
        """
        Return a list of all available keys.
        """
        return list(self.storage.keys())

    def delete(self, key: str) -> None:
        """
        Removes the specified keys. A key is ignored if it does not exist.
        """
        self.storage.pop(key, None)

    def expire(self, key: str, seconds: str) -> int:
        """
        Set a timeout on key.
        After the timeout has expired, the key will only be lazy-deleted
        if the key is called in any operations.

        Returns:
            int:
                The number of seconds if the timeout is set.
                Otherwise, return -1 if key does not exist.
        """
        seconds = convert_to_int(seconds)
        if seconds <= 0:
            raise InvalidValue(
                f"The timeout is expected to be a positive integer, "
                f"but got {seconds}"
            )

        if key not in self.storage:
            return -1

        self.storage[key].expire_at = get_timestamp() + seconds
        return seconds

    def ttl(self, key: str) -> int:
        """
        Return the remaining time to live of a key that has a timeout.

        Returns:
            int:
                The number of seconds if the timeout is set.
                -2 if the key does not exist.
                -1 if the key exists but has no associated expire.
        """
        val = self.__get_key(key)
        current_time = get_timestamp()

        if val is None:
            return -2

        if val.expire_at is None:
            return -1

        return val.expire_at - current_time

    def save(self, filename: str = None) -> None:
        """
        The SAVE commands performs a save of the dataset
        producing a point in time snapshot of all the data inside the instance.
        """
        filepath = get_snapshot_filepath(filename)
        with shelve.open(filepath) as data:
            data["snapshot"] = self.storage

    def restore(self, filename: str = None) -> None:
        """
        Load the persisted snapshot from the SAVE command to the storage

        An error is raised if there are no stored snapshots.
        """

        filepath = get_snapshot_filepath(filename)

        # The filename of Shelve data has an extension of `.db`
        full_filepath = f"{filepath}.db"
        if not file_exists(full_filepath):
            raise NoSnapshotFound("There are no saved snapshots.")

        with shelve.open(filepath) as data:
            self.storage = data["snapshot"]
