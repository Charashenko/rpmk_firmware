from .scanner import Scanner
from ..utils.log import Logger


class Keyboard:
    def __init__(
        self,
        row_pins: list,
        col_pins: list,
        scan_mode: list,
        keymap: list,
        side_pin: int,
    ):
        self.__row_pins = row_pins
        self.__col_pins = col_pins
        self.__scan_mode = scan_mode
        self.__km = keymap
        self.__logger = Logger(__name__)
        self.__side_pin = side_pin

    def run(self):
        self.__scanner = Scanner(
            self.__row_pins,
            self.__col_pins,
            self.__scan_mode,
            self.__km,
            self.__side_pin,
        )
        self.__logger.d("Starting scan")
        self.__scanner.start_scan()
