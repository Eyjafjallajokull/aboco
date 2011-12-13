from core.widget import BaseWidget

class MemoryWidget(BaseWidget):
    def collectData(self):
        meminfo = file('/proc/meminfo', 'r')
        total = meminfo.readline()[0:-4]
        free = meminfo.readline()[0:-4]
        buffers = meminfo.readline()[0:-4]
        cached = meminfo.readline()[0:-4]
        meminfo.close()
        
        total = int(total[total.rfind(' ')+1:-1])
        free = int(free[free.rfind(' ')+1:-1])
        buffers = int(buffers[buffers.rfind(' ')+1:-1])
        cached = int(cached[cached.rfind(' ')+1:-1])
        return {'total': total, 
                'free': free, 
                'buffers': buffers,
                'cached': cached,
                'used': total-free-buffers-cached }