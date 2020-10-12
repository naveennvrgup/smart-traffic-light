# ---------------------------------------------------------------------------- #
#                                    logging                                   #
# ---------------------------------------------------------------------------- #

import colorlog
import logging

handler = colorlog.StreamHandler()
handler.setFormatter(colorlog.ColoredFormatter(
    fmt='%(log_color)s %(asctime)s : %(message)s',
    datefmt='%m-%d %H:%M:%S'
    ))

logger = colorlog.getLogger('example')
logger.setLevel('DEBUG')
logger.addHandler(handler)


# ---------------------------------------------------------------------------- #
#                                 Smart Devices                                #
# ---------------------------------------------------------------------------- #

from IOTdevices.light import Light
from IOTdevices.signal import Signal
from collections import defaultdict


lights=defaultdict(Light)
signals=defaultdict(Signal)


# ---------------------------------------------------------------------------- #
#                                start emulation                               #
# ---------------------------------------------------------------------------- #

from maps.models import *
import threading

logger.debug(f"Started emulator provisioning")


def run():
    for signal in TrafficSignal.objects.all():
        threading.Thread(target=Signal.signalSpawner, args=(signal,signals,logger)).start()
        firstOne=True
        
        for light in signal.trafficlight_set.all():
            if firstOne:
                firstOne=False
                threading.Thread(target=Light.lightSpawner, args=(light,lights,logger,signals[signal.id])).start()
            else:
                threading.Thread(target=Light.lightSpawner, args=(light,lights,logger)).start()


logger.debug(f"Finished emulator Provisioning:")
logger.debug(f"Signals({len(signals)})")
logger.debug(f"Lights({len(lights)})")