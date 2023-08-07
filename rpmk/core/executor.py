import usb_hid
from adafruit_hid.keyboard import Keyboard
from .pressed_function import PressedFunction
from .event import *
from ..utils.log import Logger
from .key import Key


class Executor:
    def __init__(self, keymap: list):
        self.__pressed = []
        self.__scan_round = []
        self.__km = keymap
        self.__active_layers = [0]
        self.__active_mods = []
        self.__kb = Keyboard(usb_hid.devices)
        self.__logger = Logger(__name__)
        subscribe(ON_SYS_PRESS, self)
        subscribe(ON_SYS_LAYER, self)

    def on_detect(self, row: int, col: int):
        active_layer = self.__active_layers[-1]
        function = self.__km[active_layer][row][col]
        pressed_function = PressedFunction(function, active_layer, row, col)
        self.__scan_round.append(pressed_function)
        post_event(ON_DETECT, pressed_function)

    def on_scan_round_end(self):
        to_be_released = []
        for function in self.__pressed:
            if function not in self.__scan_round:
                to_be_released.append(function)

        for function in to_be_released:
            self.__pressed.remove(function)

        pressed_keys_count = 0
        for function in self.__pressed:
            pressed_keys_count = pressed_keys_count + function.function.count_keys()

        to_be_pressed = []
        for function in self.__scan_round:
            if function not in self.__pressed:
                if pressed_keys_count + function.function.count_keys() <= 6:
                    to_be_pressed.append(function)
                    pressed_keys_count = (
                        pressed_keys_count + function.function.count_keys()
                    )
                else:
                    self.__logger.d("Dropping extra keys")
                    break

        for function in to_be_pressed:
            self.__pressed.append(function)

        self.__scan_round.clear()

        prepared_for_press = []
        self.prepare(False, to_be_pressed, prepared_for_press)

        prepared_for_release = []
        self.prepare(True, to_be_released, prepared_for_release)

        if len(prepared_for_release) > 0:
            self.send_method(True, prepared_for_release)
        if len(prepared_for_press) > 0:
            self.send_method(False, prepared_for_press)

    def prepare(self, is_release: bool, to_prepare: list, prepared: list):
        for function in to_prepare:
            if isinstance(function, Key):
                function.exec(
                    active_layers=self.__active_layers,
                    is_release=is_release,
                    pressed_keys=self.__pressed,
                    prepared_keys=prepared,
                )
            else:
                function.function.exec(
                    active_layers=self.__active_layers,
                    is_release=is_release,
                    pressed_keys=self.__pressed,
                    prepared_keys=prepared,
                )

    def send_method(
        self, is_release: bool, key_values: list, use_combined_method: bool = False
    ):
        self.__logger.d(
            f"Send method for {key_values}, is release: {is_release}, using combined method: {use_combined_method}"
        )
        if use_combined_method:
            self.__kb.send(*key_values)
            return
        if is_release:
            for value in key_values:
                if value >= 0xE0 and value <= 0xE7:
                    self.__active_mods.remove(value)
            self.__kb.release(*key_values)
        else:
            for value in key_values:
                if value >= 0xE0 and value <= 0xE7:
                    self.__active_mods.append(value)
            self.__kb.press(*key_values)

    def handler(self, event_type, event_data):
        self.__logger.d(
            f'Recieveing event of type "{event_type}" with data "{event_data}"'
        )
        if event_type == ON_SYS_PRESS:
            prepared_for_press = []
            self.prepare(False, event_data, prepared_for_press)
            self.send_method(False, prepared_for_press, use_combined_method=True)
        elif event_type == ON_SYS_LAYER:
            if event_data[0] == "add":
                self.__active_layers.append(event_data[1])
            elif event_data[0] == "remove":
                self.__active_layers.pop()
