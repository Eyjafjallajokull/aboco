from subprocess import Popen, PIPE

class BaseWidget():
    name = 'BaseWidget'
    config = {}
    def __init__(self):
        pass
    
    def setConfig(self, config):
        self.config = config
    
    def collectData(self):
        pass
    
    def runSystemCommand(self, cmd, returnStatus=False):
        if not returnStatus:
            return Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE).communicate()[0]
        else:
            return Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE).wait()