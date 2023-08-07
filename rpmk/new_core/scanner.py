import time
from .scan_mode import *
from ..utils.log import Logger
from ..utils.led import Led

log = Logger(__name__)
led = Led.get_instance()


class Scanner:
    def __init__(
        self,
        rows: list[Pin],
        cols: list[Pin],
        scan_mode: int,
        engine: Engine,
    ):
        self.rows = rows
        self.cols = cols
        self.scan_mode = scan_mode
        self.engine = engine

    async def start_scan(self):
        while True:
            c = 0
            r = 0
            if self.scan_mode is ROW2COL:
                for row in self.rows:
                    row.value(1)
                    for col in self.cols:
                        if col.value():
                            self.engine.on_detect(r, c)
                        c = c + 1
                    row.value(0)
                    r = r + 1
                    c = 0
            elif self.scan_mode is COL2ROW:
                for col in self.cols:
                    col.value(1)
                    for row in self.rows:
                        if row.value():
                            self.engine.on_detect(r, c)
                        r = r + 1
                    col.value(0)
                    c = c + 1
                    r = 0
            await self.engine.on_scan_round_end()
