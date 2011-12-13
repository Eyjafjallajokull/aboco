from core.widget import BaseWidget

class UptimeWidget(BaseWidget):
    def collectData(self):
        s = file('/proc/uptime', 'r').read()
        return s[0 : s.find(' ')]