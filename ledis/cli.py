from typing import Any

from ledis import Ledis
from ledis.exceptions import InvalidUsage


class CLI:
    __slots__ = {"ledis", "commands"}

    def __init__(self):
        self.ledis = Ledis()
        self.commands = {
            "set": self.ledis.set,
            "get": self.ledis.get,
            "sadd": self.ledis.sadd,
            "srem": self.ledis.srem,
            "smembers": self.ledis.smembers,
            "sinter": self.ledis.sinter,
            "keys": self.ledis.keys,
            "del": self.ledis.delete,
            "expire": self.ledis.expire,
            "ttl": self.ledis.ttl,
            "save": self.ledis.save,
            "restore": self.ledis.restore,
        }

    def call(self, query: str) -> Any:
        if " " in query:
            command, data = query.split(" ", 1)
            data = data.split()
        else:
            command = query
            data = []

        if command.lower() not in self.commands:
            allowed_commands = ", ".join(key.upper() for key in self.commands)
            raise InvalidUsage(
                f"Command '{command}' is invalid. "
                f"Allowed commands are {allowed_commands}."
            )

        try:
            return self.commands[command.lower()](*data)
        except TypeError:
            raise InvalidUsage("Invalid command format")
