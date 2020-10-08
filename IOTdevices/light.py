from google.cloud import pubsub_v1

class Light:
    def __init__(self, dbObj, lights, logger, signal=None):
        self.dbObj=dbObj
        self.logger=logger
        self.signal=signal
        lights[dbObj.id]=self
        self.logger.info(f"spawned light {dbObj}")



    @staticmethod
    def lightSpawner(*args):
        obj = Light(*args)
