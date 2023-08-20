import micropython
import machine


class PDU:
    def __init__(self, size):
        self.bit_idx = 0
        self.data = [0 for i in range(2**size - 1)]
        self.size = size
        self.unit_idx = 0

    # @micropython.native
    def add(self, bit):
        if self.unit_idx >= self.size:
            self.reset()
        if not self.bit_idx < self.size:
            self.unit_idx += 1
            self.bit_idx = 0
        self.data[self.unit_idx] <<= 1
        if bit:
            self.data[self.unit_idx] += 1
        self.bit_idx += 1

    def len(self):
        return self.unit_idx * self.size + self.bit_idx + 1

    def reset(self):
        machine.disable_irq()
        for d in self.data:
            d = 0
        self.bit_idx = 0
        self.unit_idx = 0
        machine.enable_irq()

    def __str__(self):
        st = ""
        for i in range(len(self.data)):
            st += "{0:04b} ".format(self.data[i])
        return st
