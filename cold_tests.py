from tester import Test
import random
import numpy as np



class TestPlutoGatewayConfig(Test):
    def __init__(self, tester, id):
        Test.__init__(self, tester, id)
        self.name = "TestPlutoGatewayConfig"
        self.expected_config = [0, 1, 0, 0, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 100, 0, 0, 0, 1]

        '''
# Activate Data to Pluto Area 0,1
plutoGateway.gateway_config_write_read(1,0b001)

# Data to Pluto Timeout = 0
plutoGateway.gateway_config_write_read(2,0)

# Additional Data Areas for PLC 0
plutoGateway.gateway_config_write_read(5,0x01)
plutoGateway.gateway_config_write_read(6,0x02)
plutoGateway.gateway_config_write_read(7,0x03)
plutoGateway.gateway_config_write_read(8,0x04)
plutoGateway.gateway_config_write_read(9,0x05)
plutoGateway.gateway_config_write_read(10,0x06)
plutoGateway.gateway_config_write_read(11,0x07)
plutoGateway.gateway_config_write_read(12,0x08)
plutoGateway.gateway_config_write_read(13,0x09)
plutoGateway.gateway_config_write_read(14,0x0A)
plutoGateway.gateway_config_write_read(15,0x0B)
plutoGateway.gateway_config_write_read(16,0x0C)
plutoGateway.gateway_config_write_read(17,0x0D)
plutoGateway.gateway_config_write_read(18,0x0E)
plutoGateway.gateway_config_write_read(19,0x0F)


# Data to Pluto Cycle time = 100 ms
plutoGateway.gateway_config_write_read(37,100)

# Gateway Node number = 0
plutoGateway.gateway_config_write_read(41,0x001)
        '''

        self.desc = "Check Pluto Gateway configuration registers. Expected:" + str(self.expected_config)

    def test(self):
        config = self.tester.plutoGateway.read_holding_registers(4, 0, 42)
        for i in range(len(self.expected_config)):
            if config[i] != self.expected_config[i]:
                self.step(("Pluto Gateway Config doesn't match expected values.  Config:\t\t%s  Expected config:%s" % (
                    str(config), str(self.expected_config))))
                return False
        self.step(("Pluto Gateway Config match expected values.Config:\t\t%s Expected config:%s" % (
        str(config), str(self.expected_config))))
        return True


class TestPlutoPLCsPresent(Test):
    def __init__(self, tester, id):
        Test.__init__(self, tester, id)
        self.name = "TestPlutoPLCsPresent"
        self.desc = "Check Pluto Gateway sees Pluto D45 as node 0."

    def test(self):
        good = True
        for n in [0]:
            plc = self.tester.plutoGateway.read_bit(36, 1, n)

            if plc == 0:
                self.step("Pluto Gateway doens't see PLC %d as node %d" % (n, n))
                good = False

        if not good:
            return False

        self.step(("Pluto Gateway sees Pluto D45 as node 0."))
        return True


'''class TestChannelsBootDefault(Test):
    def __init__(self, tester, id):
        Test.__init__(self, tester, id)
        self.name = "TestChannelsBootDefault"
        self.desc = "Check if all IOs are as expected when the PLC is powered"

    def test(self):
        self.step(self.desc)

        self.step("Checking PLC IO boot default values.")

        self.setDefault(gateway=False,check=False)

        chs = []
        for ch in self.tester.testBox.plc.channels:
            if ch.boot_value != "":
                chs.append((ch, ch.boot_value))

        try:
            if self.checkChannels(chs):
                self.step("Boot IOs values Ok.")
                return True
        except:
            pass

        self.step("PLC Boot IOs values do not match defaults.")
        return False'''


class TestPlutoWriteReadback(Test):
    def __init__(self, tester, id):
        Test.__init__(self, tester, id)
        self.name = "TestePlutoWriteReadback"
        self.desc = "Test write and rbv Pluto addresses"

    def test(self):
        self.step(self.desc)

        plutoGateway = self.tester.plutoGateway.dict

        for ch in plutoGateway.keys():

            if plutoGateway[ch]["permissions"] == "RW":

                ch_rbv = ch.replace("_w", "")
                sleep = 0.2

                self.step("Testing %s (%s) and %s (%s)." % (
                ch, "%s:%s.%s" % (plutoGateway[ch]["unit_id"], plutoGateway[ch]["addr"], plutoGateway[ch]["bit"]),
                ch_rbv, "%s:%s.%s" % (
                plutoGateway[ch_rbv]["unit_id"], plutoGateway[ch_rbv]["addr"], plutoGateway[ch_rbv]["bit"])))

                original_write = self.tester.plutoGateway.read_ch(ch)
                read = self.tester.plutoGateway.read_ch(ch_rbv)
                if original_write != read:
                    self.step("Failed on %s (%s) and %s (%s)." % (
                        ch,
                        "%s:%s.%s" % (plutoGateway[ch]["unit_id"], plutoGateway[ch]["addr"], plutoGateway[ch]["bit"]),
                        ch_rbv, "%s:%s.%s" % (
                            plutoGateway[ch_rbv]["unit_id"], plutoGateway[ch_rbv]["addr"],
                            plutoGateway[ch_rbv]["bit"])))
                    return False

                write = 1
                self.tester.plutoGateway.write_ch(ch, write)
                self.sleep(sleep)
                read = self.tester.plutoGateway.read_ch(ch_rbv)
                if write != read:
                    self.step("Failed on %s (%s) and %s (%s)." % (
                        ch,
                        "%s:%s.%s" % (plutoGateway[ch]["unit_id"], plutoGateway[ch]["addr"], plutoGateway[ch]["bit"]),
                        ch_rbv, "%s:%s.%s" % (
                            plutoGateway[ch_rbv]["unit_id"], plutoGateway[ch_rbv]["addr"],
                            plutoGateway[ch_rbv]["bit"])))
                    return False

                write = 0
                self.tester.plutoGateway.write_ch(ch, write)
                self.sleep(sleep)
                read = self.tester.plutoGateway.read_ch(ch_rbv)
                if write != read:
                    self.step("Failed on %s (%s) and %s (%s)." % (
                        ch,
                        "%s:%s.%s" % (plutoGateway[ch]["unit_id"], plutoGateway[ch]["addr"], plutoGateway[ch]["bit"]),
                        ch_rbv, "%s:%s.%s" % (
                            plutoGateway[ch_rbv]["unit_id"], plutoGateway[ch_rbv]["addr"],
                            plutoGateway[ch_rbv]["bit"])))
                    return False

                write = 1
                self.tester.plutoGateway.write_ch(ch, write)
                self.sleep(sleep)
                read = self.tester.plutoGateway.read_ch(ch_rbv)
                if write != read:
                    self.step("Failed on %s (%s) and %s (%s)." % (
                        ch,
                        "%s:%s.%s" % (plutoGateway[ch]["unit_id"], plutoGateway[ch]["addr"], plutoGateway[ch]["bit"]),
                        ch_rbv, "%s:%s.%s" % (
                            plutoGateway[ch_rbv]["unit_id"], plutoGateway[ch_rbv]["addr"],
                            plutoGateway[ch_rbv]["bit"])))
                    return False

                write = original_write
                self.tester.plutoGateway.write_ch(ch, write)
                self.sleep(sleep)
                read = self.tester.plutoGateway.read_ch(ch_rbv)
                if write != read:
                    self.step("Failed on %s (%s) and %s (%s)." % (
                        ch,
                        "%s:%s.%s" % (plutoGateway[ch]["unit_id"], plutoGateway[ch]["addr"], plutoGateway[ch]["bit"]),
                        ch_rbv, "%s:%s.%s" % (
                            plutoGateway[ch_rbv]["unit_id"], plutoGateway[ch_rbv]["addr"],
                            plutoGateway[ch_rbv]["bit"])))
                    return False

        self.step("All write adds are connected with the respective readback values addrs")
        return True


