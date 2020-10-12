from server.settings import PROJECT_ID, subscriber, publisher
import json
import time
from IOTdevices.actions import *


class Signal:
    def __init__(self, dbObj, signals, logger):
        self.dbObj=dbObj
        self.logger=logger
        signals[dbObj.id]=self
       
        self.log("spwaned")
        self.startSpawnSequence()


    def startSpawnSequence(self):
        time.sleep(2)
        self.sendMsgHandler(SPAWN, 'all',{
            'timer': str(self.dbObj.timer),
            'controlList': self.dbObj.controlList
        })


    def sendMsgHandler(self, actionType, recipient, payload):
        topic_path = publisher.topic_path(PROJECT_ID, self.dbObj.getTopicID())

        msg={
            'actionType':actionType,
            'recipient': recipient,
            'payload': payload 
        }

        msg=json.dumps(msg)
        msg = msg.encode("utf-8")
        publisher.publish(topic_path, msg)


    def log(self,msg):
        self.logger.debug(f"{self.dbObj.getTopicID()} >>> {msg}")

    
    @staticmethod
    def signalSpawner(*args):
        obj = Signal(*args)
