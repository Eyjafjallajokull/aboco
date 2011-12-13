from core.widget import BaseWidget

class NetworkWidget(BaseWidget):
    def collectData(self):
        return self.runSystemCommand('netstat -nat | tail -n+3 | awk \'{print $6}\' | sort | uniq -c')
        