import traceback
from _datetime import datetime

import requests
from pytz import timezone

from maps.models import *
from .actions import *
from .logger import logger
from .repeater import RepeatedTimer


class Light:
    def __init__(self, TLID):
        self.TLID = TLID
        self.prev_control_index = -1

        self.on_spawn_handler()
        self.log("spawned")

    def on_msg_handler(self, msg):
        msg.ack()

        try:
            msg = json.loads(msg.data)
            if msg[RECIPIENT] in ['all', self.db_obj.getSubscriptionID()]:
                if msg[ACTION_TYPE] == OVER_RIDE:
                    self.on_over_ride_handler(msg[PAYLOAD])
                elif msg[ACTION_TYPE] == NORMAL_RIDE:
                    self.on_normal_ride_handler(msg[PAYLOAD])
        except Exception as err:
            self.log('exception')
            self.log(traceback.print_exc(err))
            self.log(msg)

    def get_control_index(self):
        timezone_india = timezone('Asia/Calcutta')
        curr_time = datetime.now(timezone_india)

        slots_passed = (curr_time - self.timer).seconds // RESET_INTERVAL

        control_len = len(self.control_list)
        control_index = slots_passed % control_len
        return control_index

    def update_light(self):
        if self.mode == OperationMode.OVERRIDE:
            return

        curr_control_index = self.control_list
        if curr_control_index == self.prev_control_index:
            return

        self.prev_control_index = curr_control_index
        curr_control = self.control_list[curr_control_index]
        curr_signal_state = SignalState.RED \
            if self.TLID in curr_control['green'] \
            else SignalState.GREEN
        # self.log(curr_signal_state)
        self.sig = curr_signal_state
        self.db_obj.save()

    def on_over_ride_handler(self, payload):
        self.db_obj.operationMode = OperationMode.OVERRIDE
        self.db_obj.signalState = payload[OPERATION_COLOR]
        self.db_obj.save()
        # log
        self.log(OperationMode.OVERRIDE + " " + payload[OPERATION_COLOR])

    def on_normal_ride_handler(self, payload):
        self.db_obj.operationMode = OperationMode.NORMAL
        self.db_obj.save()
        # update
        self.update_light()
        # log
        self.log(OperationMode.NORMAL)

    def on_spawn_handler(self):
        data = requests.get(f"http://127.0.0.1:8000/maps/syncLight/{self.TLID}/").json()

        syncTime = data['syncTime']
        self.timer = datetime.fromisoformat(syncTime[:syncTime.rfind('.')])
        self.control_list = data['controlList']
        self.mode = data['mode']
        self.resetInterval = data['resetInterval']
        self.subscription_id = data['subcription_id']
        self.project_id = data['project_id']

        # subscribe to the STS topics
        subscription_path = subscriber.subscription_path(PROJECT_ID, self.subscription_id)
        self.streaming_pull_future = subscriber.subscribe(subscription_path, callback=self.on_msg_handler)
        self.streaming_pull_future.result()

        RepeatedTimer(1, self.update_light)

    def log(self, msg):
        logger.debug(f"{self.subscription_id} --- {msg}")

    @staticmethod
    def lightSpawner(TLID):
        Light(TLID)
