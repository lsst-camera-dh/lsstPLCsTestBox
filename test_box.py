from maq20 import MAQ20
import time
import json
from os import path


class TestBox:
    def __init__(self,tester,channels_dict):
        with open(path.join(path.dirname(path.realpath(__file__)),"ip_config.json"),'r') as f:
            configs = json.loads(f.read())
            plutoGateway_ip= configs["plutoGateway_ip"]
            plutoGateway_port=configs["plutoGateway_port"]
            testBox_ip=configs["testBox_ip"]
            testBox_port=configs["testBox_port"]

        #print("plutoGateway:",plutoGateway_ip,plutoGateway_port)
        #print("testBox:",testBox_ip,testBox_port)

        self.system = MAQ20(ip_address=testBox_ip, port=testBox_port)
        self.dict = None


        self.dict = channels_dict

        self.plc = Object()
        self.plc.channels=[]

        self.cam = Object()
        self.cam.channels = []

        self.tester=tester

        for ch in self.dict.keys():
            #print(ch)
            try:
                pass
                exec("self.plc."+ch+" = TestBoxChannel(self,'plc','"+ch+"')")
                exec("self.plc.channels.append(self.plc." + ch + ")")
            except Exception as e:
                pass

            try:
                pass
                exec("self.cam." + ch + " = TestBoxChannel(self,'cam','" +ch + "')")
                exec("self.cam.channels.append(self.cam." + ch + ")")
            except Exception as e:
                print(e)
                pass


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
            while abs(module.read_channel_data(port["maq20ModuleAddr"])-value)>0.6 and value !=1 and module.read_output_channels()>0:
                module.write_channel_data(port["maq20ModuleAddr"], float(value))
                time.sleep(0.05)
                n+=1
                if n>50:
                    raise ValueError("Failed to write to channel")


    def press_port(self, ch):
        self.write_port(ch, 0)
        time.sleep(0.2)
        self.write_port(ch, 1)
        time.sleep(0.5)
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

        #print (self.ch)

        read = self.server.read_port(self.side,self.ch)
        #print(read,type(read))

        if self.type=="Digital" :
            #print(self.ch,"DIGI")
            if (read >1 or read<-1):
                return read>4 or read<-4
            else:
                return read>0.5
        elif self.type=="NONE":
            return None
        else:
            #print(self.ch, "ANA", read, type(read))
            return read

    def write(self,val,note=""):
        #print('>>>>>>>>>>>>>>',dir(self.server.tester))
        self.server.tester.log("Write %s to %s. %s" % (str(val),str(self.ch),  str(note)))
        return self.server.write_port(self.side, self.ch,val)

    def press(self,note=""):
        self.server.tester.log("Pressing %s. %s"%(self.ch,str(note)))
        return self.server.press_port(self.side, self.ch)

    def checkValue(self,val,checkBlink=False):
        if val==-1:
            return True
        if self.type == "Digital":
            if val == "P":
                return int(self.read()) == int(0)
            else:
                return int(self.read()) is int(val)

        elif self.type == "Analog":
            return abs(self.read()-int(val))<40

        elif self.type == "DigitalBlink":
            if checkBlink:
                if val == 0:
                    return self.checkNoBlink()
                elif val == 2:
                    return self.checkBlink()
            else:
                return True

    def checkBlink(self,timeout=3):
        zero = 0
        one = 0
        start = time.time()
        while time.time() - start < timeout:
            time.sleep(0.03)
            reg = self.read()
            if reg:
                one += 1
            else:
                zero += 1

            if zero > 2 and one > 2:
                return True
        return False

    def checkNoBlink(self,timeout=1):
        start = time.time()
        while time.time() - start < timeout:
            reg = self.read()
            if reg != 0:
                return False
        return True



class Object(object):
    pass