'''class TestAnalogScaling(Test):
    def __init__(self, tester, id):
        Test.__init__(self, tester, id)
        self.name = "TestAnalogScaling"
        self.desc = "Checks the analog input wiring, linearity and scaling factors and offsets"

        # [P2_IA0,P2_IA1,P2_IA2,P2_IA3,P3_IA0,P3_IA1,P3_IA2,P3_IA3]

        ma4 = 120
        ma20 = 320

        slope = (ma4 - ma20) / (4 - 20)
        offset = ma4 - slope * 4

        self.expected_factors = [slope] * 8
        self.expected_offsets = [offset] * 8

        self.n_points = 10

    def test(self):
        self.step(self.desc)
        self.step("Scaning...")

        test = dict()

        for n, port in enumerate(["P2_IA0", "P2_IA1", "P2_IA2", "P2_IA3", "P3_IA0", "P3_IA1", "P3_IA2", "P3_IA3"]):
            self.tester.testBox.write_port("plc", port, 0)
        self.sleep(2)

        for n, port in enumerate(["P2_IA0", "P2_IA1", "P2_IA2", "P2_IA3", "P3_IA0", "P3_IA1", "P3_IA2", "P3_IA3"]):

            test[port] = dict()
            test[port]["step"] = random.uniform(1.6, 4.6)
            test[port]["value"] = 0
            test[port]["value_array"] = []
            test[port]["finished"] = False

            for md in self.tester.testBox.dict[port]["modbus"]:
                if md.find("Current") > 0:
                    test[port]["channel_current"] = md
                    test[port]["channel_current_array"] = []
                elif md.find("Valid") > 0:
                    test[port]["channel_valid"] = md
                    test[port]["channel_valid_array"] = []
                else:
                    test[port]["channel_scaled"] = md
                    test[port]["channel_scaled_array"] = []

        cont = True
        while cont:
            cont = False
            for port in test.keys():
                if test[port]["value"] < 21:

                    current = test[port]["value"] + test[port]["step"]
                    if current > 21:
                        current = 21
                    self.tester.testBox.write_port("plc", port, current)
                    test[port]["value"] = current
                    test[port]["value_array"].append(current * 1000)
                else:
                    test[port]["finished"] = True

            self.sleep(.5)

            for port in test.keys():
                if test[port]["finished"] is not True:
                    test[port]["channel_current_array"].append(
                        self.tester.plutoGateway.read_ch(test[port]["channel_current"]))
                    test[port]["channel_scaled_array"].append(
                        self.tester.plutoGateway.read_ch(test[port]["channel_scaled"]))
                    test[port]["channel_valid_array"].append(
                        self.tester.plutoGateway.read_ch(test[port]["channel_valid"]))

                cont = cont | (test[port]["value"] < 21.0)

        from scipy import stats

        self.step("Evaluating Valid")
        for port in test.keys():
            if sum(test[port]["channel_valid_array"]) != len(test[port]["channel_valid_array"]):
                self.step("Channel %s read not valid" % port)
                return False

        self.step("Evaluating Correct wiring")
        for port in test.keys():
            y = test[port]["value_array"]
            x = range(len(test[port]["channel_current_array"]))
            values = stats.linregress(x, y)

            y = test[port]["channel_current_array"]
            x = range(len(test[port]["channel_current_array"]))
            current = stats.linregress(x, y)

            if values.rvalue < 0.98 or current.rvalue < 0.98:
                self.step("R-square too high on %s" % port)
                return False

            if abs(values.slope - current.slope) > (values.slope + current.slope) / 2 * 0.02:
                self.step(
                    "Slope (over time) discrepancy between input and read value on %s. Probably wrong wiring." % port)
                return False

            if abs(values.intercept - current.intercept) > test[port]["value_array"][-1] * 0.01:
                self.step(
                    "Intercept  (over time) discrepancy between input and read value on %s. Probably wrong wiring." % port)
                return False

        self.step("Evaluating current linearity")
        for port in test.keys():
            y = test[port]["channel_current_array"]
            x = test[port]["value_array"]
            values = stats.linregress(x, y)

            if values.rvalue < 0.98:
                self.step("R-square too high on %s" % port)
                return False

            if abs(values.slope - 1) > 0.02:
                self.step("Transfer function Slope not 1 +- 2%% on %s." % port)
                return False

            if abs(values.intercept) > 20000 * 0.01:
                self.step("Transfer function Intercept not 0 +- 1%% (20 mA)on %s." % port)
                return False

        self.step("Evaluating scaling coeficients")
        for port in test.keys():
            y = test[port]["channel_scaled_array"]
            x = test[port]["channel_current_array"]
            values = stats.linregress(x, y)

            print(values, m, b)

            if values.rvalue < 0.98:
                print('dddd')
                self.step("R-square too high on %s" % port)
                return False

            if abs(values.slope - m / 1000) > m * 1000 * 0.01:
                print('dddd2')
                self.step("Scaling function Slope not %.2d +- 1%% on %s." % m, port)
                return False

            if abs(values.intercept - b / 1000) > b * 1000 * 0.1:
                print('dddd3')
                self.step("Scaling function Intercept not %.2d +- 1%% on %s." % b, port)
                return False

        self.step("Analog input wiring, linearity and scaling factors and offsets OK")
        return True'''



