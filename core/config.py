import os
import json
import logging

class Config:
    defaults = { 
                'http':{
                        'address':'localhost',
                        'port':2468,
                        'threads':1
                        },
                'core':{
                        'logging':'INFO'
                        },
                'client':{
                        'core':{
                                'updateInterval':5
                                }
                        }
                }
    fileName = 'config.json'
    __config = None
    __shared_state = {}
    
    def __init__(self):
        self.__dict__ = self.__shared_state
        if self.__config == None:
            self.load()
    
    def save(self):
        logging.debug('save config file')
        cf = open(self.fileName, 'w')
        json.dump(self.__config, cf, indent=2)
        cf.close()
        
    def load(self):
        if os.path.isfile(self.fileName):
            cf = file(self.fileName,'r')
            self.__config = json.load(cf)
            cf.close()
            
            self.__config = dict(self.defaults, **self.__config)
        else:
            self.__config = self.defaults
            self.save()
            
    def get(self, namespace, name, default=None):
        if namespace in self.__config and name in self.__config[namespace]:
            return self.__config[namespace][name]
        else:
            return default
    
    def set(self, namespace, name, value):
        if not namespace in self.__config:
            self.__config[namespace] = {}
        self.__config[namespace][name] = value
        self.save()
            
    def getNamespace(self, namespace, string=False):
        if namespace in self.__config:
            if string:
                return json.dumps(self.__config[namespace])
            return self.__config[namespace]
        else:
            return {}
    
    def setNamespace(self, namespace, value):
        if type(value).__name__ == 'str':
            value = json.loads(value)
        print type(value)
        self.__config[namespace] = value
        self.save()
