import neopixel
import time
import machine

p = machine.Pin(16, machine.Pin.OUT)
n = neopixel.NeoPixel(p, 1)
for i in range(0, 5):
    n[0] = (0, 5, 0)
    n.write()
    time.sleep(0.1)
    n[0] = (0, 0, 0)
    n.write()
    time.sleep(0.1)
