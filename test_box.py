from maq20 import MAQ20
import time
from mapping_parser import import_mappings
from dotmap import DotMap


class TestBox:
    def __init__(self,tester):
        self.system = MAQ20(ip_address="192.168.1.101", port=502)
        self.dict = None

        self.dict, plutoGateway = import_mappings()

        self.plc = Object()
        self.plc.channels=[]

        self.cam = Object()
        self.cam.channels = []

        self.tester=tester



        for ch in self.dict.keys():
            try:
                pass
                exec(("self.plc."+ch+" = TestBoxChannel(self,'plc','"+ch+"')"))
                exec("self.plc.channels.append(self.plc." + ch + ")")
            except Exception as e:
                pass

            try:
                pass
                #exec("self.cam." + ch + " = TestBoxChannel(self,'cam','" + ch + "')")
                #exec("self.cam.channels.append(self.cam." + ch + ")")
            except:
                pass

        #print(self.plc.channels)

    def close(self):
        pass


    def read_port(self,side,port):
        port = self.dict[port][side]

        module = self.system.find(port["maq20ModuleSn"])

        if not module.has_range_information():
            response = module.read_channel_data_counts(port["maq20ModuleAddr"])
        else:
            module.load_channel_active_ranges()
            response = module.read_channel_data(port["maq20ModuleAddr"])
        return response


    def write_port(self,side,port,value):
        port = self.dict[port][side]
        module = self.system.find(port["maq20ModuleSn"])
        value=float(value)


        if not module.has_range_information():
            module.write_register(1000 + port["maq20ModuleAddr"], int(value))
        else:
            module.write_channel_data(port["maq20ModuleAddr"], float(value))

            n = 0
            while abs(module.read_channel_data(port["maq20ModuleAddr"])-value)>0.4 and value !=1 and module.read_output_channels()>0:
                module.write_channel_data(port["maq20ModuleAddr"], float(value))
                time.sleep(0.01)
                print("Can't write")
                n+=1
                #if n>10:
                 #   break


    def press_port(self, ch):
        self.write_port(ch, 0)
        time.sleep(0.2)
        self.write_port(ch, 1)
        time.sleep(0.2)
        self.write_port(ch, 0)


class TestBoxChannel():

    def __init__(self,server,side, ch):
        self.server = server
        self.side = side
        self.ch = ch
        self.type = self.server.dict[ch][side]["type"]

        self.default_value = self.server.dict[ch][side]["default_value"]
        self.boot_value = self.server.dict[ch][side]["boot_value"]


    def read(self):
        read = self.server.read_port(self.side,self.ch)
        if self.type=="Digital" :
            if (read >1 or read<-1):
                return read>4 or read<-4
            else:
                return read>0.5
        else:
            return read

    def write(self,val,note=""):
        self.server.tester.log("Write %s to %s. %s" % (str(val),str(self.ch),  str(note)))
        return self.server.write_port(self.side, self.ch,val)

    def press(self,note=""):
        self.server.tester.log("Pressing %s. %s"%(self.ch,str(note)))
        return self.server.press_port(self.side, self.ch)

    def checkValue(self,val):
        if val==-1:
            return True
        if self.type == "Digital":
            return int(self.read()) is int(val)
        else:
            return abs(int(self.read())-int(val))<40



class Object(object):
    pass
