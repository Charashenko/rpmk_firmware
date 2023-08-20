from machine import Pin
import neopixel
import time


class Led:
    instance = None

    @classmethod
    def get_instance(cls):
        if not cls.instance:
            cls.instance = Led()
        return cls.instance

    def __init__(self):
        self.pin = Pin(16, Pin.OUT)
        self.pixel = neopixel.NeoPixel(
            self.pin,
            1,
        )

    def rgb(self, r: int = 0, g: int = 0, b: int = 0):
        self.pixel[0] = (r, g, b)
        self.__write()

    def on(self):
        self.pixel[0] = (5, 5, 5)
        self.__write()

    def off(self):
        self.pixel[0] = (0, 0, 0)
        self.__write()

    def indicate_start(self):
        count = 3
        self.blink(count, color=(0, 0, 5))

    def blink(self, count, color=(0, 5, 0), delay=0.05):
        for i in range(count):
            self.pixel[0] = color
            self.__write()
            time.sleep(delay)
            self.off()
            time.sleep(delay)

    def __write(self):
        self.pixel.write()
