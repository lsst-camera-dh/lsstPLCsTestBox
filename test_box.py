from maq20 import MAQ20

class TestBox:
    def __init__(self):
        self.system = MAQ20(ip_address="192.168.1.101", port=502)
        self.dict = None

    def read_port(self,side,port):
        port = self.dict[port][side]

        print (port)
        module = self.system.find(port.maq20ModuleSn)

        print("vip")

        if module.get_name() in ["MAQ20-DORLY20  "] or not module.has_range_information():
            response = module.read_channel_data_counts(port.maq20ModuleAddr)
        else:
            module.load_channel_active_ranges()
            response = module.read_channel_data(port.maq20ModuleAddr)

        return response


    def write_port(self,side,port,value):
        port = self.dict[port]
        module = self.system.find(port.maq20ModuleSn)

        if module.get_name() in ["MAQ20-DORLY20  "] or not module.has_range_information():
            module.write_register(1000 + port.maq20ModuleAddr, value)
        else:
            module.write_channel_data(port.maq20ModuleAddr, value)