'''class TestTemperaturePressuresSetpoints(Test):
    def __init__(self, tester, id):
        Test.__init__(self, tester, id)
        self.name = "TestTemperatureSetpoints"
        self.desc = "Test PLC reaction to temperature and Pressure Setpoints"

    def test(self):
        self.step(self.desc)

        tmpPorts = [self.tester.testBox.plc.P2_IA0, self.tester.testBox.plc.P2_IA1, self.tester.testBox.plc.P2_IA2,
                    self.tester.testBox.plc.P2_IA3, self.tester.testBox.plc.P3_IA0, self.tester.testBox.plc.P3_IA1,
                    self.tester.testBox.plc.P3_IA2, self.tester.testBox.plc.P3_IA3]

        tmpCurrents = [self.tester.plutoGateway.P2_ClpRtd0Current, self.tester.plutoGateway.P2_ClpRtd1Current,
                       self.tester.plutoGateway.P2_ClpRtd2Current, self.tester.plutoGateway.P2_ClpRtd3Current,
                       self.tester.plutoGateway.P3_CryRtd0Current, self.tester.plutoGateway.P3_CryRtd1Current,
                       self.tester.plutoGateway.P3_CryRtd2Current, self.tester.plutoGateway.P3_CryRtd3Current]

        tmpTemps = [self.tester.plutoGateway.P2_ClpRtd0Temp, self.tester.plutoGateway.P2_ClpRtd1Temp,
                    self.tester.plutoGateway.P2_ClpRtd2Temp, self.tester.plutoGateway.P2_ClpRtd3Temp,
                    self.tester.plutoGateway.P3_CryRtd0Temp, self.tester.plutoGateway.P3_CryRtd1Temp,
                    self.tester.plutoGateway.P3_CryRtd2Temp, self.tester.plutoGateway.P3_CryRtd3Temp]

        tmpsNotLows = [self.tester.plutoGateway.P2_ClpTemp0NotLow, self.tester.plutoGateway.P2_ClpTemp1NotLow,
                       self.tester.plutoGateway.P2_ClpTemp2NotLow, self.tester.plutoGateway.P2_ClpTemp3NotLow,
                       self.tester.plutoGateway.P3_CryTemp0NotLow, self.tester.plutoGateway.P3_CryTemp1NotLow,
                       self.tester.plutoGateway.P3_CryTemp2NotLow, self.tester.plutoGateway.P3_CryTemp3NotLow]

        tmpNotHighs = [self.tester.plutoGateway.P2_ClpTemp0NotHigh, self.tester.plutoGateway.P2_ClpTemp1NotHigh,
                       self.tester.plutoGateway.P2_ClpTemp2NotHigh, self.tester.plutoGateway.P2_ClpTemp3NotHigh,
                       self.tester.plutoGateway.P3_CryTemp0NotHigh, self.tester.plutoGateway.P3_CryTemp1NotHigh,
                       self.tester.plutoGateway.P3_CryTemp2NotHigh, self.tester.plutoGateway.P3_CryTemp3NotHigh]

        coldhighLimitCurr = KtoC(295)
        coldlowLimitCurr = KtoC(228)

        cryhighLimitCurr = KtoC(270)
        crydlowLimitCurr = KtoC(130)

        highLimitCurrs = [coldhighLimitCurr, coldhighLimitCurr, coldhighLimitCurr, coldhighLimitCurr, cryhighLimitCurr,
                          cryhighLimitCurr, cryhighLimitCurr, cryhighLimitCurr]
        lowLimitCurrs = [coldlowLimitCurr, coldlowLimitCurr, coldlowLimitCurr, coldlowLimitCurr, crydlowLimitCurr,
                         crydlowLimitCurr, crydlowLimitCurr, crydlowLimitCurr]

        zeroLimitCurr = 3  # mA

        val = [x * 0.1 for x in range(25, 210, 5)]

        for n, v in enumerate(val):
            for ref in [coldhighLimitCurr, coldlowLimitCurr, cryhighLimitCurr, crydlowLimitCurr, zeroLimitCurr]:
                if abs(v - ref) < 0.05:
                    val[n] = val[n] * 1.1

        vals = []

        for n in range(len(tmpPorts)):
            vals.append(random.sample(val, len(val)))

        try:
            self.setDefault(gateway=True)
            for n in range(len(val)):
                self.step("{}/{}".format(n, len(val)))
                checks = []

                for i, port in enumerate(tmpPorts):
                    port.write(vals[i][n])

                    checks.append((port, vals[i][n]))
                    checks.append((tmpCurrents[i], vals[i][n] * 1000))
                    checks.append((tmpTemps[i], CtoK(vals[i][n])))

                    checks.append((tmpsNotLows[i], vals[i][n] > lowLimitCurrs[i]))
                    checks.append((tmpNotHighs[i], vals[i][n] < highLimitCurrs[i] and vals[i][n] > zeroLimitCurr))

                self.checkChange(checks, 1)

            self.step("Temperature Limits logic correct.")
            return True

        except Exception as e:
            self.step("TestTemperatureLimits logic failed! Failed at %s. Error: %s " % (self.step_m, str(e)))
            return False'''



P4mA = 0
P20mA = 500  #psi
Pm = (P20mA - P4mA) / (20 - 4)
Pb = P4mA - (4 * Pm)
def c2P(mA):
    psi = mA * Pm + Pb
    return psi
def P2c(psi):
    mA = (psi - Pb) / Pm
    mA = min(mA, 21.5)
    if mA < 3.5:
        mA = 21.5
    return mA

