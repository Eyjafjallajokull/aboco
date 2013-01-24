from core.widget import BaseWidget

class ProcessesWidget(BaseWidget):
    tags = ['doubleWidth','system']
    def collectData(self):
        return self.runSystemCommand('ps -A -o "user pid %cpu %mem cmd" --sort -%cpu | head -11 | tail -10')