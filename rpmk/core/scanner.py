import time
from .scan_mode import *
import digitalio
from .executor import Executor
from ..utils.log import Logger


class Scanner:
    def __init__(
        self,
        row_pins: list,
        col_pins: list,
        scan_mode: ScanMode,
        keymap: list,
        side_pin: int,
    ):
        self._row_pins = row_pins
        self._col_pins = col_pins
        self._rows = []
        self._cols = []
        self._scan_mode = scan_mode
        self._executor = Executor(keymap=keymap)
        self.__side_pin = side_pin
        self.init_pins()

    def init_pins(self):
        side_pin = digitalio.DigitalInOut(self.__side_pin)
        side_pin.direction = digitalio.Direction.INPUT
        side_pin.pull = digitalio.Pull.DOWN
        Logger(__name__).d(f"Side pin {side_pin.value}")
        for row_pin in self._row_pins:
            pin = digitalio.DigitalInOut(row_pin)
            if self._scan_mode is ROW2COL:
                pin.direction = digitalio.Direction.OUTPUT
            elif self._scan_mode is COL2ROW:
                pin.direction = digitalio.Direction.INPUT
                pin.pull = digitalio.Pull.DOWN
            self._rows.append(pin)
        for col_pin in self._col_pins:
            pin = digitalio.DigitalInOut(col_pin)
            if self._scan_mode is ROW2COL:
                pin.direction = digitalio.Direction.INPUT
                pin.pull = digitalio.Pull.DOWN
            elif self._scan_mode is COL2ROW:
                pin.direction = digitalio.Direction.OUTPUT
            self._cols.append(pin)

    def start_scan(self):
        while True:
            time.sleep(0.01)
            # print("scan")
            c = 0
            r = 0
            if self._scan_mode is ROW2COL:
                for row in self._rows:
                    row.value = True
                    for col in self._cols:
                        if col.value:
                            self._executor.on_detect(r, c)
                        c = c + 1
                    row.value = False
                    r = r + 1
                    c = 0
            elif self._scan_mode is COL2ROW:
                for col in self._cols:
                    col.value = True
                    for row in self._rows:
                        if row.value:
                            self._executor.on_detect(r, c)
                        r = r + 1
                    col.value = False
                    c = c + 1
                    r = 0
            self._executor.on_scan_round_end()
