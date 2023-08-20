from rpmk.utils.led import Led
from rpmk.utils.log import Logger
from rpmk.new_core.core import Core
from rpmk.new_core.scan_mode import *
import uasyncio

led = Led.get_instance()
led.indicate_start()

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


uasyncio.run(c.start())
