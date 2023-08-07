class PressedFunction:
    def __init__(self, function, layer: int, row: int, col: int):
        self.function = function
        self.layer = layer
        self.row = row
        self.col = col

    def __str__(self):
        return str(self.function)

    def __eq__(self, o):
        if isinstance(o, PressedFunction):
            return self.row == o.row and self.col == o.col
        return False
