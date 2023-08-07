from .keycodes import *
from .event import Event
from .event_handler import *

class Key:
    def __init__(self, value: int = KC_NO, chained_key: object = None):
        self.value = value
        self.chained_key = chained_key
        if self.count_keys() > 5:
            raise RuntimeWarning("Reached maximum of chained keys")

    def __str__(self):
        return (
            str(self.value) + (f" {self.chained_key}")
            if self.chained_key is not None
            else ""
        )

    def __eq__(self, o):
        if isinstance(o, Key):
            return self.value == o.value and self.chained_key == o.chained_key
        return False

    def count_keys(self, count: int = 1):
        if self.chained_key is not None:
            return self.chained_key.count_keys(count=count + 1)
        else:
            return count