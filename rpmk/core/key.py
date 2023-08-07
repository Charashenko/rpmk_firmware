from .keycodes import *


class Key:
    def __init__(self, value: int = KC_NO, chained_key: object = None):
        self.value = value
        self.__chained_key = chained_key
        self.__no_next_keys = (
            1 + chained_key.__no_next_keys if chained_key != None else 0
        )
        if self.__no_next_keys > 5:
            raise Exception("Reached maximum of chained keys")

    def __str__(self):
        return (
            str(self.value) + (f" {self.__chained_key}")
            if self.__chained_key is not None
            else ""
        )

    def __eq__(self, o):
        if isinstance(o, Key):
            return (
                self.value == o.value
                and self.__chained_key == o.__chained_key
                and self.__no_next_keys == o.__no_next_keys
            )
        return False

    def exec(
        self,
        active_layers: list,
        is_release: bool,
        pressed_keys: list,
        prepared_keys: list,
    ):
        prepared_keys.append(self.value)
        if self.__chained_key is not None:
            self.__chained_key.exec(
                active_layers=active_layers,
                is_release=is_release,
                pressed_keys=pressed_keys,
                prepared_keys=prepared_keys,
            )

    def count_keys(self, count: int = 1):
        if self.__chained_key is not None:
            return self.__chained_key.count_keys(count=count + 1)
        else:
            return count
