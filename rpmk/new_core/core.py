from ..utils.log import Logger
from ..utils.led import Led
from .scan_mode import *
from .protocol import Protocol
from .scanner import Scanner
from .engine import Engine
import time

from machine import Pin
import asyncio

log = Logger(__name__)
led = Led.get_instance()


class Core:
    def __init__(
        self,
        left_side_pin: int,
        clock_pin: int,
        data_pin: int,
        col_pins: list[int],
        row_pins: list[int],
        scan_mode: int,
    ):
        self.left_side_pin = left_side_pin
        self.clock_pin = clock_pin
        self.data_pin = data_pin
        self.col_pins = col_pins
        self.row_pins = row_pins
        self.scan_mode = scan_mode

        self.init_session()

    def init_session(self):
        led.on()
        log.d("Running init")

        rows, cols = self.init_pins()
        self.get_is_left_half()
        self.get_is_usb_conn()
        self.protocol = Protocol(self.clock_pin, self.data_pin, self.is_main)
        self.engine = Engine(self.is_main, self.protocol)
        self.scanner = Scanner(rows, cols, self.scan_mode, self.engine)

        log.d("Init done")
        led.off()

    def init_pins(self) -> (list[Pin], list[Pin]):
        rows = []
        cols = []
        for row_pin in self.row_pins:
            if self.scan_mode is ROW2COL:
                pin = Pin(row_pin, Pin.OUT)
            elif self.scan_mode is COL2ROW:
                pin = Pin(row_pin, Pin.IN, Pin.PULL_DOWN)
            rows.append(pin)
        for col_pin in self.col_pins:
            if self.scan_mode is ROW2COL:
                pin = Pin(col_pin, Pin.IN, Pin.PULL_DOWN)
            elif self.scan_mode is COL2ROW:
                pin = Pin(col_pin, Pin.OUT)
            cols.append(pin)

        return (rows, cols)

    def get_is_left_half(self):
        self.is_left = Pin(self.left_side_pin, Pin.IN, Pin.PULL_DOWN).value()
        log.d("Board is left") if self.is_left else log.d("Board is right")

    def get_is_usb_conn(self):
        try:
            self.is_main = self.is_left
            log.d("Board is main")
        except Exception as e:
            if str(e) == "USB busy":
                log.d("Board is not main")
            else:
                log.e(str(e))
                raise RuntimeError(str(e))

    async def start(self):
        log.d("Starting")
        scanner_task = asyncio.create_task(self.scanner.start_scan())
        protocol_task = asyncio.create_task(self.protocol.recieve_data())
        await asyncio.gather(scanner_task, protocol_task)
