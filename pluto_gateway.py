import socket
from umodbus.client import tcp
from utils import set_bit,get_bit
import time
from mapping_parser import import_mappings
from dotmap import DotMap

class PlutoGateway:
    def __init__(self,tester):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(('192.168.1.100', 502))
        self.dict = None

        testBox, self.dict = import_mappings()

        self.channels=[]

        self.tester=tester

        for ch in self.dict.keys():
            try:
                exec("self." + ch + " = PlutoGatewayChannel(self,'" + ch + "')")
                exec("self.channels.append(self." + ch + ")")
            except Exception as e:
                pass
                raise e
       # print((self.channels))


    def read_holding_registers(self, slave_id, starting_address, quantity):
        message = tcp.read_holding_registers(slave_id, starting_address, quantity)
        response = tcp.send_message(message, self.sock)
        return response

    def write_single_registers(self, slave_id, starting_address, val):
        message = tcp.write_single_register(slave_id, starting_address, val)
        response = tcp.send_message(message, self.sock)
        return response

    def read_bit(self, slave_id, address, bit):
        message = tcp.read_holding_registers(slave_id, address, 1)
        return get_bit(tcp.send_message(message, self.sock)[0],bit)

    def write_bit(self, slave_id, address, bit,value):
        message = tcp.read_holding_registers(slave_id, address, 1)
        current_value = tcp.send_message(message, self.sock)[0]

        new_value = set_bit(current_value,bit,value)

        message = tcp.write_single_register(slave_id, address,new_value)
        response = tcp.send_message(message, self.sock)
        return response

    def read_ch(self,ch):
        dict = self.dict
        if dict[ch]["bit"] != None:
            return self.read_bit(dict[ch]["unitId"],dict[ch]["addr"],dict[ch]["bit"])
        else:
            return self.read_holding_registers(dict[ch]["unitId"],dict[ch]["addr"],1)[0]

    def write_ch(self,ch,val):
        dict = self.dict
        if dict[ch]["bit"] != None:

            while (self.read_bit(dict[ch]["unitId"],dict[ch]["addr"],dict[ch]["bit"])!=val):
                self.write_bit(dict[ch]["unitId"], dict[ch]["addr"], dict[ch]["bit"], val)
                time.sleep(0.001)

        else:
            while self.read_holding_registers(dict[ch]["unitId"],dict[ch]["addr"])!=val:
                self.write_single_register(dict[ch]["unitId"],dict[ch]["addr"],val)[0]
                time.sleep(0.001)

    def press_ch(self,ch):
        self.write_ch(ch, 0)
        time.sleep(0.1)
        self.write_ch(ch, 1)
        time.sleep(0.5)
        self.write_ch(ch, 0)
        time.sleep(0.1)

    def close(self):
        self.sock.close()
        self.sock = None



class PlutoGatewayChannel():

    def __init__(self, server, ch, type="D"):
        self.ch = ch
        self.type = type
        self.server = server
        self.default_value = self.server.dict[ch]["default_value"]
        self.boot_value = self.server.dict[ch]["boot_value"]
        self.type = self.server.dict[ch]["type"]

    def read(self):
        return self.server.read_ch(self.ch)

    def write(self,val,note=""):
        self.server.tester.log("Write %s to %s. %s"%(str(val),self.ch,str(note)))

        return self.server.write_ch(self.ch,(val))

    def press(self,note=""):
        self.server.tester.log("Pressing %s. %s"%(self.ch,str(note)))
        return self.server.press_ch(self.ch)

    def checkValue(self,val,checkBlink=False):
        if (val) is -1:
            return True
        if self.type == "Analog":
            return abs(self.read()-int(val))<40
        elif self.type == "DigitalBlink":
            if checkBlink:
                if val == 0:
                    return self.checkNoBlink()
                elif val == 2:
                    return self.checkBlink()
            else:
                return True
        else:
            if val == "P":
                return int(self.read())==int(0)
            else:
                return int(self.read()) is int(val)


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




#plutoGateway = PlutoGateway()

#print(plutoGateway.read_holding_registers(4, 0, 42))

#plutoGateway.HVStatBlock_w.write(0)



#print( plutoGateway.write_ch('CVStatLatchReset_w',0) )