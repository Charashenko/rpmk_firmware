from rpmk.utils.led import Led
from rpmk.utils.log import Logger

log = Logger(__name__)
led = Led.get_instance()

for i in range(0, 5):
    led.on()
    time.sleep(0.1)
    led.off()
    time.sleep(0.1)
