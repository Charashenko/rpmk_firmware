from digitalio import DigitalInOut, Direction, Pull
import time
from ..utils.log import Logger

log = Logger(__name__)


class Protocol:
    def __init__(
        self,
        clock_pin: int,
        data_pin: int,
        is_main: bool,
    ):
        self.is_main = is_main
        self.init_pins(clock_pin, data_pin)

    def init_pins(self, clock_pin, data_pin):
        if self.is_main:
            self.clock_pin = DigitalInOut(clock_pin)
            self.clock_pin.direction = Direction.OUTPUT
            self.data_pin = DigitalInOut(data_pin)
            self.data_pin.direction = Direction.INPUT
            self.data_pin.pull = Pull.DOWN
        else:
            self.data_pin = DigitalInOut(data_pin)
            self.data_pin.direction = Direction.OUTPUT
            self.clock_pin = DigitalInOut(clock_pin)
            self.clock_pin.direction = Direction.INPUT
            self.clock_pin.pull = Pull.DOWN

    def negotiate(self):
        if self.is_main:
            log.d("Setting clock, waiting data")
            self.clock_pin.value = True
            while not self.data_pin.value:
                time.sleep(0.01)
            log.d("Data received")
        else:
            log.d("Waiting clock")
            while not self.clock_pin.value:
                time.sleep(0.01)
            log.d("Clock received, setting data")
            self.data_pin.value = True
