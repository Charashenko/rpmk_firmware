from .event import Event
from .event_handler import *
from adafruit_hid.keyboard import Keyboard
import usb_hid
from .km_parser import KeymapParser
from ..utils.log import Logger

log = Logger(__name__)


@subscribe(Event(event_type=Event.ON_DETECT))
def on_detect(event: Event):
    row = event.data[0]
    col = event.data[1]
    log.d(f"r: {row} c: {col}")
    log.d(f"Key {self.km.get_key(self.active_layer, row, col)}")


@subscribe(Event(event_type=Event.ON_SCAN_ROUND_END))
def on_scan_round_end(event):
    pass


class Executor:
    def __init__(self):
        self.kb = Keyboard(usb_hid.devices)
        self.km = KeymapParser()
        self.active_layer = 0
        self.pressed_keys = []
        self.on_detect = on_detect
        self.on_scan_round_end = on_scan_round_end
