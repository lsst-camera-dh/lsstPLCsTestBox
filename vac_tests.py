from tester import Test
from pluto_gateway import PlutoGateway
from test_box import TestBox
from mapping_parser import import_mappings
from utils import set_bit,get_bit

from dotmap import DotMap


class test0(Test):
    def __init__(self,tester,id):
        Test.__init__(self,tester,id)
        self.name = "Template"
        self.desc = "Template"

    def test(self):
        self.log("Initial message.")
        if False:
            self.log("Failure message.")
            return False
        self.log("Success message")
        return True


class test1 (Test):
    def __init__(self,tester,id):
        Test.__init__(self,tester,id)
        self.name = "Connect to Pluto Gateway"
        self.desc = "192.168.1.100:502"

    def test(self):
        try:
            self.log("Trying to connect to Pluto Gateway.")
            self.tester.plutoGateway = PlutoGateway()
            
            testBox , plutoGateway = import_mappings()
            self.tester.plutoGateway.dict = DotMap(plutoGateway)

        except Exception as e:
            self.log("Can't connect to Pluto Gateway :: "+str(e))
            return False

        self.log("Successfully connected to Pluto Gateway")
        return True


class test11(Test):
    def __init__(self, tester, id):
        Test.__init__(self, tester, id)
        self.name = "Connect to Test Box"
        self.desc = "192.168.1.101:502"

    def test(self):
        try:
            self.log("Trying to connect to Test Box.")
            self.tester.testBox = TestBox()

            testBox, plutoGateway = import_mappings()
            self.tester.testBox.dict = DotMap(testBox)

        except Exception as e:
            self.log("Can't connect to Test Box :: " + str(e))
            return False

        self.log("Successfully connected to Test Box")
        return True


class test2(Test):
    def __init__(self,tester,id):
        Test.__init__(self,tester,id)
        self.name = "Pluto Gateway Config"
        self.expected_config = [0, 3, 0, 0, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 0, 0, 0,
                                    0, 0, 0, 0,
                                    0, 0, 0, 0, 0, 0, 0, 0, 99, 0, 0, 0, 0]
        self.desc = "Check Pluto Gateway configuration registers. Expected:" + str(self.expected_config)

    def test(self):
        config = self.tester.plutoGateway.read_holding_registers(4, 0, 42)
        for i in range(len(self.expected_config)):
            if config[i] != self.expected_config[i]:
                self.log(("Pluto Gateway Config doesn't match expected values.\nConfig:\t\t%s\nExpected config:%s" % (
                str(config), str(self.expected_config))))
                return False
        self.log(("Pluto Gateway Config match expected values.\nConfig:\t\t%s \nExpected config:%s"%(str(config),str(self.expected_config))))
        return True


class test3(Test):
    def __init__(self,tester,id):
        Test.__init__(self,tester,id)
        self.name = "Pluto Bus"
        self.desc = "Check Pluto Gateway sees Pluto D45 as node 0."

    def test(self):
        mask = self.tester.plutoGateway.read_holding_registers(36, 1, 1)[0]

        if mask == 0:
            self.log("Pluto Gateway doens't see any PLC")
            return False
        elif mask != 1:
            self.log(
                "Pluto Gateway see a PLC(s) in  unexpected nodes adds. Binary mask for detected PLCs:{0:b}".format(
                    mask))
            return False

        self.log(("Pluto Gateway sees D45 PLC as node 0"))
        return True


