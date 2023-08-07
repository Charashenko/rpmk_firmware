import board
import neopixel


class Led:
    instance = None

    @classmethod
    def get_instance(cls):
        if not cls.instance:
            cls.instance = Led()
        return cls.instance

    def __init__(self):
        self.pin = board.NEOPIXEL
        self.pixel = neopixel.NeoPixel(
            self.pin,
            1,
            brightness=0.3,
            auto_write=False,
        )

    def rgb(self, r: int = 0, g: int = 0, b: int = 0):
        self.pixel[0] = (r, g, b)
        self.__write()

    def on(self):
        self.pixel[0] = (10, 10, 10)
        self.__write()

    def off(self):
        self.pixel[0] = (0, 0, 0)
        self.__write()

    def __write(self):
        self.pixel.show()