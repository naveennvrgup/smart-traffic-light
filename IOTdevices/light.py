from google.cloud import pubsub_v1
from server.settings import PROJECT_ID, subscriber, publisher
from IOTdevices.actions import *
import json


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
            self.log(msg)
            if msg['recipient'] in ['all',self.dbObj.getSubscriptionID()]:
                if msg['actionType']==SPAWN:
                    self.onSpwanHandler(msg['payload'])
        except:
            self.log(msg.data)
    

    def onSpwanHandler(self, payload):
        self.log(payload)


    def log(self,msg):
        self.logger.debug(f"{self.dbObj.getSubscriptionID()} => {msg}")


    @staticmethod
    def lightSpawner(*args):
        obj = Light(*args)
