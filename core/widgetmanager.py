import widgets
import pkgutil
import logging
import time
import inspect
import sys
import json
import time
from core.config import Config

# http://stackoverflow.com/questions/1707709/list-all-the-modules-that-are-part-of-a-python-package

class WidgetManager():
    _widgets = {}
    lastCheck = 0
    cache = None
    
    def __init__(self):
        self.loadWidgets()
        
    def loadWidgets(self):
        package=widgets
        for importer, modname, ispkg in pkgutil.walk_packages(path=package.__path__,
                                                          prefix=package.__name__+'.',
                                                          onerror=lambda x: None):
            if modname.endswith('.main') and not ispkg:
                newModule = __import__(modname, globals(), locals(), 'dummy')
                className = inspect.getmembers(sys.modules[modname], inspect.isclass)[1][0]
                
                if className.endswith('Widget') and len(className)>len('Widget'):
                    self._widgets[className] = newModule
                    logging.debug("Found widget %s" % className)
                
        for widgetId, widget in self._widgets.items():
            self._widgets[widgetId] = getattr(widget, widgetId)()
            
            
    def collectData(self):
        if self.lastCheck >= time.time()-Config().get('core','updateInterval')+.5 and self.cache != None:
            return self.cache
        
        newData = []
        installedWidgets = Config().getNamespace('widgets')
        for widgetInstanceId in range(len(installedWidgets)):
            installedWidgetConfig = installedWidgets[widgetInstanceId]
            
            found = False
            for widgetId, widget in self._widgets.items():
                if installedWidgetConfig['id'] == widgetId:
                    try:
                        widget.setConfig( installedWidgetConfig['config'] )
                    except KeyError:
                        pass
                    
                    newData.append( widget.collectData() )
                    found = True
            if not found:
                raise Exception('Unknown widget found in config.')
            
        self.lastCheck = time.time()
        self.cache = json.dumps(newData)
        return self.cache