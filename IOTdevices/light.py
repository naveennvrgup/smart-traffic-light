from google.cloud import pubsub_v1
from server.settings import PROJECT_ID, subscriber, publisher
from IOTdevices.actions import *
import json
from datetime import datetime
from maps.models import *


class Light:
    def __init__(self, dbObj, lights, logger, signal=None):
        lights[dbObj.id]=self

        self.dbObj=dbObj
        self.logger=logger
        self.signal=signal
        self.log("spwaned")

        # subscribe to the STS topics
        subscription_path = subscriber.subscription_path(PROJECT_ID, self.dbObj.getSubscriptionID())
        self.streaming_pull_future = subscriber.subscribe(subscription_path, callback=self.onMsgHandler)
        self.streaming_pull_future.result()



    def onMsgHandler(self, msg):
        msg.ack()

        try:
            msg=json.loads(msg.data)
            if msg['recipient'] in ['all',self.dbObj.getSubscriptionID()]:
                if msg['actionType']==SPAWN:
                    self.onSpwanHandler(msg['payload'])
        except Exception as err:
            self.log(err)
            self.log(msg)
    

    def onSpwanHandler(self, payload):
        self.timer=datetime.strptime(payload['timer'], "%H:%M:%S.%f")
        self.controlList=payload['controlList']
        self.controlLen=len(self.controlList)
        
        minsPassed=(datetime.now() - self.timer).seconds//60
        self.controlIndex=minsPassed%self.controlLen

        self.log(self.controlList[self.controlIndex])
        if self.dbObj.id in self.controlList[self.controlIndex]['green']:
            self.dbObj.signalState = SignalState.RED
        else:
            self.dbObj.signalState = SignalState.GREEN
        self.dbObj.save()


    def log(self,msg):
        self.logger.debug(f"{self.dbObj.getSubscriptionID()} => {msg}")


    @staticmethod
    def lightSpawner(*args):
        obj = Light(*args)
