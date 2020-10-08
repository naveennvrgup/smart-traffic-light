# ---------------------------------------------------------------------------- #
#                             run in django context                            #
# ---------------------------------------------------------------------------- #

import sys
import os
import django
import logging
from pathlib import Path
import tkinter as tk


projectDir = str(Path(__file__).parent.parent.absolute())
sys.path.append(projectDir)

os.environ['DJANGO_SETTINGS_MODULE'] = 'server.settings'
django.setup()


# ---------------------------------------------------------------------------- #
#                                  setup logs                                  #
# ---------------------------------------------------------------------------- #

import colorlog

handler = colorlog.StreamHandler()
handler.setFormatter(colorlog.ColoredFormatter(
    fmt='%(log_color)s %(asctime)s : %(message)s',
    datefmt='%m-%d %H:%M:%S'
    ))

logger = colorlog.getLogger('example')
logger.setLevel('DEBUG')
logger.addHandler(handler)


# ---------------------------------------------------------------------------- #
#                                   emulator                                   #
# ---------------------------------------------------------------------------- #

from maps.models import *

class Emulator:
   # state shared by each instance 
    __shared_state = dict() 
    state=None
  
    # constructor method 
    def __init__(self): 
  
        self.__dict__ = self.__shared_state 

        print(self.state)
        if not self.state:
            logger.debug("adfasd")
            logger.info("adfasd")
            logger.warning("adfasd")
            logger.error("adfasd")
        self.state = 'GeeksforGeeks'
  
    def __str__(self): 
        return self.state 

# ---------------------------------------------------------------------------- #
#                                 run emulator                                 #
# ---------------------------------------------------------------------------- #

if __name__ == "__main__":
    Emulator()
    a=tk.Tk()