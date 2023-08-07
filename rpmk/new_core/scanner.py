import time
from .scan_mode import *
from ..utils.log import Logger
from .event_handler import *
from .event import Event

log = Logger(__name__)


class Scanner:
    def __init__(
        self,
        rows: list[DigitalInOut],
        cols: list[DigitalInOut],
        scan_mode: int,
    ):
        self.rows = rows
        self.cols = cols
        self.scan_mode = scan_mode

    def start_scan(self):
        while True:
            time.sleep(0.01)
            # print("scan")
            c = 0
            r = 0
            if self.scan_mode is ROW2COL:
                for row in self.rows:
                    row.value = True
                    for col in self.cols:
                        if col.value:
                            self.on_detect(r, c)
                        c = c + 1
                    row.value = False
                    r = r + 1
                    c = 0
            elif self.scan_mode is COL2ROW:
                for col in self.cols:
                    col.value = True
                    for row in self.rows:
                        if row.value:
                            self.on_detect(r, c)
                        r = r + 1
                    col.value = False
                    c = c + 1
                    r = 0
            self.on_scan_round_end()

    def on_detect(self, r: int, c: int):
        post_event(Event(event_type=Event.ON_DETECT, event_data=[r, c]))

    def on_scan_round_end(self):
        post_event(Event(event_type=Event.ON_SCAN_ROUND_END))
