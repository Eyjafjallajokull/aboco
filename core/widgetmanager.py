import re
import widgets
import pkgutil
import logging
import time
import inspect
import sys
import json
import traceback
from core.config import Config
import hashlib

# http://stackoverflow.com/questions/1707709/list-all-the-modules-that-are-part-of-a-python-package

class WidgetManager():
    ''' 
    Widget Manager
    
    Initialize and collect data from widgets.
    '''
    _widgets = {}
    _installed = {}
    lastCheck = 0
    cache = None
    
    def __init__(self):
        self.loadWidgets()
        self.initWidgets()
        self.interval = Config().get('core','updateInterval')+.5
        
    def loadWidgets(self):
        '''
        Find and import all available widgets. 
        '''
        package=widgets
        for importer, modname, ispkg in pkgutil.walk_packages(path=package.__path__,
                                                          prefix=package.__name__+'.',
                                                          onerror=lambda x: None):
            if modname.endswith('.main') and not ispkg:
                newModule = __import__(modname, globals(), locals(), 'dummy')
                classes = inspect.getmembers(sys.modules[modname], inspect.isclass)
                for (className, _) in classes:
                    if className.endswith('Widget') and className != 'BaseWidget':
                        logging.debug("Found widget %s" % className)
                        self._widgets[className] = getattr(newModule, className)
                        break
                
    def initWidgets(self):
        widgetConfigs = Config().getNamespace('widgets')
        for i in range(len(widgetConfigs)):
            widgetConfig = widgetConfigs[i]
            found = False
            for widgetId, widget in self._widgets.items():
                if widgetConfig['id'] == widgetId:
                    found = True
                    hash = hashlib.md5(widgetId+str(time.time())).digest().encode("base64")
                    hash = re.sub(r'\W+', '', hash)[0:4]
                    try:
                        self._installed[hash] = self._widgets[widgetId](widgetConfig['config'])
                    except KeyError:
                        self._installed[hash] = self._widgets[widgetId]()
                    try:
                        self._installed[hash].setTags(widgetConfig['tags'])
                    except KeyError: pass
            if not found:
                raise Exception('Unknown widget found in config: '+widgetConfig['id'])

    def collectData(self):
        '''
        Collect data from all enabled widgets.
        '''
        if self.lastCheck >= time.time()-self.interval and self.cache != None:
            return self.cache
        
        newData = {}
        for widgetId, widget in self._installed.items():
            widgetData = None
            try:
                widgetData = widget.collectData()
            except Exception as e:
                logging.error(widget.name+': '+str(e)+'\n'+(''.join(traceback.format_stack())))
            newData[widgetId] = widgetData

        self.lastCheck = time.time()
        self.cache = json.dumps(newData)
        return self.cache

    def getConfig(self):
        config = {}
        for (id, widget) in self._installed.items():
            config[id] = { 'id': widget.name, 'config': widget.config, 'tags': widget.tags }
        return config