class test4(Test):
    def __init__(self,tester,id):
        Test.__init__(self,tester,id)
        self.name = "Pluto Modbus Read Default"
        self.desc = ""
        self.expected_values = [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 21, 2, 23, 2, 22, 2, 22, 2, 22, 2, 0, 0, 23, 2, 22, 2, 0, 127, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    def test(self):

        for n in range(5):
            self.log(("Read number %d/5:" % (n+1)))
            self.sleep(0.13)

            read=[]
            for add in range(130):
                reg = self.tester.plutoGateway.read_holding_registers(36, add, 1)
             #   print(reg)
                read.append(reg[0])

            for i, reg in enumerate(read):
                if reg != self.expected_values[i]:

                    # Analog Voltages margin
                    if i in [67,69,71,75,77,79,81]:
                        if not( reg>15 and reg < 25):
                            self.log(("Analog Voltage Register %d not in expected interval (15-25) : %d "%(i,reg)))
                            return False

                    # Analog Scaled Values margin
                    elif i in [68, 70, 72, 76, 78, 80, 82]:
                        if not(reg > 0 and reg < 3):
                            self.log(("Analog Scaled Register %d not in expected interval (0-3) : %d " % (i, reg)))
                            return False

                    # Test the ones that should be blinking
                    elif i in [86,88,90,96]:
                        pass

                    else:
                        self.log(("Digtial Register %d doesn't match in expected value (%d) : %d " % (i, self.expected_values[i],reg)))
                        return False

        reg = self.tester.plutoGateway.read_holding_registers(36, 86, 1)[0]
        reg = set_bit(reg,4,0)
        reg = set_bit(reg,6,0)
        expected = 00
        if reg != expected:
            self.log(
                ("Digtial Register %d doesn't match in expected value (%d) : %d " % (i, expected, reg)))
            return False


        reg = self.tester.plutoGateway.read_holding_registers(36, 88, 1)[0]
        reg = set_bit(reg,4,0)
        reg = set_bit(reg,6,0)
        expected = 0
        if reg != expected:
            self.log(
                ("Digtial Register %d doesn't match in expected value (%d) : %d " % (i, expected, reg)))
            return False

        reg = self.tester.plutoGateway.read_holding_registers(36, 90, 1)[0]
        reg = set_bit(reg,1,0)
        reg = set_bit(reg,4,0)
        expected = 0
        if reg != expected:
            self.log(
                ("Digtial Register %d doesn't match in expected value (%d) : %d " % (i, expected, reg)))
            return False

        reg = self.tester.plutoGateway.read_holding_registers(36, 96, 1)[0]
        reg = set_bit(reg,1,0)
        reg = set_bit(reg,4,0)
        expected = 0
        if reg != expected:
            self.log("Digtial Register %d doesn't match in expected value (%d) : %d " % (i, expected, reg))
            return False

        def test_blink(add,bit):
            self.log("Testing blink on add %d.%d" % (add,bit))
            zero = 0
            one = 0
            for n in range(50):
                self.sleep(0.05)
                reg = self.tester.plutoGateway.read_holding_registers(36, add, 1)[0]
                if get_bit(reg,bit):
                    one +=1
                else:
                    zero+=1

                if zero>2 and one>2:
                    return True

            self.log("Digtial bit %d.%d is not blinking" % (add, bit))
            return False

        if not test_blink(86,4):
            return False
        if not test_blink(86,6):
            return False

        if not test_blink(88,4):
            return False
        if not test_blink(88,6):
            return False

        if not test_blink(90,1):
            return False
        if not test_blink(90,4):
            return False

        if not test_blink(96,1):
            return False
        if not test_blink(96,4):
            return False

        self.log("Pluto read modbus registers default values as expected" )
        return True


class test5(Test):
    def __init__(self, tester, id):
        Test.__init__(self, tester, id)
        self.name = "Pluto Modbus write registers default"
        self.desc = ""
        self.expected_values = [0, 0]

    def test(self):
        read = []
        for add in [2,5]:
            reg = self.tester.plutoGateway.read_holding_registers(1, add, 1)
            read.append(reg[0])
        print(read)

        for n in range(1):
            self.log(("Read number %d/1:" % (n + 1)))
            self.sleep(0.134)
            for i, reg in enumerate(read):
                if reg != self.expected_values[i]:
                        self.log(("Digtial Register %d doesn't match in expected value (%d) : %d " % (
                        i, self.expected_values[i], reg)))
                        return False



        self.log("Pluto write modbus registers default values as expected")
        return True

class test6(Test):
    def __init__(self,tester,id):
        Test.__init__(self,tester,id)
        self.name = "Permits and valves Off on boot"
        self.desc = "Check if all permits are off when the PLC is powered"

    def test(self):
        self.log(self.desc)

        for port in ["Q0","Q1","Q2","Q3","Q4","Q5","IQ20","IQ21","IQ22","IQ23"]:
            if self.tester.testBox.read_port("plc",port) > 0.5:
                self.log("PLC output %s is not off."%port)
                return False

        for ch in ["HVStat","CVStat","VcrPumpPerm","VhxPumpPerm","MainVcrVcc","MainVhxVcc","VcrVcc01","VcrVcc02","VcrVcc03","VcrVcc04"]:
            if self.tester.plutoGateway.read_ch(ch) != 0:
                self.log("Pluto modbus indicator for %s is not off."%ch)
                return False


        self.log("Success message")
        return True

# After boot
class testz100(Test):
    def __init__(self,tester,id):
        Test.__init__(self,tester,id)
        self.name = "Write to Read Pluto"
        self.desc = "Test write and rbv Pluto adds"

    def test(self):
        self.log(self.desc)

        plutoGateway = self.tester.plutoGateway.dict

        for ch in plutoGateway.keys():

            if plutoGateway[ch].permissions == "RW":
                print (ch)
                print(plutoGateway[ch])

                ch_rbv = ch.replace("_w","")
                sleep=0.2

                self.log("Testing %s (%s) and %s (%s)."%(ch,"%d:%d.%d"%(plutoGateway[ch].unitId,plutoGateway[ch].addr,plutoGateway[ch].bit),ch_rbv,"%d:%d.%d"%(plutoGateway[ch_rbv].unitId,plutoGateway[ch_rbv].addr,plutoGateway[ch_rbv].bit)))


                original_write = self.tester.plutoGateway.read_ch(ch)
                read = self.tester.plutoGateway.read_ch( ch_rbv)
                if original_write != read:
                    self.log("Failed on %s (%s) and %s (%s)." % (ch, "%d:%d.%d" % (plutoGateway[ch].unitId, plutoGateway[ch].addr, plutoGateway[ch].bit), ch_rbv,
                                                               "%d:%d.%d" % (plutoGateway[ch_rbv].unitId, plutoGateway[ch_rbv].addr, plutoGateway[ch_rbv].bit)))
                    return False

                write = 1
                self.tester.plutoGateway.write_ch( ch,write)
                self.sleep(sleep)
                read = self.tester.plutoGateway.read_ch( ch_rbv)
                if write != read:
                    self.log("Failed on %s (%s) and %s (%s)." % (ch, "%d:%d.%d" % (plutoGateway[ch].unitId, plutoGateway[ch].addr, plutoGateway[ch].bit), ch_rbv,
                                                               "%d:%d.%d" % (plutoGateway[ch_rbv].unitId, plutoGateway[ch_rbv].addr, plutoGateway[ch_rbv].bit)))
                    return False

                write = 0
                self.tester.plutoGateway.write_ch( ch,write)
                self.sleep(sleep)
                read = self.tester.plutoGateway.read_ch( ch_rbv)
                if write != read:
                    self.log("Failed on %s (%s) and %s (%s)." % (ch, "%d:%d.%d" % (plutoGateway[ch].unitId, plutoGateway[ch].addr, plutoGateway[ch].bit), ch_rbv,
                                                               "%d:%d.%d" % (plutoGateway[ch_rbv].unitId, plutoGateway[ch_rbv].addr, plutoGateway[ch_rbv].bit)))
                    return False

                write = 1
                self.tester.plutoGateway.write_ch( ch,write)
                self.sleep(sleep)
                read = self.tester.plutoGateway.read_ch( ch_rbv)
                if write != read:
                    self.log("Failed on %s (%s) and %s (%s)." % (ch, "%d:%d.%d" % (plutoGateway[ch].unitId, plutoGateway[ch].addr, plutoGateway[ch].bit), ch_rbv,
                                                               "%d:%d.%d" % (plutoGateway[ch_rbv].unitId, plutoGateway[ch_rbv].addr, plutoGateway[ch_rbv].bit)))
                    return False

                write = original_write
                self.tester.plutoGateway.write_ch( ch,write)
                self.sleep(sleep)
                read = self.tester.plutoGateway.read_ch( ch_rbv)
                if write != read:
                    self.log("Failed on %s (%s) and %s (%s)." % (ch, "%d:%d.%d" % (plutoGateway[ch].unitId, plutoGateway[ch].addr, plutoGateway[ch].bit), ch_rbv,
                                                               "%d:%d.%d" % (plutoGateway[ch_rbv].unitId, plutoGateway[ch_rbv].addr, plutoGateway[ch_rbv].bit)))
                    return False



        self.log("All write adds are connected with the respective readback values addrs")
        return True