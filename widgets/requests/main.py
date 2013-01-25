import time
from core.widget import BaseWidget
import os
from multiprocessing import Process, Value

class RequestsWidget(BaseWidget):

    def __init__(self, config={}):
        super(RequestsWidget, self).__init__(config)
        self.fileError = not os.path.exists(self.config['file'])
        if self.fileError:
            return

        file = open(self.config['file'])
        file.seek(0, os.SEEK_END)
        self.lines = Value('i', 0)
        self.readerProcess = Process(target=reader, args=(self.lines, file))
        self.readerProcess.start()

    def __del__(self):
        if self.readerProcess:
            self.readerProcess.terminate()

    def collectData(self):
        if self.fileError:
            return {'error':'File %s does not exist' % self.config['file']}

        value = self.lines.value
        self.lines.value = 0
        return value

def reader(lines, stream):
    while True:
        lines.value += len(stream.readlines())
        time.sleep(0.1)
