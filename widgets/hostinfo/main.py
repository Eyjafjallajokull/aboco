from core.widget import BaseWidget

class HostInfoWidget(BaseWidget):
    tags = [ 'customWidget','system' ]
    def collectData(self):
        return {
            "uname": self.runSystemCommand('uname -snrmo'),
            "date": self.runSystemCommand('date'),
            "uptime": file('/proc/uptime', 'r').read()
        }