T2v = -50  #
T10v = 150  #C
Tm = (T10v - T2v) / (10 - 2)
Tb = T2v - (2 * Tm)

def v2C(v):
    C = v * Tm + Tb
    return C
def C2v(C):
    v = (C - Tb) / Tm
    v = min(v, 10.1)
    return v

CurT0v = 0  #A
Cur5v = 25  #A
Curm = (Cur5v - CurT0v) / (5 - 0)
Curb = CurT0v

def v2Cur(v):
    Cur = v * Curm + Curb
    return Cur
def Cur2v(Cur):
    v = (Cur - Curb) / Curm
    v = min(v, 10.1)
    return v


Volt0v = 0  #V
Volt5v = 250  #v
Voltm = (Volt5v - Volt0v) / (5 - 0)
Voltb = Volt0v

def v2Volt(v):
    Volt = v * Voltm + Voltb
    return Volt
def Volt2v(Volt):
    v = (Volt - Voltb) / Voltm
    v = min(v, 10.1)
    return v



def setDefautls(test,reset=True):
        self=test
        self.tester.testBox.plc.cold_I31.write(1)
        self.tester.testBox.plc.cold_I32.write(1)
        self.tester.testBox.plc.cold_I34.write(1)

        self.tester.testBox.plc.cold_IA0.write(C2v(120))
        self.tester.testBox.plc.cold_IA1.write(C2v(-25))
        self.tester.testBox.plc.cold_IA2.write(C2v(40))

        self.tester.testBox.plc.cold_IA3.write(P2c(430))
        self.tester.testBox.plc.cold_IA4.write(P2c(430))

        self.tester.testBox.plc.cold_IA7.write(Cur2v(2))
        self.tester.testBox.plc.cold_IA6.write(Volt2v(230))


        self.tester.plutoGateway.CompIntPerm_w.write(1)
        self.tester.plutoGateway.LightsOn_w.write(1)

        if reset:
            self.tester.testBox.plc.cold_I33.write(1)
            self.tester.plutoGateway.ResetGate_w.write(1)
            self.sleep(0.5)
            self.tester.testBox.plc.cold_I33.write(0)
            self.tester.plutoGateway.ResetGate_w.write(0)

            self.tester.testBox.plc.cold_I33.write(1)
            self.tester.plutoGateway.ResetGate_w.write(1)
            self.sleep(0.5)
            self.tester.testBox.plc.cold_I33.write(0)
            self.tester.plutoGateway.ResetGate_w.write(0)


def checkDefautls(test):
    pass





class TestDigitalInputs(Test):
    def __init__(self, tester, id):
        Test.__init__(self, tester, id)
        self.name = "TestDigitalInputs"
        self.desc = "TestDigitalInputs"

    def test(self):
        self.step(self.desc)

        setDefautls(self)
        reset = self.tester.testBox.plc.cold_I33
        soft_reset = self.tester.plutoGateway.ResetGate_w
        permit = self.tester.testBox.plc.cold_Q0
        resetModes = [True,False]

        ports = [self.tester.testBox.plc.cold_I31,self.tester.testBox.plc.cold_I34]
        lacthOK =[self.tester.plutoGateway.ExtPermLatch,self.tester.plutoGateway.SmokeOKLatch]
        lacthStatus = [self.tester.plutoGateway.ExtPermLatchStatus,self.tester.plutoGateway.SmokeOKLatchStatus]
        latchStatusNeedsReset =[self.tester.plutoGateway.ExtPermLatchNeedsReset,self.tester.plutoGateway.SmokeOKLatchNeedsReset]

        self.tester.testBox.plc.cold_IA0v.write(0)
        self.tester.testBox.plc.cold_IA1v.write(0)
        self.tester.testBox.plc.cold_IA2v.write(0)
        self.tester.testBox.plc.cold_IA6v.write(0)
        self.tester.testBox.plc.cold_IA7v.write(0)


        try:

            for resetMode in resetModes:
                for i, port in enumerate(ports):

                    port.write(0)

                    self.sleep(0.5)

                    self.pressChannels([reset])

                    self.checkChange([(port, 0),
                                      (permit, 0),
                                      (lacthOK[i],0),
                                      (lacthStatus[i],1),
                                      (latchStatusNeedsReset[i],0)
                                      ],
                                     3)


                    port.write(1)

                    self.checkChange([(port, 1),
                                      (permit, 0),
                                      (lacthOK[i],0),
                                      (lacthStatus[i],2),
                                      (latchStatusNeedsReset[i],1)
                                      ],
                                     3)

                    if resetMode:
                        self.pressChannels([reset])
                    else:
                        self.pressChannels([soft_reset])

                    checkDefautls(self)

        except Exception as e:
            self.step("fail." + str(e))
            return False

        ports = [self.tester.testBox.plc.cold_I32]  # ,self.tester.plutoGateway.CompIntPerm]

        try:

            for i, port in enumerate(ports):

                port.write(0)

                self.sleep(0.5)

                self.pressChannels([reset,soft_reset])

                self.checkChange([(port, 0),
                                  (permit, 0),
                                  ],
                                 3)

                port.write(1)
                checkDefautls(self)


        except Exception as e:
            self.step("TestDigitalInputs failed." + str(e))
            return False


        return True


