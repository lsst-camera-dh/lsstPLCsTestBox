from os import path
from pydm import Display
from mapping_parser import *

maq20_ip = "192.168.1.101"
maq20_port = 502

class VaccumMonitor(Display):
    def __init__(self, parent=None, args=None, macros=None):
        super(VaccumMonitor, self).__init__(parent=parent, macros=macros)

        modbus_mapping_path = path.join(path.dirname(path.realpath(__file__)), "mapping", "vac_modbus_mapping.csv")
        testbox_mapping_path = path.join(path.dirname(path.realpath(__file__)), "mapping", "vac_testbox_mapping.csv")

        self.testBox, self.modbus = import_mappings(modbus_mapping_path,testbox_mapping_path)

        '''for widget in dir(self.ui):
            try:
                if "channel" in dir(getattr(self.ui,widget)):
                    channel = getattr(getattr(self.ui, widget),"channel")

                    if channel.split("://")[0] == "testBox":
                        side , name = find_test_box_address(self.map, channel.split("://")[1])


                        channel = "testBoxMaq20://" + side + ":" + name
                        setattr(getattr(self.ui, widget), "channel", channel)

                    channel = getattr(getattr(self.ui, widget), "channel")
                    if channel.split("://")[0] == "testBoxMaq20":
                        module_sn, address = find_maq20_address(self.map,channel.split("://")[1])
                        if module_sn is not None and address is not None:
                            channel = "maq20://"+maq20_ip+":"+str(maq20_port)+"/"+module_sn+":"+str(address)
                        setattr(getattr(self.ui, widget), "channel",channel)
            except:
                pass
                '''
        for widget in dir(self.ui):
            if "channel" in dir(getattr(self.ui,widget)):
                channel = getattr(getattr(self.ui, widget),"channel")

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
                        print(channel, side, port)
                        print("Failed to parse channel: ",channel)






    def ui_filename(self):
        return 'vaccumMonitor.ui'

    def ui_filepath(self):
        return path.join(path.dirname(path.realpath(__file__)),"ui", self.ui_filename())



def import_maq20_mapping(path):
    import csv

    map = dict()
    map["plc"]=dict()
    map["cam"]=dict()

    with open(path, 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if row[3] != "":
                map[row[4]][row[3]]=dict()
                map[row[4]][row[3]]["module"]=row[0]
                map[row[4]][row[3]]["module_sn"] = row[1]
                map[row[4]][row[3]]["address"] = row[2]
                map[row[4]][row[3]]["plc_port_name"] = row[5]

    return map



def find_maq20_address(map,name):
    side = name.split(":")[0]
    port_name = name.split(":")[1]
    module_sn = map[side][port_name]["module_sn"]
    address = map[side][port_name]["address"]

    if module_sn == "":
        module_sn = None
    if address =="":
        address = None

    return (module_sn,address)


def find_test_box_address(map,name):

    side = name.split(":")[0]
    port_name = name.split(":")[1]

    test_box_name = None
    for port in map[side].keys():
        if map[side][port]["plc_port_name"] == port_name:
            test_box_name = port

    return (side,test_box_name)