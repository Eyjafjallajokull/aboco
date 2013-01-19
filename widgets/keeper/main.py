import os
from core.widget import BaseWidget

class KeeperWidget(BaseWidget):
    cores = 1
        
    def collectData(self):
        result = self.config['monitor']
        for monitor in result:
            if monitor['type'] == 'process':
                cmd = self.runSystemCommand('ps -o "cmd" -C "%s" -L | wc -l' % monitor['value'])
                monitor['status'] = int(cmd)-1
            if monitor['type'] == 'file':
                if os.path.isfile(monitor['value']):
                    monitor['status'] = os.path.getsize(monitor['value'])
                else:
                    monitor['status'] = -1
            if monitor['type'] == 'command':
                monitor['status'] = self.runSystemCommand(monitor['value'], True)
        return result
