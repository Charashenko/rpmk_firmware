from .km_parser import KeymapParser
from ..utils.log import Logger
import asyncio

log = Logger(__name__)


class Engine:
    def __init__(self, is_main, protocol):
        # self.kb = Keyboard(usb_hid.devices)
        self.is_main = is_main
        self.protocol = protocol
        self.km = KeymapParser()
        self.active_layer = 0
        self.pressed_keys = []
        self.scan_round = []

    def on_detect(self, r, c):
        self.scan_round.append(f"{r}:{c}")

    async def on_scan_round_end(self):
        self.to_manage = []

        for rc in self.pressed_keys:
            if rc not in self.scan_round:
                self.to_manage.append(f"{rc}:0")
                self.pressed_keys.remove(rc)
                log.d(f"Released {rc}:0")

        for rc in self.scan_round:
            if rc not in self.pressed_keys:
                self.to_manage.append(f"{rc}:1")
                self.pressed_keys.append(rc)
                log.d(f"Pressed {rc}:1")

        if not self.is_main:
            self.protocol.send_data(self.to_manage)

        self.scan_round.clear()
        await asyncio.sleep(0)
