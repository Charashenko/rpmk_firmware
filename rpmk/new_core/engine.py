from .km_parser import KeymapParser
from ..utils.log import Logger
import uasyncio
from .keyboard import Keyboard

log = Logger(__name__)


class Engine:
    def __init__(self, is_main, protocol):
        self.kb = Keyboard()
        self.is_main = is_main
        self.protocol = protocol
        self.km = KeymapParser()
        self.active_layer = 0
        self.pressed_keys = []
        self.scan_round = []

    def on_detect(self, r, c):
        self.scan_round.append(f"{r}:{c}")

    async def on_scan_round_end(self):
        self.to_release = []
        self.to_press = []

        if not self.is_main:
            self.protocol.send_data(self.scan_round)

        else:
            nc = self.protocol.nc
            nr = self.protocol.nr
            bits = self.protocol._format_bin(self.protocol.bits, fixed=nr * nc)
            ridx = 0
            cidx = 0

            for bit in reversed(bits):
                if bit == "1":
                    self.scan_round.append(f"{nr - ridx - 1}:{cidx + nc}")
                cidx += 1
                if cidx == nc:
                    ridx += 1
                    cidx = 0

            for rc in self.pressed_keys:
                if rc not in self.scan_round:
                    self.to_release.append(f"{rc}")
                    self.pressed_keys.remove(rc)
                    r = rc.split(":")[0]
                    c = rc.split(":")[1]
                    key = self.km.get_key(self.active_layer, int(r), int(c))
                    self.kb.release(key.value)
                    log.d(f"Released {key}")

            for rc in self.scan_round:
                if rc not in self.pressed_keys:
                    self.to_press.append(f"{rc}")
                    self.pressed_keys.append(rc)
                    r = rc.split(":")[0]
                    c = rc.split(":")[1]
                    key = self.km.get_key(self.active_layer, int(r), int(c))
                    self.kb.press(key.value)
                    log.d(f"Pressed {key}")

        self.scan_round.clear()
        await uasyncio.sleep(0)
