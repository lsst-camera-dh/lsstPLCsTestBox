from os import path
from pydm import Display
from mapping_parser import *

maq20_ip = "192.168.1.101"
maq20_port = 502

class VaccumMonitor(Display):
    def __init__(self, parent=None, args=None, macros=None):
        super(VaccumMonitor, self).__init__(parent=parent, macros=macros)

        modbus_mapping_path = path.join(path.dirname(path.realpath(__file__)), "mapping", "mpm_modbus_mapping.csv")
        testbox_mapping_path = path.join(path.dirname(path.realpath(__file__)), "mapping", "mpm_testbox_mapping.csv")

        self.testBox, self.plutoGateway = import_mappings(modbus_mapping_path,testbox_mapping_path)

        for widget in dir(self.ui):
            if "channel" in dir(getattr(self.ui,widget)):
                channel = getattr(getattr(self.ui, widget),"channel")

               # print (channel)

                if channel.split("://")[0] == "testBox":

                    side = channel.split("://")[1].split(":")[0]
                    port = channel.split("://")[1].split(":")[1]

                    try:
                        maq20_ip = "192.168.1.101"
                        maq20_port = 502
                        module_sn = self.testBox[port][side]['maq20ModuleSn']
                        address = self.testBox[port][side]['maq20ModuleAddr']

                        channel = "maq20://"+maq20_ip+":"+str(maq20_port)+"/"+module_sn+":"+str(address)
                        setattr(getattr(self.ui, widget), "channel",channel)
                    except:
                        print("Failed to parse channel: ",channel)

                elif channel.split("://")[0] == "plutoGateway" :

                    channel = channel.split("://")[1]

                    try:
                        ip = "192.168.1.100"
                        port = 502
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








