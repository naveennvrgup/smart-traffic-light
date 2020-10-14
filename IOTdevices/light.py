import json
import traceback
from _datetime import datetime

from maps.models import *
from .actions import *
from .logger import logger
from .repeater import RepeatedTimer


class Light:
    def __init__(self, db_obj, signal_obj):
        self.db_obj = db_obj
        self.signal_obj = signal_obj
        self.control_list = None
        self.timer = None
        self.prev_control_index = None
        self.update_interval = 5

        # subscribe to the STS topics
        subscription_path = subscriber.subscription_path(PROJECT_ID, self.db_obj.getSubscriptionID())
        self.streaming_pull_future = subscriber.subscribe(subscription_path, callback=self.on_msg_handler)
        self.streaming_pull_future.result()

        self.log("spawned")

    def on_msg_handler(self, msg):
        msg.ack()

        try:
            msg = json.loads(msg.data)
            if msg['recipient'] in ['all', self.db_obj.getSubscriptionID()]:
                if msg['action_type'] == SPAWN:
                    self.on_spawn_handler(msg['payload'])
        except Exception as err:
            self.log('exception')
            self.log(traceback.print_exc(err))
            self.log(msg)

    def get_control_index(self):
        minutes_passed = (datetime.now() - self.timer).seconds // self.update_interval
        control_len = len(self.control_list)
        control_index = minutes_passed % control_len
        return control_index

    def update_light(self):
        curr_control_index = self.get_control_index()

        if curr_control_index == self.prev_control_index:
            return

        self.prev_control_index = curr_control_index
        curr_control = self.control_list[curr_control_index]
        curr_signal_state = SignalState.RED \
            if self.db_obj.id in curr_control['green'] \
            else SignalState.GREEN
        self.log(curr_signal_state)
        self.db_obj.signalState = curr_signal_state
        self.db_obj.save()

    def on_spawn_handler(self, payload):
        self.log(payload)

        self.timer = datetime.strptime(payload['timer'], "%H:%M:%S.%f")
        self.control_list = payload['controlList']

        RepeatedTimer(1, self.update_light)

    def log(self, msg):
        logger.debug(f"{self.db_obj.getSubscriptionID()} --- {msg}")

    @staticmethod
    def lightSpawner(db_obj, signal_obj):
        Light(db_obj, signal_obj)
