from core.widget import BaseWidget

class NetworkWidget(BaseWidget):
    prevValues = {'rx':0, 'tx':0}
    
    def collectData(self):
        cmd = '''awk -v interface="%s" -F'[: \t]+' '{ sub(/^ */,"");
            if ($1 == interface) print $2 " " $10; //down up
            }' /proc/net/dev''' % self.config['interface']
        return self.runSystemCommand(cmd)
