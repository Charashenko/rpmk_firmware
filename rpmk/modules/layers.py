from ..core.key import Key
import time
from ..core.event import *
from ..utils.log import Logger


class L_MO:
    def __init__(self, layer: int):
        self.__layer = layer
        self.__logger = Logger(__name__)

    def __eq__(self, o):
        if isinstance(o, L_MO):
            return self.__layer == o.__layer
        return False

    def exec(
        self,
        active_layers: list,
        is_release: bool,
        pressed_keys: list,
        prepared_keys: list,
    ):
        if is_release:
            active_layers.pop()
            self.__logger.d(f"Switched to layer {active_layers[-1]}")
        else:
            active_layers.append(self.__layer)
            self.__logger.d(f"Switched to layer {self.__layer}")

    def count_keys(self, count: int = 0):
        return count


class L_HT:
    def __init__(self, layer: int, key: Key):
        self.__delay = 2000
        self.__start = 0
        self.__layer = layer
        self.__key = key
        self.__logger = Logger(__name__)

    def __eq__(self, o):
        if isinstance(o, L_HT):
            return self.__key == o.__key and self.__layer == o.__layer
        return False

    def exec(
        self,
        active_layers: list,
        is_release: bool,
        pressed_keys: list,
        prepared_keys: list,
    ):
        if is_release:
            unsubscribe(ON_DETECT, self)
            if not self.__check_delay():
                post_event(ON_SYS_PRESS, (self.__key,))
            else:
                post_event(ON_SYS_LAYER, ("remove",))
        else:
            self.__start = time.monotonic_ns()
            subscribe(ON_DETECT, self)

    def __check_delay(self):
        return time.monotonic_ns() - self.__start >= self.__delay * 1000000

    def handler(self, event_type, event_data):
        self.__logger.d(
            f'Recieveing event of type "{event_type}" with data "{event_data}"'
        )
        if event_type is ON_DETECT:
            if self.__check_delay():
                unsubscribe(ON_DETECT, self)
                post_event(ON_SYS_LAYER, ("add", self.__layer))

    def count_keys(self, count: int = 0):
        return count