class TestSensorsValid(Test):
    def __init__(self, tester, id):
        Test.__init__(self, tester, id)
        self.name = "TestSensorsValid"
        self.desc = "TestSensorsValid"

    def test(self):
        self.step(self.desc)

        setDefautls(self)

        reset = self.tester.testBox.plc.cold_I33
        soft_reset = self.tester.plutoGateway.ResetGate_w
        permit = self.tester.testBox.plc.cold_Q0
        resetMode = True

        sensorValidLatch = self.tester.plutoGateway.SensorsValidLatch
        sensorValidLatchStatus = self.tester.plutoGateway.SensorsValidLatchStatus
        sensorValidLatchNeedsReset = self.tester.plutoGateway.SensorsValidLatchNeedsReset

        ports =  [self.tester.testBox.plc.cold_IA0,self.tester.testBox.plc.cold_IA1,self.tester.testBox.plc.cold_IA2,self.tester.testBox.plc.cold_IA3,self.tester.testBox.plc.cold_IA6]
        invalidVals=[1,1,1,1,0]
        valids = [self.tester.plutoGateway.DisTempValid,self.tester.plutoGateway.SucTempValid,self.tester.plutoGateway.LiqTempValid,self.tester.plutoGateway.DisPressValid,self.tester.plutoGateway.VoltageValid]
        #notvalids = [self.tester.testBox.plc.cold_IA0v,self.tester.testBox.plc.cold_IA1v,self.tester.testBox.plc.cold_IA2v,None,self.tester.testBox.plc.cold_IA6v]

        lacthOK =[self.tester.plutoGateway.DisTempOKLatch,self.tester.plutoGateway.SucTempOKLatch,self.tester.plutoGateway.LiqTempOKLatch,self.tester.plutoGateway.DisPressOKLatch,self.tester.plutoGateway.PowerOKLatch]
        lacthStatus = [self.tester.plutoGateway.DisTempOKLatchStatus,self.tester.plutoGateway.SucTempOKLatchStatus,self.tester.plutoGateway.LiqTempOKLatchStatus,self.tester.plutoGateway.DisPressOKLatchStatus,self.tester.plutoGateway.PowerOKLatchStatus]
        latchStatusNeedsReset =[self.tester.plutoGateway.DisTempOKLatchNeedsReset,self.tester.plutoGateway.SucTempOKLatchNeedsReset,self.tester.plutoGateway.LiqTempOKLatchNeedsReset,self.tester.plutoGateway.DisPressOKLatchNeedsReset,self.tester.plutoGateway.PowerOKLatchNeedsReset]

        try:
            for i, port in enumerate(ports):

                port.write(invalidVals[i])

                self.pressChannels([reset,soft_reset])

                self.checkChange([(port, invalidVals[i]),
                                  (valids[i],0),
                                  (permit, 0),
                                  (sensorValidLatch,0),
                                  (sensorValidLatchStatus,1),
                                  (sensorValidLatchNeedsReset, 0),
                                  (lacthOK[i],0),
                                  (lacthStatus[i], 1),
                                  (latchStatusNeedsReset[i], 0),
                                  ],
                                 3)

                setDefautls(self,reset=False)

                self.checkChange([(port, invalidVals[i]),
                                  (valids[i],1),
                                  (permit, 0),
                                  (sensorValidLatch,0),
                                  (sensorValidLatchStatus,2),
                                  (sensorValidLatchNeedsReset, 1),
                                  (lacthOK[i],0),
                                  (lacthStatus[i], 2),
                                  (latchStatusNeedsReset[i], 1),
                                  ],
                                 3)

                if resetMode:
                    self.pressChannels([reset])
                else:
                    self.pressChannels([soft_reset])
                resetMode = not resetMode

                checkDefautls(self)

                continue #TODO

                if notvalids[i] is None:
                    continue

                notvalids[i].write(1)

                self.pressChannels([reset,soft_reset])

                self.checkChange([(port, invalidVals[i]),
                                  (valids[i],0),
                                  (permit, 0),
                                  (sensorValidLatch,0),
                                  (sensorValidLatchStatus,1),
                                  (sensorValidLatchNeedsReset, 0),
                                  (lacthOK[i],0),
                                  (lacthStatus[i], 1),
                                  (latchStatusNeedsReset[i], 0),
                                  ],
                                 3)

                notvalids[i].write(0)

                self.checkChange([(port, invalidVals[i]),
                                  (valids[i],1),
                                  (permit, 0),
                                  (sensorValidLatch,0),
                                  (sensorValidLatchStatus,2),
                                  (sensorValidLatchNeedsReset,1),
                                  (lacthOK[i],0),
                                  (lacthStatus[i], 2),
                                  (latchStatusNeedsReset[i], 1),
                                  ],
                                 3)

                if resetMode:
                    self.pressChannels([reset])
                else:
                    self.pressChannels([soft_reset])
                resetMode=not resetMode

                checkDefautls(self)

        except Exception as e:
            self.step("TestDigitalInputs failed." + str(e))
            return False

        return True


