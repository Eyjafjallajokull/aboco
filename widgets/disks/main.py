from core.widget import BaseWidget

class DisksWidget(BaseWidget):
    tags = [ 'system', 'doubleWidth' ]
    def collectData(self):
        return self.runSystemCommand('df -hP | egrep --color=never "^/"')