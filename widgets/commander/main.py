from core.widget import BaseWidget

class CommanderWidget(BaseWidget):
    def collectData(self):
        return self.runSystemCommand(self.config['command'])