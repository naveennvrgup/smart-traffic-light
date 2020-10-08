import threading
import time
import logging
import random


class SmartTrafficLight
    controlList=[]

    def __init__(self, isMaster, lat, lng, direction):
        self.isMaster=isMaster
        self.lat=lat
        self.lng=lng
        self.dir=direction
        self.controlIndex




def thread_function(name):
    logging.info(f"Thread {name} starting")
    time.sleep(random.randint(1,5))
    logging.info(f"Thread {name} finishing")


if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")
    logging.info("Main    : before creating thread")
    
    for i in range(10):
        x=threading.Thread(target=thread_function,args=(i,))
        x.start()
    print("done")