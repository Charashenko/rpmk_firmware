from ..keymap import KEYMAP


class KeymapParser:
    def __init__(self):
        self.km = KEYMAP

    def get_key(self, layer: int, row: int, col: int):
        layer_str = self.km["layers"][layer]
        row_str = self.km[layer_str][row]
        key = self.km[row_str][col]
        return col
