import time
from ..utils.log import Logger
from machine import Pin
import asyncio

log = Logger(__name__)

PULSES_START = 3
PULSES_STOP = 4
PULSES_ONE = 2
PULSES_ZERO = 1
PULSE_DELAY = 0.001


class Protocol:
    def __init__(
        self,
        clock_pin: int,
        data_pin: int,
        is_main: bool,
    ):
        self.is_main = is_main
        self.init_pins(clock_pin, data_pin)

    def init_pins(self, c, d):
        if self.is_main:
            self.c = Pin(c, Pin.IN, Pin.PULL_DOWN)
            self.d = Pin(d, Pin.IN, Pin.PULL_DOWN)
        else:
            self.c = Pin(c, Pin.OUT)
            self.d = Pin(d, Pin.OUT)

    async def recieve_data(self):
        row = None
        col = None
        state = None
        recieving_row = True
        recieving_col = False
        recieving_state = False
        while True:
            while self._pulse_counter() != PULSES_START:
                await asyncio.sleep(0)
            bits = ""
            while True:
                count = self._pulse_counter()
                if count == PULSES_ZERO:
                    bits += "0"
                elif count == PULSES_ONE:
                    bits += "1"
                elif count == PULSES_STOP:
                    break
            if recieving_row:
                row = int(bits, 2)
                recieving_row = False
                recieving_col = True
            elif recieving_col:
                col = int(bits, 2)
                recieving_col = False
                recieving_state = True
            elif recieving_state:
                state = int(bits, 2)
                print(f"Recieved: {row}:{col} {bool(state)}")
                recieving_state = False
                recieving_row = True
                row = None
                col = None
                state = None
            await asyncio.sleep(0)

    def send_data(self, data):
        for rcs in data:
            split = rcs.split(":")
            r = split[0]
            c = split[1]
            s = split[2]
            self._send_bits(self._format_bin(int(r)))
            self._send_bits(self._format_bin(int(c)))
            self._send_bits(self._format_bin(int(s)))

    def _pulse_counter(self):
        last_state = False
        pulse_count = 0
        while True:
            cv = self.c.value()
            dv = self.d.value()
            if not last_state and dv:
                pulse_count += 1
            last_state = dv
            if not cv:
                break
        return pulse_count

    def _send_bits(self, bits):
        self._start_transmission()
        for bit in bits:
            if bit == "1":
                self._send_one()
            else:
                self._send_zero()
        self._stop_transmission()

    def _format_bin(self, num):
        return "{0:b}".format(num)

    def _start_transmission(self):
        self._gen_pulses(PULSES_START)

    def _stop_transmission(self):
        self._gen_pulses(PULSES_STOP)

    def _send_one(self):
        self._gen_pulses(PULSES_ONE)

    def _send_zero(self):
        self._gen_pulses(PULSES_ZERO)

    def _gen_pulses(self, count):
        self.c.value(1)
        for i in range(0, count):
            time.sleep(PULSE_DELAY)
            self.d.value(1)
            time.sleep(PULSE_DELAY)
            self.d.value(0)
        self.c.value(0)