class TestImmediateTrips(Test):
    def __init__(self, tester, id):
        Test.__init__(self, tester, id)
        self.name = "TestImmediateTrips"
        self.desc = "TestImmediateTrips"

    def test(self):
        self.step(self.desc)

        setDefautls(self)

        reset = self.tester.testBox.plc.cold_I33
        soft_reset = self.tester.plutoGateway.ResetGate_w
        permit = self.tester.testBox.plc.cold_Q0
        resetMode = True


        try:

            port = self.tester.testBox.plc.cold_IA0
            valid = self.tester.plutoGateway.DisTempValid
            warn = self.tester.plutoGateway.DisTempWarn
            lacthOK = self.tester.plutoGateway.DisTempOKLatch
            lacthStatus = self.tester.plutoGateway.DisTempOKLatchStatus
            latchStatusNeedsReset =  self.tester.plutoGateway.DisTempOKLatchNeedsReset
            temp = self.tester.plutoGateway.DisTemp

            vals = np.arange(1.6, 10, 0.3)

            for val in vals:
                if abs(v2C(val) - 130)<0.5 or abs(v2C(val) - 125)<0.5 or abs(v2C(val))<10:
                    continue

                port.write(val)

                print(v2C(val)*100)

                tempVal = int(v2C(val)*100)
                if tempVal<0:
                    tempVal = 65535+tempVal

                print(tempVal)

                trip = val > C2v(130)
                warning = val > C2v(125)

                self.pressChannels([reset, soft_reset])

                self.checkChange([(port, val),
                                  (valid, True),
                                  (permit, not trip),
                                  (warn, warning),
                                  (lacthOK,not trip),
                                  (lacthStatus, trip),
                                  (latchStatusNeedsReset, 0),
                                  (temp, tempVal)],3)

                if trip:
                    setDefautls(self, reset=False)
                    self.checkChange([(permit, not trip),
                                      (warn, 0),
                                      (lacthOK, 0),
                                      (lacthStatus, 2),
                                      (latchStatusNeedsReset, 1),
                                      ], 3)
                    if resetMode:
                        self.pressChannels([reset])
                    else:
                        self.pressChannels([soft_reset])
                    resetMode = not resetMode


            # discharge pressure is OK (<=465 psia AND, <=440 psia(wait 10 min))

            port = self.tester.testBox.plc.cold_IA3
            valid = self.tester.plutoGateway.DisPressValid
            warn = self.tester.plutoGateway.DisPressWarn
            lacthOK = self.tester.plutoGateway.DisPressOKLatch
            lacthStatus = self.tester.plutoGateway.DisPressOKLatchStatus
            latchStatusNeedsReset = self.tester.plutoGateway.DisPressOKLatchNeedsReset
            press = self.tester.plutoGateway.DisPress

            vals = np.arange(4, 20, 0.6)

            for val in vals:
                if abs(c2P(val) - 465) < 0.5 or abs(c2P(val) - 440) < 0.5 or abs(c2P(val)) < 100:
                    continue

                port.write(val)

                print(c2P(val) * 10)

                pressVal = int(c2P(val) * 10)
                if pressVal < 0:
                    pressVal = 65535 + pressVal

                print(pressVal)

                trip = val >= P2c(465)
                warning = val >= P2c(440)

                self.pressChannels([reset, soft_reset])

                self.checkChange([(port, val),
                                  (valid, True),
                                  (permit, not trip),
                                  (warn, warning),
                                  (lacthOK, not trip),
                                  (lacthStatus, trip),
                                  (latchStatusNeedsReset, 0),
                                  (press, pressVal)], 3)

                if trip:
                    setDefautls(self, reset=False)
                    self.checkChange([(permit, not trip),
                                      (warn, 0),
                                      (lacthOK, 0),
                                      (lacthStatus, 2),
                                      (latchStatusNeedsReset, 1),
                                      ], 3)
                    if resetMode:
                        self.pressChannels([reset])
                    else:
                        self.pressChannels([soft_reset])
                    resetMode = not resetMode

            #the suction temperature is OK (>-30C)

            port = self.tester.testBox.plc.cold_IA1
            valid = self.tester.plutoGateway.SucTempValid
            lacthOK = self.tester.plutoGateway.SucTempOKLatch
            lacthStatus = self.tester.plutoGateway.SucTempOKLatchStatus
            latchStatusNeedsReset =  self.tester.plutoGateway.SucTempOKLatchNeedsReset
            temp = self.tester.plutoGateway.SucTemp

            vals = np.arange(1.6, 10, 0.3)


            for val in vals:
                if abs(v2C(val) +30)<0.5 or abs(v2C(val))<10:
                    continue

                port.write(val)

                print(v2C(val)*100)

                tempVal = int(v2C(val)*100)
                if tempVal<0:
                    tempVal = 65535+tempVal

                print(tempVal)

                trip = v2C(val) <-30
                print(trip)

                self.pressChannels([reset, soft_reset])

                self.checkChange([(port, val),
                                  (valid, True),
                                  (permit, not trip),
                                  (lacthOK,not trip),
                                  (lacthStatus, trip),
                                  (latchStatusNeedsReset, 0),
                                  (temp, tempVal)],3)

                if trip:
                    setDefautls(self, reset=False)
                    self.checkChange([(permit, not trip),
                                      (warn, 0),
                                      (lacthOK, 0),
                                      (lacthStatus, 2),
                                      (latchStatusNeedsReset, 1),
                                      ], 3)
                    if resetMode:
                        self.pressChannels([reset])
                    else:
                        self.pressChannels([soft_reset])
                    resetMode = not resetMode




            #the liquid line temperature is OK (<45C)

            port = self.tester.testBox.plc.cold_IA2
            valid = self.tester.plutoGateway.LiqTempValid
            lacthOK = self.tester.plutoGateway.LiqTempOKLatch
            lacthStatus = self.tester.plutoGateway.LiqTempOKLatchStatus
            latchStatusNeedsReset = self.tester.plutoGateway.LiqTempOKLatchNeedsReset
            temp = self.tester.plutoGateway.LiqTemp

            vals = np.arange(1.6, 10, 0.3)

            for val in vals:
                if abs(v2C(val) -45) < 0.5 or abs(v2C(val)) < 10:
                    continue

                port.write(val)

                print(v2C(val) * 100)

                tempVal = int(v2C(val) * 100)
                if tempVal < 0:
                    tempVal = 65535 + tempVal

                print(tempVal)

                trip = v2C(val) > 45
                print(trip)

                self.pressChannels([reset, soft_reset])

                self.checkChange([(port, val),
                                  (valid, True),
                                  (permit, not trip),
                                  (lacthOK, not trip),
                                  (lacthStatus, trip),
                                  (latchStatusNeedsReset, 0),
                                  (temp, tempVal)], 3)

                if trip:
                    setDefautls(self, reset=False)
                    self.checkChange([(permit, not trip),
                                      (warn, 0),
                                      (lacthOK, 0),
                                      (lacthStatus, 2),
                                      (latchStatusNeedsReset, 1),
                                      ], 3)
                    if resetMode:
                        self.pressChannels([reset])
                    else:
                        self.pressChannels([soft_reset])
                    resetMode = not resetMode


        except Exception as e:
            self.step("TestImmediateTrips failed." + str(e))
            return False

        return True

