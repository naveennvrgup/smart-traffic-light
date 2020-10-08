class Signal:
    def __init__(self, dbObj, signals, logger):
        self.dbObj=dbObj
        self.logger=logger
        signals[dbObj.id]=self
        self.logger.info(f"spawned signal {dbObj}")

    @staticmethod
    def signalSpawner(*args):
        obj = Signal(*args)
