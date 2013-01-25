from core.widget import BaseWidget

class MemoryWidget(BaseWidget):
    tags = [ 'system' ]
    def collectData(self):
        meminfo = self.runSystemCommand('head -4 /proc/meminfo').split('\n')[0:4]
        (total, free, buffers, cached) = meminfo
        return {'total': total,
                'free': free, 
                'buffers': buffers,
                'cached': cached }