class TestImmediatePowerTrips(Test):
    def __init__(self, tester, id):
        Test.__init__(self, tester, id)
        self.name = "TestImmediatePowerTrips"
        self.desc = "TestImmediatePowerTrips"

    def test(self):
        self.step(self.desc)

        setDefautls(self)

        reset = self.tester.testBox.plc.cold_I33
        soft_reset = self.tester.plutoGateway.ResetGate_w
        permit = self.tester.testBox.plc.cold_Q0
        resetMode = True

        try:

            #the compressor power is OK - (<2500 VA AND <1800 (wait 5 min))

            port = self.tester.testBox.plc.cold_IA6
            valid = self.tester.plutoGateway.VoltageValid
            warn = self.tester.plutoGateway.PowerBadWarn
            lacthOK = self.tester.plutoGateway.PowerOKLatch
            lacthStatus = self.tester.plutoGateway.PowerOKLatchStatus
            latchStatusNeedsReset =  self.tester.plutoGateway.PowerOKLatchNeedsReset
            voltage = self.tester.plutoGateway.Voltage

            vals = np.arange(1, 10, 0.6)


            port2 = self.tester.testBox.plc.cold_IA7
            valid2 = self.tester.plutoGateway.CurrentValid

            curent = self.tester.plutoGateway.Current

            vals2 = np.arange(1, 10, 0.7)




            for val in vals:
                for val2 in vals2:

                    print(v2Volt(val), 'V')
                    print(v2Cur(val2), 'A')

                    print(3 * v2Volt(val) * v2Cur(val2))

                    if abs(3 * v2Volt(val) * v2Cur(val2) - 2500) < 60 or abs(3 * v2Volt(val) * v2Cur(val2) - 1800) < 60:
                        continue


                    port.write(val)
                    port2.write(val2)

                    trip = 3 * v2Volt(val) * v2Cur(val2) > 2500
                    warning = 3 * v2Volt(val) * v2Cur(val2) > 1800

                    self.pressChannels([reset, soft_reset])

                    self.checkChange([(port, val),
                                      (port2, val2),
                                      (valid, True),
                                      (valid2, True),

                                      (permit, not trip),
                                      (warn, warning),
                                      (lacthOK,not trip),
                                      (lacthStatus, trip),
                                      (latchStatusNeedsReset, 0),
                                      (voltage, v2Volt(val)*10),
                                      (curent, v2Cur(val2)*100)
                                      ],3)

                    if trip:
                        setDefautls(self,reset=False)

                        self.checkChange([(permit, not trip),
                                          (warn, 0),
                                          (lacthOK, 0),
                                          (lacthStatus, 2),
                                          (latchStatusNeedsReset, 1),
                                          ], 3)

                        if resetMode:
                            self.pressChannels([reset])
                        else:
                            self.pressChannels([soft_reset])
                        resetMode = not resetMode





        except Exception as e:
            self.step("TestImmediateTrips failed." + str(e))
            return False

        return True


class TestDelay0(Test):
    def __init__(self, tester, id):
        Test.__init__(self, tester, id)
        self.name = "TestDelay0"
        self.desc = "TestDelay0"

    def test(self):
        self.step(self.desc)

        setDefautls(self)

        reset = self.tester.testBox.plc.cold_I33
        soft_reset = self.tester.plutoGateway.ResetGate_w
        permit = self.tester.testBox.plc.cold_Q0
        resetMode = True

        sensorValidLatch = self.tester.plutoGateway.SensorsValidLatch
        sensorValidLatchStatus = self.tester.plutoGateway.SensorsValidLatchStatus
        sensorValidLatchNeedsReset = self.tester.plutoGateway.SensorsValidLatchNeedsReset

        try:

            setDefautls(self)
            self.sleep(1)

            self.tester.testBox.plc.cold_IA7.write(0)

            self.checkDuring([(permit, 1),(sensorValidLatch,1)], 133 + 15)
            print("passou o tempo")


            self.checkChange([(permit, 0),
                              (sensorValidLatch,0),
                              (sensorValidLatchStatus,1),
                              (sensorValidLatchNeedsReset, 0),
                              (self.tester.plutoGateway.PowerOKLatch,0),
                              (self.tester.plutoGateway.PowerOKLatchStatus, 1),
                              (self.tester.plutoGateway.PowerOKLatchNeedsReset, 0),
                              ],
                             30)

            setDefautls(self,reset=False)

            self.checkChange([(permit, 0),
                              (sensorValidLatch,0),
                              (sensorValidLatchStatus,2),
                              (sensorValidLatchNeedsReset, 1),
                              (self.tester.plutoGateway.PowerOKLatch,0),
                              (self.tester.plutoGateway.PowerOKLatchStatus, 2),
                              (self.tester.plutoGateway.PowerOKLatchNeedsReset, 1),
                              ],
                             3)

            if resetMode:
                self.pressChannels([reset])
            else:
                self.pressChannels([soft_reset])
            resetMode = not resetMode

            checkDefautls(self)

            #no problem

            setDefautls(self)

            self.checkDuring([(permit, 1)], 133+20)

            print("passou o tempo")

            '''self.checkChange([(self.tester.plutoGateway.CurrentValid,1),
                              (permit, 1),
                              (sensorValidLatch,1),
                              (sensorValidLatchStatus,0),
                              (sensorValidLatchNeedsReset, 0),
                              (self.tester.plutoGateway.PowerOKLatch,1),
                              (self.tester.plutoGateway.PowerOKLatchStatus, 0),
                              (self.tester.plutoGateway.PowerOKLatchNeedsReset, 0),
                              ],
                             20)'''

            checkDefautls(self)




        except Exception as e:
            self.step("TestDigitalInputs failed." + str(e))
            return False

        return True

class TestDelay1(Test):
    def __init__(self, tester, id):
        Test.__init__(self, tester, id)
        self.name = "TestDelay1"
        self.desc = "TestDelay1"

    def test(self):
        self.step(self.desc)

        setDefautls(self)

        reset = self.tester.testBox.plc.cold_I33
        soft_reset = self.tester.plutoGateway.ResetGate_w
        permit = self.tester.testBox.plc.cold_Q0
        resetMode = True

        try:

            #the compressor power is OK - (<2500 VA AND <1800 (wait 5 min))

            port = self.tester.testBox.plc.cold_IA6
            valid = self.tester.plutoGateway.VoltageValid
            warn = self.tester.plutoGateway.PowerBadWarn
            lacthOK = self.tester.plutoGateway.PowerOKLatch
            lacthStatus = self.tester.plutoGateway.PowerOKLatchStatus
            latchStatusNeedsReset =  self.tester.plutoGateway.PowerOKLatchNeedsReset
            voltage = self.tester.plutoGateway.Voltage

            vals = [4.6]


            port2 = self.tester.testBox.plc.cold_IA7
            valid2 = self.tester.plutoGateway.CurrentValid

            curent = self.tester.plutoGateway.Current

            vals2 = [0.70]




            for val in vals:
                for val2 in vals2:

                    print(v2Volt(val), 'V')
                    print(v2Cur(val2), 'A')

                    print(3 * v2Volt(val) * v2Cur(val2))


                    port.write(val)
                    port2.write(val2)

                    trip = 3 * v2Volt(val) * v2Cur(val2) > 2500
                    warning = 3 * v2Volt(val) * v2Cur(val2) > 1800

                    self.pressChannels([reset, soft_reset])

                    self.checkChange([(port, val),
                                      (port2, val2),
                                      (valid, True),
                                      (valid2, True),

                                      (permit, not trip),
                                      (warn, warning),
                                      (lacthOK,not trip),
                                      (lacthStatus, trip),
                                      (latchStatusNeedsReset, 0),
                                      (voltage, v2Volt(val)*10),
                                      (curent, v2Cur(val2)*100)
                                      ],3)

                    self.checkDuring([(permit, 1), (lacthOK, 1)], 60*5-10)

                    self.checkChange([(port, val),
                                      (valid, True),
                                      (permit, not warning),
                                      (warn, 0),
                                      (lacthOK, not warning),
                                      (lacthStatus, warning),
                                      (latchStatusNeedsReset, 0),
                                      (voltage, v2Volt(val)*10),
                                      (curent, v2Cur(val2)*100)
                                      ], 30)

                    print('**********************************************************************************************')

                    if warning:
                        setDefautls(self,reset=False)

                        self.checkChange([(permit, 0),
                                          (warn, 0),
                                          (lacthOK, 0),
                                          (lacthStatus, 2),
                                          (latchStatusNeedsReset, 1)], 30)

                        if resetMode:
                            self.pressChannels([reset])
                        else:
                            self.pressChannels([soft_reset])
                        resetMode = not resetMode








        except Exception as e:
            self.step("TestImmediateTrips failed." + str(e))
            return False

        return True



