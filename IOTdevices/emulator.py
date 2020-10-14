import threading
from collections import defaultdict

import colorlog

from IOTdevices.light import Light
from IOTdevices.signal import Signal
from maps.models import *

# logging setup

handler = colorlog.StreamHandler()
handler.setFormatter(colorlog.ColoredFormatter(
    fmt='%(log_color)s %(asctime)s : %(message)s',
    datefmt='%m-%d %H:%M:%S'
))

logger = colorlog.getLogger('example')
logger.setLevel('DEBUG')
logger.addHandler(handler)

# smart devices

lights = defaultdict(Light)
signals = defaultdict(Signal)


# emulator main

def run():
    logger.debug(f"Started emulator provisioning")

    for signal in TrafficSignal.objects.all()[:1]:
        threading.Thread(target=Signal.signalSpawner, args=(signal, signals, logger)).start()
        first_one = True

        for light in signal.trafficlight_set.all():
            if first_one:
                first_one = False
                threading.Thread(target=Light.lightSpawner, args=(light, lights, logger, signals[signal.id])).start()
            else:
                threading.Thread(target=Light.lightSpawner, args=(light, lights, logger)).start()

    logger.debug(f"Finished emulator Provisioning:")
    logger.debug(f"Signals({len(signals)})")
    logger.debug(f"Lights({len(lights)})")
