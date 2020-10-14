import json
import time

from .logger import logger
from .light import Light
import threading

class Signal:
    def __init__(self, db_obj):
        self.db_obj = db_obj
        self.log("spawned")
        # self.startSpawnSequence()

    # def startSpawnSequence(self):
    #     time.sleep(2)
    #     self.sendMsgHandler(SPAWN, 'all', {
    #         'timer': str(self.db_obj.timer),
    #         'controlList': self.db_obj.controlList
    #     })

    # def sendMsgHandler(self, action_type, recipient, payload):
    #     topic_path = publisher.topic_path(PROJECT_ID, self.db_obj.getTopicID())
    #
    #     msg = {
    #         'action_type': action_type,
    #         'recipient': recipient,
    #         'payload': payload
    #     }
    #
    #     msg = json.dumps(msg)
    #     msg = msg.encode("utf-8")
    #     publisher.publish(topic_path, msg)

    def log(self, msg):
        logger.debug(f"{self.db_obj.getTopicID()} >>> {msg}")

    @staticmethod
    def signalSpawner(db_obj):
        signal = Signal(db_obj)
        lights = db_obj.trafficlight_set.all()

        for light_obj in lights:
            threading.Thread(target=Light.lightSpawner, args=(light_obj, db_obj)).start()