class TestDelay2(Test):
    def __init__(self, tester, id):
        Test.__init__(self, tester, id)
        self.name = "TestDelay2"
        self.desc = "TestDelay2"

    def test(self):
        self.step(self.desc)

        setDefautls(self)

        reset = self.tester.testBox.plc.cold_I33
        soft_reset = self.tester.plutoGateway.ResetGate_w
        permit = self.tester.testBox.plc.cold_Q0
        resetMode = True


        try:


            # discharge pressure is OK (<=465 psia AND, <=440 psia(wait 10 min))

            port = self.tester.testBox.plc.cold_IA3
            valid = self.tester.plutoGateway.DisPressValid
            warn = self.tester.plutoGateway.DisPressWarn
            lacthOK = self.tester.plutoGateway.DisPressOKLatch
            lacthStatus = self.tester.plutoGateway.DisPressOKLatchStatus
            latchStatusNeedsReset = self.tester.plutoGateway.DisPressOKLatchNeedsReset
            press = self.tester.plutoGateway.DisPress

            val = P2c(450)

            port.write(val)

            print(c2P(val) * 10)

            pressVal = int(c2P(val) * 10)

            print(pressVal)

            trip = val >= P2c(465)
            warning = val >= P2c(440)



            self.checkChange([(port, val),
                              (valid, True),
                              (permit, not trip),
                              (warn, warning),
                              (lacthOK,not trip),
                              (lacthStatus, trip),
                              (latchStatusNeedsReset, 0),
                              (press, pressVal)],3)

            self.checkDuring([(permit, 1), (lacthOK, 1)], 60 * 10 - 10)

            self.checkChange([(port, val),
                              (valid, True),
                              (permit, not warning),
                              (warn, 0),
                              (lacthOK,not warning),
                              (lacthStatus, warning),
                              (latchStatusNeedsReset, 0),
                              (press, pressVal)],30)

            if warning:
                setDefautls(self, reset=False)

                self.checkChange([(permit, 0),
                                  (warn, 0),
                                  (lacthOK, 0),
                                  (lacthStatus, 2),
                                  (latchStatusNeedsReset, 1)], 30)

                if resetMode:
                    self.pressChannels([reset])
                else:
                    self.pressChannels([soft_reset])
                resetMode = not resetMode




        except Exception as e:
            self.step("TestImmediateTrips failed." + str(e))
            return False

        return True

class TestDelay3(Test):
    def __init__(self, tester, id):
        Test.__init__(self, tester, id)
        self.name = "TestDelay3"
        self.desc = "TestDelay3"

    def test(self):
        self.step(self.desc)

        setDefautls(self)

        reset = self.tester.testBox.plc.cold_I33
        soft_reset = self.tester.plutoGateway.ResetGate_w
        permit = self.tester.testBox.plc.cold_Q0
        resetMode = True


        try:
            #the discharge temperature is OK (<=130C AND <=125C(wait 30 min) )

            port = self.tester.testBox.plc.cold_IA0
            valid = self.tester.plutoGateway.DisTempValid
            warn = self.tester.plutoGateway.DisTempWarn
            lacthOK = self.tester.plutoGateway.DisTempOKLatch
            lacthStatus = self.tester.plutoGateway.DisTempOKLatchStatus
            latchStatusNeedsReset =  self.tester.plutoGateway.DisTempOKLatchNeedsReset
            temp = self.tester.plutoGateway.DisTemp

            val = C2v(128)


            port.write(val)

            print(v2C(val)*100)

            tempVal = int(v2C(val)*100)

            trip = val > C2v(130)
            warning = val > C2v(125)


            self.checkChange([(port, val),
                              (valid, True),
                              (permit, not trip),
                              (warn, warning),
                              (lacthOK,not trip),
                              (lacthStatus, trip),
                              (latchStatusNeedsReset, 0),
                              (temp, tempVal)],3)

            self.checkDuring([(permit, 1), (lacthOK, 1)], 60 * 30 - 10)

            self.checkChange([(port, val),
                              (valid, True),
                              (permit, not warning),
                              (warn, 0),
                              (lacthOK,not warning),
                              (lacthStatus, warning),
                              (latchStatusNeedsReset, 0),
                              (temp, tempVal)],30)



            if warning:
                setDefautls(self, reset=False)

                self.checkChange([(permit, 0),
                                  (warn, 0),
                                  (lacthOK, 0),
                                  (lacthStatus, 2),
                                  (latchStatusNeedsReset, 1)], 30)

                if resetMode:
                    self.pressChannels([reset])
                else:
                    self.pressChannels([soft_reset])
                resetMode = not resetMode





        except Exception as e:
            self.step("TestImmediateTrips failed." + str(e))
            return False

        return True