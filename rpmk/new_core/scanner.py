import time
from .scan_mode import *
from ..utils.log import Logger

log = Logger(__name__)


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
                    row.on()
                    for col in self.cols:
                        if col.value():
                            self.engine.on_detect(r, c)
                        c = c + 1
                    row.off()
                    r = r + 1
                    c = 0
            elif self.scan_mode is COL2ROW:
                for col in self.cols:
                    col.on()
                    for row in self.rows:
                        if row.value():
                            self.engine.on_detect(r, c)
                        r = r + 1
                    col.off()
                    c = c + 1
                    r = 0
            await self.engine.on_scan_round_end()
