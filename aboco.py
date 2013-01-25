import sys
import os
import logging
from core.http import AbocoHTTPServer
from core.config import Config
from core.widgetmanager import WidgetManager

class Aboco():
    ''' Main application controller '''
    
    def __init__(self):
        ''' initialize whole application '''
        self.initLogging()
        self.initWidgetManager()
        self.initHTTPServer()
        
    def initLogging(self):
        logLevel = logging._levelNames.get(Config().get('core','logging'))

        rawFormatter = logging.Formatter('%(asctime)s;%(levelname)s;%(message)s')
        prettyFormatter = logging.Formatter('%(message)s')
        stdoutHandler = logging.StreamHandler(sys.stdout)
        stdoutHandler.setFormatter(prettyFormatter)
        fileHandler = logging.FileHandler('aboco.log')
        fileHandler.setFormatter(rawFormatter)
        logging.root.setLevel(logLevel)
        logging.root.addHandler(stdoutHandler)
        logging.root.addHandler(fileHandler)

#        logging.basicConfig(format='%(asctime)s %(levelname)s > %(message)s',
#                            datefmt='%Y/%m/%d %H:%M:%S',
#                            level=logLevel)
    
    def initWidgetManager(self):
        self.wm = WidgetManager()
        
    def initHTTPServer(self):
        httpsrv = AbocoHTTPServer(self.wm)
        httpsrv.start()

if __name__ == '__main__':
    Aboco()
