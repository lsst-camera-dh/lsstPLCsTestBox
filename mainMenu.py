from pydm import Display
from os import path
import json

class VaccumMonitor(Display):
    def __init__(self, parent=None, args=None, macros=None):
        super(VaccumMonitor, self).__init__(parent=parent, macros=macros)

        self.configs=dict()

        with open(path.join(path.dirname(path.realpath(__file__)),"ip_config.json"),'r') as f:
            self.configs = json.loads(f.read())



        self.ui.gateway_ip.setText(self.configs['plutoGateway_ip'])
        self.ui.gateway_ip.textEdited.connect(self.changeGatewayIp)

        self.ui.gateway_port.setText(str(self.configs['plutoGateway_port']))
        self.ui.gateway_port.textEdited.connect(self.changeGatewayPort)



        self.ui.testBox_ip.setText(self.configs['testBox_ip'])
        self.ui.testBox_ip.textEdited.connect(self.changeTestBoxIp)

        self.ui.testBox_port.setText(str(self.configs['testBox_port']))
        self.ui.testBox_port.textEdited.connect(self.changeTestBoxPort)





    def ui_filename(self):
        return 'mainMenu.ui'

    def ui_filepath(self):
        return path.join(path.dirname(path.realpath(__file__)),"ui", self.ui_filename())


    def changeGatewayIp(self,newValue):
        self.configs["plutoGateway_ip"] = newValue
        self.writeConfigs()

    def changeGatewayPort(self, newValue):
        try:
            self.configs["plutoGateway_port"] = int(newValue)
            self.writeConfigs()
        except:
            self.ui.gateway_port.setText(str(self.configs['plutoGateway_port']))


    def changeTestBoxIp(self,newValue):
        self.configs["testBox_ip"] = newValue
        self.writeConfigs()

    def changeTestBoxPort(self, newValue):
        try:
            self.configs["testBox_port"]= int(newValue)
            self.writeConfigs()
        except:
            self.ui.testBox_port.setText(str(self.configs['testBox_port']))



    def writeConfigs(self):

        with open(path.join(path.dirname(path.realpath(__file__)),"ip_config.json"),'w') as f:
            f.write(json.dumps(self.configs))

        print("Config Saved")
