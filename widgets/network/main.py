from core.widget import BaseWidget

class NetworkWidget(BaseWidget):
    prevValues = {'rx':0, 'tx':0}
    
    def collectData(self):
        interfaces = self.runSystemCommand('cat /proc/net/dev | awk \'{print $2,$10}\'').split('\n')[2:-1]
        interfaces = [a.split(' ') for a in interfaces]
        
        currentValues = {'rx':0, 'tx':0}
        for interface in interfaces:
            currentValues['rx'] = currentValues['rx'] + int(interface[0])
            currentValues['tx'] = currentValues['tx'] + int(interface[1])
        
        diff = { 'rx': abs(self.prevValues['rx'] - currentValues['rx']),
                 'tx': abs(self.prevValues['tx'] - currentValues['tx']) }
        diff = diff if self.prevValues['rx']!=0 else {'rx':0, 'tx':0}
        self.prevValues = currentValues
        return diff
        