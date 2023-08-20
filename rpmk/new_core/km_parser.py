from ..keymap import KEYMAP
from ..utils.log import Logger

log = Logger(__name__)


class KeymapParser:
    def __init__(self):
        self.km = KEYMAP

    def get_key(self, layer: int, row: int, col: int, right_side: bool = False):
        if right_side:
            layer_str = self.km["layers"][layer]
            row_str = self.km[layer_str][row]
            key = self.km[row_str][-col]
            return key
        layer_str = self.km["layers"][layer]
        row_str = self.km[layer_str][row]
        key = self.km[row_str][col]
        return key
