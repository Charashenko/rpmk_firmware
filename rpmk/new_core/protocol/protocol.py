import time
from ...utils.log import Logger
from machine import Pin
import uasyncio

log = Logger(__name__)

SEND_DELAY_US = 1200
PULSE_LENGTH_US = 50
PULSE_SPACING_US = 50
PULSES_ONE = 2
PULSES_ZERO = 1
PULSES_START = 3
PULSES_STOP = 4


class Protocol:
    def __init__(
        self,
        clock_pin: int,
        data_pin: int,
        is_main: bool,
        num_of_rows: int,
        num_of_cols: int,
    ):
        self.is_main = is_main
        self.nr = num_of_rows
        self.nc = num_of_cols
        self.bits = 0
        self._init_pins(clock_pin, data_pin)
        self.last_state = 0

    def _init_pins(self, c, d):
        if self.is_main:
            self.c = Pin(c, Pin.IN, Pin.PULL_DOWN)
            self.d = Pin(d, Pin.IN, Pin.PULL_DOWN)
        else:
            self.c = Pin(c, Pin.OUT)
            self.d = Pin(d, Pin.OUT)

    def send_data(self, data):
        bits = 0
        for r in range(self.nr):
            for c in range(self.nc):
                if f"{r}:{c}" in data:
                    bits <<= 1
                    bits += 1
                else:
                    bits <<= 1
        self._send_bits(self._format_bin(bits))

    async def recieve_data(self):
        while True:
            while self._pulse_counter() != PULSES_START:
                await uasyncio.sleep(0)
            self.bits = 0
            while True:
                pulse_count = self._pulse_counter()
                if pulse_count == PULSES_ZERO:
                    self.bits <<= 1
                elif pulse_count == PULSES_ONE:
                    self.bits <<= 1
                    self.bits += 1
                elif pulse_count == PULSES_STOP:
                    break
            # log.d(f"Recieved bits: {self._format_bin(self.bits)} {self.bits}")
            await uasyncio.sleep(0)

    def _send_bits(self, bits):
        self._start_transaction()
        for bit in bits:
            if bit == "1":
                self._send_one()
            else:
                self._send_zero()
        self._stop_transaction()

    def _gen_pulses(self, num):
        self.c.on()
        for i in range(num):
            time.sleep_us(SEND_DELAY_US)
            self.d.on()
            time.sleep_us(PULSE_LENGTH_US)
            self.d.off()
        time.sleep_us(PULSE_LENGTH_US)
        self.c.off()
        time.sleep_us(PULSE_SPACING_US)

    def _pulse_counter(self):
        last_state = False
        pulse_count = 0
        while True:
            cv = self.c.value()
            if not cv:
                break
            dv = self.d.value()
            if not last_state and dv:
                pulse_count += 1
            last_state = dv
        return pulse_count

    def _start_transaction(self):
        self._gen_pulses(PULSES_START)

    def _stop_transaction(self):
        self._gen_pulses(PULSES_STOP)

    def _send_one(self):
        self._gen_pulses(PULSES_ONE)

    def _send_zero(self):
        self._gen_pulses(PULSES_ZERO)

    def _format_bin(self, num: int, fixed: int = 0):
        fixed = "{" + f"0:0{fixed}b" + "}"
        return fixed.format(num)
