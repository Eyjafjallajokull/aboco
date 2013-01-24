from subprocess import Popen, PIPE

class BaseWidget(object):
    '''
    Base widget class

    All widgets must inherit from this class.
    '''

    config = {}
    tags = []

    @property
    def name(self):
        return self.__class__.__name__

    def __init__(self, config={}):
        self.setConfig(config)
    
    def setConfig(self, config):
        self.config = config

    def setTags(self, tags):
        self.tags = tags
    
    def collectData(self):
        ''' 
        Gather and return system information
        
        Return value of this function will be json encoded and sent to web client.
        '''
        pass
    
    def runSystemCommand(self, cmd, returnStatus=False):
        ''' Run shell command '''
        if returnStatus:
            return Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE).wait()
        else:
            return Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE).communicate()[0]
