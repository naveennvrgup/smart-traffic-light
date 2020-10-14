import json

from server.settings import PROJECT_ID, subscriber
from .actions import *
from .logger import logger


class Light:
    def __init__(self, db_obj, signal_obj):
        self.db_obj = db_obj
        self.signal_obj = signal_obj
        self.log("spwaned")

        # subscribe to the STS topics
        subscription_path = subscriber.subscription_path(PROJECT_ID, self.db_obj.getSubscriptionID())
        self.streaming_pull_future = subscriber.subscribe(subscription_path, callback=self.on_msg_handler)
        self.streaming_pull_future.result()

    def on_msg_handler(self, msg):
        msg.ack()

        try:
            msg = json.loads(msg.data)
            if msg['recipient'] in ['all', self.db_obj.getSubscriptionID()]:
                if msg['actionType'] == SPAWN:
                    self.on_spawn_handler(msg['payload'])
        except Exception as err:
            self.log(err)
            self.log(msg)

    def on_spawn_handler(self, payload):
        self.log(payload)

    #     self.timer = datetime.strptime(payload['timer'], "%H:%M:%S.%f")
    #     self.controlList = payload['controlList']
    #     self.controlLen = len(self.controlList)
    #
    #     minsPassed = (datetime.now() - self.timer).seconds // 60
    #     self.controlIndex = minsPassed % self.controlLen
    #
    #     self.log(self.controlList[self.controlIndex])
    #     if self.db_obj.id in self.controlList[self.controlIndex]['green']:
    #         self.db_obj.signalState = SignalState.RED
    #     else:
    #         self.db_obj.signalState = SignalState.GREEN
    #     self.db_obj.save()

    def log(self, msg):
        logger.debug(f"{self.db_obj.getSubscriptionID()} --- {msg}")

    @staticmethod
    def lightSpawner(db_obj, signal_obj):
        Light(db_obj, signal_obj)
