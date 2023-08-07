from rpmk.utils.led import Led
from rpmk.utils.log import Logger
from rpmk.new_core.core import Core
from rpmk.new_core.scan_mode import *

from machine import Pin
import asyncio
import time

log = Logger(__name__)
led = Led.get_instance()


def start():
    for i in range(0, 3):
        led.rgb(0, 5, 0)
        time.sleep(0.05)
        led.off()
        time.sleep(0.05)


c = Core(
    clock_pin=29,
    data_pin=28,
    left_side_pin=27,
    col_pins=[
        0,
        1,
        2,
        3,
        4,
    ],
    row_pins=[
        5,
        6,
        7,
    ],
    scan_mode=COL2ROW,
)

asyncio.run(c.start())
