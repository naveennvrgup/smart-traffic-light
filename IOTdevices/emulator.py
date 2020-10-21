import threading

from maps.models import *
from .light import Light
from .logger import logger


def run():
    logger.debug(f"Started emulator provisioning")

    for light_obj in TrafficLight.objects.all():
        threading.Thread(target=Light.lightSpawner, args=(light_obj.id,)).start()
