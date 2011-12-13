from core.widget import BaseWidget

class DisksWidget(BaseWidget):
    def collectData(self):
        return self.runSystemCommand('df -hP | egrep --color=never "^/"')