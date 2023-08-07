from ..utils.log import Logger
from ..utils.led import Led
from adafruit_hid.keyboard import Keyboard
from digitalio import DigitalInOut, Direction, Pull
import usb_hid
from .scan_mode import *
from .protocol import Protocol
from .scanner import Scanner
from .event_handler import *
from .event import Event
from .executor import Executor
import time

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
        self.executor = Executor()

        self.init_session()

    def init_session(self):
        led.on()
        log.d("Running init")

        rows, cols = self.init_pins()
        side_pin = self.init_side_pin()
        self.get_is_left_half(side_pin)
        self.get_is_usb_conn()
        # self.init_comm_protocol(self.clock_pin, self.data_pin)
        self.init_scanner(rows, cols)

        log.d("Init done")
        led.off()

    def init_pins(self) -> (list[DigitalInOut], list[DigitalInOut]):
        rows = []
        cols = []
        for row_pin in self.row_pins:
            pin = DigitalInOut(row_pin)
            if self.scan_mode is ROW2COL:
                pin.direction = Direction.OUTPUT
            elif self.scan_mode is COL2ROW:
                pin.direction = Direction.INPUT
                pin.pull = Pull.DOWN
            rows.append(pin)
        for col_pin in self.col_pins:
            pin = DigitalInOut(col_pin)
            if self.scan_mode is ROW2COL:
                pin.direction = Direction.INPUT
                pin.pull = Pull.DOWN
            elif self.scan_mode is COL2ROW:
                pin.direction = Direction.OUTPUT
            cols.append(pin)

        return (rows, cols)

    def init_side_pin(self) -> DigitalInOut:
        side_pin = DigitalInOut(self.left_side_pin)
        side_pin.direction = Direction.INPUT
        side_pin.pull = Pull.DOWN
        return side_pin

    def get_is_left_half(self, pin: DigitalInOut):
        self.is_left = pin.value
        log.d("Board is left") if self.is_left else log.d("Board is right")

    def get_is_usb_conn(self):
        try:
            kb = Keyboard(usb_hid.devices)
            self.is_main = True
            log.d("Board is main")
        except Exception as e:
            if str(e) == "USB busy":
                log.d("Board is not main")
            else:
                log.e(str(e))
                raise RuntimeError(str(e))

    def init_comm_protocol(self, clock_pin, data_pin):
        self.protocol = Protocol(clock_pin, data_pin, self.is_main)
        self.protocol.negotiate()

    def init_scanner(
        self,
        rows: list[DigitalInOut],
        cols: list[DigitalInOut],
    ):
        self.scanner = Scanner(rows, cols, self.scan_mode)

    def start(self):
        log.d("Starting")
        self.scanner.start_scan()
