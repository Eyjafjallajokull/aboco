from core.widget import BaseWidget

class ProcessorWidget(BaseWidget):
    cores = 1
    
    def __init__(self, config={}):
        super(ProcessorWidget, self).__init__(config)
        self.cores = int(self.runSystemCommand('cat /proc/cpuinfo | grep processor | wc -l'))
        
    def collectData(self):
        """
        s = file('/proc/loadavg', 'r').read()
        return s[0 : s.find(' ')]
        """
        out = self.runSystemCommand('ps -A -o "%cpu" --sort -%cpu')
        sum = 0
        for i in out.split('\n')[1:-1]:
            sum += float(i)
        return sum/self.cores