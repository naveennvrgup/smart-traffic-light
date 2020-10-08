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


from light import Light
from signal import Signal
from collections import defaultdict
lights=defaultdict(Light)
signals=defaultdict(Signal)


if __name__ == "__main__":
    # setup django context
    import sys
    import os
    import django
    from pathlib import Path


    projectDir = str(Path(__file__).parent.parent.absolute())
    sys.path.append(projectDir)

    os.environ['DJANGO_SETTINGS_MODULE'] = 'server.settings'
    os.environ['GOOGLE_APPLICATION_CREDENTIALS']=str(Path(__file__).parent.absolute())+"/serverKey.json"
    django.setup()


    # ---------------------------------------------------------------------------- #
    #                                start emulation                               #
    # ---------------------------------------------------------------------------- #

    from maps.models import *
    import threading

    logger.debug(f"Started emulator provisioning")

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
    
    # from publisher import publishToSignalTopic
    # publishToSignalTopic('asfasdf')
    from subscriber import subscribeToSignal
    subscribeToSignal(1)