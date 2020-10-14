import threading

from maps.models import *
from .logger import logger
from .signal import Signal


def run():
    logger.debug(f"Started emulator provisioning")

    for signal_obj in TrafficSignal.objects.all():
        threading.Thread(target=Signal.signalSpawner, args=(signal_obj,)).start()
