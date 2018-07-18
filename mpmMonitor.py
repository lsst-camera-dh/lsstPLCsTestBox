from os import path
from pydm import Display
from mapping_parser import *
import json


class VaccumMonitor(Display):
    def __init__(self, parent=None, args=None, macros=None):
        super(VaccumMonitor, self).__init__(parent=parent, macros=macros)

        with open(path.join(path.dirname(path.realpath(__file__)),"ip_config.json"),'r') as f:
            configs = json.loads(f.read())
        plutoGateway_ip= configs["plutoGateway_ip"]
        plutoGateway_port=configs["plutoGateway_port"]
        testBox_ip=configs["testBox_ip"]
        testBox_port=configs["testBox_port"]

        print("plutoGateway:",plutoGateway_ip,plutoGateway_port)
        print("testBox:",testBox_ip,testBox_port)

        plutoGateway_mapping_path = path.join(path.dirname(path.realpath(__file__)), "mapping", "mpm_modbus_mapping.csv")
        testbox_mapping_path = path.join(path.dirname(path.realpath(__file__)), "mapping", "mpm_testbox_mapping.csv")

        self.testBox, self.plutoGateway = import_mappings(plutoGateway_mapping_path,testbox_mapping_path)

        for widget in dir(self.ui):
            if "channel" in dir(getattr(self.ui,widget)):
                channel = getattr(getattr(self.ui, widget),"channel")

                if channel.split("://")[0] == "testBox":
                    side = channel.split("://")[1].split(":")[0]
                    port = channel.split("://")[1].split(":")[1]
                    try:
                        maq20_ip = testBox_ip
                        maq20_port = testBox_port
                        module_sn = self.testBox[port][side]['maq20ModuleSn']
                        address = self.testBox[port][side]['maq20ModuleAddr']
                        channel = "maq20://"+maq20_ip+":"+str(maq20_port)+"/"+module_sn+":"+str(address)
                        setattr(getattr(self.ui, widget), "channel",channel)
                    except:
                        print("Failed to parse channel: ",channel)

                elif channel.split("://")[0] == "plutoGateway" :
                    channel = channel.split("://")[1]
                    try:
                        ip = plutoGateway_ip
                        port = plutoGateway_port
                        unit_id = self.plutoGateway[channel]['unit_id']
                        type = self.plutoGateway[channel]['mb_type']
                        address = self.plutoGateway[channel]['addr']
                        bit = self.plutoGateway[channel]['bit']
                        channel = "modbus://"+ip+":"+str(port)+"/"+str(unit_id)+":"+str(type)+":"+str(address)
                        if bit is not None:
                            channel = channel + "."+str(bit)
                        setattr(getattr(self.ui, widget), "channel",channel)
                    except:
                        print("Failed to parse channel: ",channel)
                else:
                    print(channel)

    def ui_filename(self):
        return 'mpmMonitor.ui'

    def ui_filepath(self):
        return path.join(path.dirname(path.realpath(__file__)),"ui", self.ui_filename())








