import socket
from umodbus.client import tcp
from utils import set_bit,get_bit

class PlutoGateway:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(('192.168.1.100', 502))
        self.dict = None

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
            return self.write_bit(dict[ch]["unitId"],dict[ch]["addr"],dict[ch]["bit"],val)
        else:
            return self.write_single_register(dict[ch]["unitId"],dict[ch]["addr"],val)[0]
