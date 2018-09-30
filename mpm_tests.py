from tester import Test
import random

# ligar a test box e por defaults

mA4 = 110
mA20 = 320
m = (mA20 - mA4) / (20 - 4)
b = mA4 - (4 * m)


def CtoK(mA):
    K = mA * m + b
    return K


def KtoC(K):
    mA = (K - b) / m
    mA = min(mA, 21.5)
    if mA < 3.5:
        mA = 21.5
    return mA


class TestPlutoGatewayConfig(Test):
    def __init__(self, tester, id):
        Test.__init__(self, tester, id)
        self.name = "TestPlutoGatewayConfig"
        self.expected_config = [0, 7, 0, 0, 0, 257, 258, 259, 260, 0, 0, 0, 0, 0, 356, 513, 514, 515, 516, 517, 518,
                                519, 520, 0, 612, 769,
                                770, 771, 772, 773, 774, 775, 776, 777, 868, 0, 0, 100, 0, 0, 0, 1]

        '''
        # Activate Data to Pluto Area 0, 1 and 2
        gateway_config_write_read(1,0b0111)
        
        # Data to Pluto Timeout = 0
        gateway_config_write_read(2,0)
        
        # Additional Data Areas for PLC 1
        gateway_config_write_read(5,0x0101)
        gateway_config_write_read(6,0x0102)
        gateway_config_write_read(7,0x0103)
        gateway_config_write_read(8,0x0104)
        gateway_config_write_read(9,0x0000)
        gateway_config_write_read(10,0x0000)
        gateway_config_write_read(11,0x0000)
        gateway_config_write_read(12,0x0000)
        gateway_config_write_read(13,0x0000)
        gateway_config_write_read(14,0x0164)
        
        # Additional Data Areas for PLC 2
        gateway_config_write_read(15,0x0201)
        gateway_config_write_read(16,0x0202)
        gateway_config_write_read(17,0x0203)
        gateway_config_write_read(18,0x0204)
        gateway_config_write_read(19,0x0205)
        gateway_config_write_read(20,0x0206)
        gateway_config_write_read(21,0x0207)
        gateway_config_write_read(22,0x0208)
        gateway_config_write_read(23,0x0000)
        gateway_config_write_read(24,0x0264)
        
        
        # Additional Data Areas for PLC 3
        gateway_config_write_read(25,0x0301)
        gateway_config_write_read(26,0x0302)
        gateway_config_write_read(27,0x0303)
        gateway_config_write_read(28,0x0304)
        gateway_config_write_read(29,0x0305)
        gateway_config_write_read(30,0x0306)
        gateway_config_write_read(31,0x0307)
        gateway_config_write_read(32,0x0308)
        gateway_config_write_read(33,0x0309)
        gateway_config_write_read(34,0x0364)
        
        
        # Data to Pluto Cycle time = 100 ms
        gateway_config_write_read(37,100)
        
        # Gateway Node number = 0
        gateway_config_write_read(41,0x001)
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
        self.desc = "Check Pluto Gateway sees Pluto D20 as node 1,2 and 3."

    def test(self):
        good = True
        for n in [1, 2, 3]:
            plc = self.tester.plutoGateway.read_bit(36, 1, n)

            if plc == 0:
                self.step("Pluto Gateway doens't see PLC %d as node %d" % (n, n))
                good = False

        if not good:
            return False

        self.step(("Pluto Gateway sees all 3 D20 PLCs as nodes 1,2,3."))
        return True


class TestChannelsBootDefault(Test):
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
        return False


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
                ch, "%d:%d.%d" % (plutoGateway[ch]["unit_id"], plutoGateway[ch]["addr"], plutoGateway[ch]["bit"]),
                ch_rbv, "%d:%d.%d" % (
                plutoGateway[ch_rbv]["unit_id"], plutoGateway[ch_rbv]["addr"], plutoGateway[ch_rbv]["bit"])))

                original_write = self.tester.plutoGateway.read_ch(ch)
                read = self.tester.plutoGateway.read_ch(ch_rbv)
                if original_write != read:
                    self.step("Failed on %s (%s) and %s (%s)." % (
                        ch,
                        "%d:%d.%d" % (plutoGateway[ch]["unit_id"], plutoGateway[ch]["addr"], plutoGateway[ch]["bit"]),
                        ch_rbv, "%d:%d.%d" % (
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
                        "%d:%d.%d" % (plutoGateway[ch]["unit_id"], plutoGateway[ch]["addr"], plutoGateway[ch]["bit"]),
                        ch_rbv, "%d:%d.%d" % (
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
                        "%d:%d.%d" % (plutoGateway[ch]["unit_id"], plutoGateway[ch]["addr"], plutoGateway[ch]["bit"]),
                        ch_rbv, "%d:%d.%d" % (
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
                        "%d:%d.%d" % (plutoGateway[ch]["unit_id"], plutoGateway[ch]["addr"], plutoGateway[ch]["bit"]),
                        ch_rbv, "%d:%d.%d" % (
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
                        "%d:%d.%d" % (plutoGateway[ch]["unit_id"], plutoGateway[ch]["addr"], plutoGateway[ch]["bit"]),
                        ch_rbv, "%d:%d.%d" % (
                            plutoGateway[ch_rbv]["unit_id"], plutoGateway[ch_rbv]["addr"],
                            plutoGateway[ch_rbv]["bit"])))
                    return False

        self.step("All write adds are connected with the respective readback values addrs")
        return True


class TestAnalogScaling(Test):
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
        return True


class TestTemperatureSetpoints(Test):
    def __init__(self, tester, id):
        Test.__init__(self, tester, id)
        self.name = "TestTemperatureSetpoints"
        self.desc = "Test PLC reaction to temperature Setpoints"

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
            return False


class TestAcPermitCoolantValve(Test):
    def __init__(self, tester, id):
        Test.__init__(self, tester, id)
        self.name = "TestAcPermitCoolantValve"
        self.desc = "Test PLC 01 permits logic: power and coolant valve."

    def test(self):
        self.step(self.desc)

        noLeakPort = self.tester.testBox.plc.P1_I4
        noLeak = self.tester.plutoGateway.P1_NoLeak
        leakFilter = self.tester.plutoGateway.P1_LeakFilter
        leakOkLatch = self.tester.plutoGateway.P1_LeakOkLatch
        leakOkLatchStatus = self.tester.plutoGateway.P1_LeakOkLatchStatus
        leakOkLatchNeedsReset = self.tester.plutoGateway.P1_LeakOkLatchNeedsReset

        noLeakFaultPort = self.tester.testBox.plc.P1_I7
        noLeakFault = self.tester.plutoGateway.P1_NotLeakFault
        leakFaultFilter = self.tester.plutoGateway.P1_LeakFaultFilter
        leakFaultOkLatch = self.tester.plutoGateway.P1_LeakFaultOkLatch
        leakFaultOkLatchStatus = self.tester.plutoGateway.P1_LeakFaultOkLatchStatus
        leakFaultOkLatchNeedsReset = self.tester.plutoGateway.P1_LeakFaultOkLatchNeedsReset

        leakIndicator = self.tester.testBox.plc.P1_IQ13

        resetLeak_w = self.tester.plutoGateway.P1_ResetLeak_w

        noSmokePort = self.tester.testBox.plc.P1_I6
        noSmoke = self.tester.plutoGateway.P1_NoSmoke
        smokeFilter = self.tester.plutoGateway.P1_SmokeFilter
        smokeOkLatch = self.tester.plutoGateway.P1_SmokeOkLatch
        smokeOkLatchStatus = self.tester.plutoGateway.P1_SmokeOkLatchStatus
        smokeOkLatchNeedsReset = self.tester.plutoGateway.P1_SmokeOkLatchNeedsReset

        noSmokeFaultPort = self.tester.testBox.plc.P2_I4
        noSmokeFault = self.tester.plutoGateway.P2_NoSmokeFault
        smokeFaultFilter = self.tester.plutoGateway.P1_SmokeFaultFilter
        smokeFaultOkLatch = self.tester.plutoGateway.P1_SmokeFaultOkLatch
        smokeFaultOkLatchStatus = self.tester.plutoGateway.P1_SmokeFaultOkLatchStatus
        smokeFaultOkLatchNeedsReset = self.tester.plutoGateway.P1_SmokeFaultOkLatchNeedsReset

        smokeIndicator = self.tester.testBox.plc.P1_IQ15

        resetSmoke_w = self.tester.plutoGateway.P1_ResetSmoke_w

        tmp0Port = self.tester.testBox.plc.P1_IA0
        tmp1Port = self.tester.testBox.plc.P1_IA1
        tmp2Port = self.tester.testBox.plc.P1_IA2
        tmp3Port = self.tester.testBox.plc.P1_IA3

        tmp0 = self.tester.plutoGateway.P1_Tsw0
        tmp1 = self.tester.plutoGateway.P1_Tsw1
        tmp2 = self.tester.plutoGateway.P1_Tsw2
        tmp3 = self.tester.plutoGateway.P1_Tsw3

        tempOk = self.tester.plutoGateway.P1_TempOk
        tempHighFilter = self.tester.plutoGateway.P1_TempHighFilter
        tempOkLatch = self.tester.plutoGateway.P1_TempOkLatch
        tempOkLatchStatus = self.tester.plutoGateway.P1_TempOkLatchStatus
        tempOkLatchNeedsReset = self.tester.plutoGateway.P1_TempOkLatchNeedsReset

        tempIndicator = self.tester.testBox.plc.P1_IQ14

        resetTemp_w = self.tester.plutoGateway.P1_ResetTemp_w

        masterResetPort = self.tester.testBox.plc.P2_I7
        masterReset = self.tester.plutoGateway.P2_MasterResetButton

        valvePort = self.tester.testBox.plc.P1_Q2
        valve = self.tester.plutoGateway.P1_CoolantValve

        utPermitPort = self.tester.testBox.plc.P1_Q0
        utPermitIndicator = self.tester.testBox.plc.P1_IQ16
        utPermit = self.tester.plutoGateway.P1_UtPowerPerm

        noLeakPortValues = [0, 1]
        noLeakFaultPortValues = [0, 1]

        noSmokePortValues = [0, 1]
        noSmokeFaultPortValues = [0, 1]

        tmp0PortValues = [0, 1]
        tmp1PortValues = [0, 1]
        tmp2PortValues = [0, 1]
        tmp3PortValues = [0, 1]

        resetMode = True  # ["soft", "hard"]

        self.setDefault(check=False)

        n = 0

        try:
            for noLeakPortValue in noLeakPortValues:
                for noLeakFaultPortValue in noLeakFaultPortValues:
                    for noSmokePortValue in noSmokePortValues:
                        for noSmokeFaultPortValue in noSmokeFaultPortValues:
                            for tmp0PortValue in tmp0PortValues:
                                for tmp1PortValue in tmp1PortValues:
                                    for tmp2PortValue in tmp2PortValues:
                                        for tmp3PortValue in tmp3PortValues:
                                            # for resetMode in resetModes:

                                            n = n + 1
                                            print(
                                                "--------------------------------------------------------------------------",
                                                n)

                                            if (tmp0PortValue + tmp1PortValue + tmp2PortValue + tmp3PortValue) <= 2:
                                                continue

                                            if n < 0:
                                                continue

                                            compare = self.readAllChannels()

                                            noLeakPort.write(noLeakPortValue)
                                            noLeakFaultPort.write(noLeakFaultPortValue)
                                            noSmokePort.write(noSmokePortValue)
                                            noSmokeFaultPort.write(noSmokeFaultPortValue)
                                            tmp0Port.write(tmp0PortValue)
                                            tmp1Port.write(tmp1PortValue)
                                            tmp2Port.write(tmp2PortValue)
                                            tmp3Port.write(tmp3PortValue)

                                            # No permit output should change during 7 seconds

                                            self.checkDuring([(valvePort, 1),
                                                              (valve, 1,),
                                                              (utPermitPort, 1),
                                                              (utPermitIndicator, 1),
                                                              (utPermit, 1)
                                                              ], 7)

                                            leakFilterValue = not noLeakPortValue
                                            leakOkLatchValue = noLeakPortValue
                                            leakOkLatchStatusValue = not noLeakPortValue
                                            leakOkLatchNeedsResetValue = 0

                                            leakFaultFilterValue = not noLeakFaultPortValue
                                            leakFaultOkLatchValue = noLeakFaultPortValue
                                            leakFaultOkLatchStatusValue = not noLeakFaultPortValue
                                            leakFaultOkLatchNeedsResetValue = 0

                                            leakIndicatorValue = 0
                                            if leakOkLatchStatusValue == 2 or leakFaultOkLatchStatusValue == 2:
                                                leakIndicatorValue = 2
                                            if leakOkLatchStatusValue == 1 or leakFaultOkLatchStatusValue == 1:
                                                leakIndicatorValue = 1

                                            smokeFilterValue = not noSmokePortValue
                                            smokeOkLatchValue = noSmokePortValue
                                            smokeOkLatchStatusValue = not noSmokePortValue
                                            smokeOkLatchNeedsResetValue = 0

                                            smokeFaultFilterValue = not noSmokeFaultPortValue
                                            smokeFaultOkLatchValue = noSmokeFaultPortValue
                                            smokeFaultOkLatchStatusValue = not noSmokeFaultPortValue
                                            smokeFaultOkLatchNeedsResetValue = 0

                                            smokeIndicatorValue = 0
                                            if smokeOkLatchStatusValue == 2 or smokeFaultOkLatchStatusValue == 2:
                                                smokeIndicatorValue = 2
                                            if smokeOkLatchStatusValue == 1 or smokeFaultOkLatchStatusValue == 1:
                                                smokeIndicatorValue = 1

                                            tempOkValue = (
                                                                      tmp0PortValue + tmp1PortValue + tmp2PortValue + tmp3PortValue) >= 3
                                            tempHighFilterValue = not tempOkValue
                                            tempOkLatchValue = tempOkValue
                                            tempOkLatcStatusValue = not tempOkValue
                                            tempOkLatchNeedsResetValue = 0

                                            tempIndicatorValue = tempOkLatcStatusValue

                                            valvePortValue = leakFaultOkLatchValue and leakOkLatchValue
                                            valveValue = valvePortValue

                                            utPermitPortValue = tempOkLatchValue and leakFaultOkLatchValue and leakOkLatchValue and smokeFaultOkLatchValue and smokeOkLatchValue
                                            utPermitIndicatorValue = utPermitPortValue
                                            utPermitValue = utPermitPortValue

                                            # Try to reset but this must have no effect
                                            self.pressChannels(
                                                [resetTemp_w, resetLeak_w, resetSmoke_w, masterResetPort])

                                            print("NICE")

                                            self.checkChange([
                                                # Leak
                                                (noLeakPort, noLeakPortValue),
                                                (noLeak, noLeakPortValue),

                                                (noLeakFaultPort, noLeakFaultPortValue),
                                                (noLeakFault, noLeakFaultPortValue),

                                                (leakFilter, leakFilterValue),
                                                (leakOkLatch, leakOkLatchValue),
                                                (leakOkLatchStatus, leakOkLatchStatusValue),
                                                (leakOkLatchNeedsReset, leakOkLatchNeedsResetValue),

                                                (leakFaultFilter, leakFaultFilterValue),
                                                (leakFaultOkLatch, leakFaultOkLatchValue),
                                                (leakFaultOkLatchStatus, leakFaultOkLatchStatusValue),
                                                (leakFaultOkLatchNeedsReset, leakFaultOkLatchNeedsResetValue),

                                                (leakIndicator, leakIndicatorValue),

                                                # Smoke
                                                (noSmokePort, noSmokePortValue),
                                                (noSmoke, noSmokePortValue),

                                                (noSmokeFaultPort, noSmokeFaultPortValue),
                                                (noSmokeFault, noSmokeFaultPortValue),

                                                (smokeFilter, smokeFilterValue),
                                                (smokeOkLatch, smokeOkLatchValue),
                                                (smokeOkLatchStatus, smokeOkLatchStatusValue),
                                                (smokeOkLatchNeedsReset, smokeOkLatchNeedsResetValue),

                                                (smokeFaultFilter, smokeFaultFilterValue),
                                                (smokeFaultOkLatch, smokeFaultOkLatchValue),
                                                (smokeFaultOkLatchStatus, smokeFaultOkLatchStatusValue),
                                                (smokeFaultOkLatchNeedsReset, smokeFaultOkLatchNeedsResetValue),

                                                (smokeIndicator, smokeIndicatorValue),

                                                # Temperature

                                                (tmp0Port, tmp0PortValue),
                                                (tmp1Port, tmp1PortValue),
                                                (tmp2Port, tmp2PortValue),
                                                (tmp3Port, tmp3PortValue),

                                                (tmp0, tmp0PortValue),
                                                (tmp1, tmp1PortValue),
                                                (tmp2, tmp2PortValue),
                                                (tmp3, tmp3PortValue),

                                                (tempOk, tempOkValue),
                                                (tempHighFilter, tempHighFilterValue),
                                                (tempOkLatch, tempOkLatchValue),
                                                (tempOkLatchStatus, tempOkLatcStatusValue),
                                                (tempOkLatchNeedsReset, tempOkLatchNeedsResetValue),

                                                (tempIndicator, tempIndicatorValue),

                                                # Outputs

                                                (valvePort, valvePortValue),
                                                (valve, valveValue),
                                                (utPermitPort, utPermitPortValue),
                                                (utPermitIndicator, utPermitIndicatorValue),
                                                (utPermit, utPermitValue),

                                            ], 5, compare)

                                            print("NICE2")
                                            resets = []

                                            if not noLeakPortValue:
                                                compare = self.readAllChannels()
                                                noLeakPort.write(1)

                                                leakIndicatorVal = 2
                                                if not noLeakFaultPortValue:
                                                    leakIndicatorVal = 1

                                                self.checkChange([(noLeakPort, 1),
                                                                  (noLeak, 1),

                                                                  (leakFilter, 0),
                                                                  (leakOkLatch, 0),
                                                                  (leakOkLatchStatus, 2),
                                                                  (leakOkLatchNeedsReset, 1),

                                                                  (leakIndicator, leakIndicatorVal),

                                                                  (valvePort, 0),
                                                                  (valve, 0),
                                                                  (utPermitPort, 0),
                                                                  (utPermitIndicator, 0),
                                                                  (utPermit, 0),

                                                                  ], 1, compare)
                                                resets.append(resetLeak_w)

                                            print("NICE3")

                                            if not noLeakFaultPortValue:
                                                compare = self.readAllChannels()
                                                noLeakFaultPort.write(1)
                                                self.checkChange([(noLeakFaultPort, 1),
                                                                  (noLeakFault, 1),

                                                                  (leakFaultFilter, 0),
                                                                  (leakFaultOkLatch, 0),
                                                                  (leakFaultOkLatchStatus, 2),
                                                                  (leakFaultOkLatchNeedsReset, 1),

                                                                  (leakIndicator, 2),

                                                                  (valvePort, 0),
                                                                  (valve, 0),
                                                                  (utPermitPort, 0),
                                                                  (utPermitIndicator, 0),
                                                                  (utPermit, 0),

                                                                  ], 1, compare)
                                                resets.append(resetLeak_w)

                                            print("NICE4")

                                            if not noSmokePortValue:
                                                compare = self.readAllChannels()
                                                noSmokePort.write(1)

                                                smokeIndicatorVal = 2
                                                if not noSmokeFaultPortValue:
                                                    smokeIndicatorVal = 1

                                                self.checkChange([(noSmokePort, 1),
                                                                  (noSmoke, 1),

                                                                  (smokeFilter, 0),
                                                                  (smokeOkLatch, 0),
                                                                  (smokeOkLatchStatus, 2),
                                                                  (smokeOkLatchNeedsReset, 1),

                                                                  (smokeIndicator, smokeIndicatorVal),

                                                                  (utPermitPort, 0),
                                                                  (utPermitIndicator, 0),
                                                                  (utPermit, 0),

                                                                  ], 1, compare)
                                                resets.append(resetSmoke_w)

                                            print("NICE4.2")

                                            if not noSmokeFaultPortValue:
                                                compare = self.readAllChannels()
                                                noSmokeFaultPort.write(1)
                                                self.checkChange([(noSmokeFaultPort, 1),
                                                                  (noSmokeFault, 1),

                                                                  (smokeFaultFilter, 0),
                                                                  (smokeFaultOkLatch, 0),
                                                                  (smokeFaultOkLatchStatus, 2),
                                                                  (smokeFaultOkLatchNeedsReset, 1),

                                                                  (smokeIndicator, 2),

                                                                  (utPermitPort, 0),
                                                                  (utPermitIndicator, 0),
                                                                  (utPermit, 0),

                                                                  ], 1, compare)
                                                resets.append(resetSmoke_w)

                                            print("NICE4.3")

                                            if not tempOkValue:
                                                tmp0Port.write(1)
                                                tmp1Port.write(1)
                                                tmp2Port.write(1)
                                                tmp3Port.write(1)
                                                self.checkChange([(tmp0Port, 1),
                                                                  (tmp1Port, 1),
                                                                  (tmp2Port, 1),
                                                                  (tmp3Port, 1),

                                                                  (tmp0, 1),
                                                                  (tmp1, 1),
                                                                  (tmp2, 1),
                                                                  (tmp3, 1),

                                                                  (tempOk, 1),
                                                                  (tempHighFilter, 0),
                                                                  (tempOkLatch, 0),
                                                                  (tempOkLatchStatus, 2),
                                                                  (tempOkLatchNeedsReset, 1),

                                                                  (tempIndicator, 2),

                                                                  (utPermitPort, 0),
                                                                  (utPermitIndicator, 0),
                                                                  (utPermit, 0),

                                                                  ], 1, compare)

                                                resets.append(resetTemp_w)

                                            print("NICE5")
                                            if len(resets) > 0:
                                                if resetMode:
                                                    # self.pressChannels([masterResetPort])
                                                    # self.pressChannels([masterResetPort])

                                                    masterResetPort.write(1)

                                                    self.sleep(1)
                                                    masterResetPort.write(0)
                                                    print('>>>>>>>>>>>>>>>>>>>>hard')

                                                else:
                                                    self.pressChannels(resets)
                                                    print('>>>>>>>>>>>>>>>>>>>>soft')

                                                resetMode = not resetMode

                                            tmp0Port.write(1)
                                            tmp1Port.write(1)
                                            tmp2Port.write(1)
                                            tmp3Port.write(1)

                                            self.checkDefault()

            self.step("Power and Coolant Valve logic correct.")
            return True

        except ValueError as e:
            print(n)
            self.step("Power and Coolant Valve logic failed! Failed at %s. Error: %s " % (self.step_m, str(e)))
            return False


class TestColdCryoPermits(Test):
    def __init__(self, tester, id):
        Test.__init__(self, tester, id)
        self.name = "TestColdCryoPermits"
        self.desc = "Test Cold and Cryo plate permits logic"

    def test(self):
        self.step(self.desc)

        ## Cold

        tmp0Port = self.tester.testBox.plc.P2_IA0
        tmp1Port = self.tester.testBox.plc.P2_IA1
        tmp2Port = self.tester.testBox.plc.P2_IA2
        tmp3Port = self.tester.testBox.plc.P2_IA3

        tmp0Current = self.tester.plutoGateway.P2_ClpRtd0Current
        tmp1Current = self.tester.plutoGateway.P2_ClpRtd1Current
        tmp2Current = self.tester.plutoGateway.P2_ClpRtd2Current
        tmp3Current = self.tester.plutoGateway.P2_ClpRtd3Current

        tmp0Temp = self.tester.plutoGateway.P2_ClpRtd0Temp
        tmp1Temp = self.tester.plutoGateway.P2_ClpRtd1Temp
        tmp2Temp = self.tester.plutoGateway.P2_ClpRtd2Temp
        tmp3Temp = self.tester.plutoGateway.P2_ClpRtd3Temp

        tmp0NotLow = self.tester.plutoGateway.P2_ClpTemp0NotLow
        tmp1NotLow = self.tester.plutoGateway.P2_ClpTemp1NotLow
        tmp2NotLow = self.tester.plutoGateway.P2_ClpTemp2NotLow
        tmp3NotLow = self.tester.plutoGateway.P2_ClpTemp3NotLow

        tmp0NotHigh = self.tester.plutoGateway.P2_ClpTemp0NotHigh
        tmp1NotHigh = self.tester.plutoGateway.P2_ClpTemp1NotHigh
        tmp2NotHigh = self.tester.plutoGateway.P2_ClpTemp2NotHigh
        tmp3NotHigh = self.tester.plutoGateway.P2_ClpTemp3NotHigh

        tempNotHigh = self.tester.plutoGateway.P2_ClpTempNotHigh
        tempHighFilter = self.tester.plutoGateway.P2_ClpTempHighFilter

        tempHighOkLatch = self.tester.plutoGateway.P2_ClpTempHighOkLatch
        tempHighOkLatchStatus = self.tester.plutoGateway.P2_ClpTempHighOkLatchStatus
        tempHighOkLatchNeedsReset = self.tester.plutoGateway.P2_ClpTempHighOkLatchNeedsReset
        hotLight = self.tester.plutoGateway.P2_ClpHotLight
        hotLightPort = self.tester.testBox.plc.P2_IQ14

        resetTempHigh_w = self.tester.plutoGateway.P2_ResetClpHigh_w

        heatPermitLockLight = self.tester.plutoGateway.P2_ClpHeatLockLight
        heatPermitLockLightPort = self.tester.testBox.plc.P2_IQ16
        heatPermit = self.tester.plutoGateway.P2_ClpHeatPerm
        heatPermitPort = self.tester.testBox.plc.P2_Q0

        tempNotLow = self.tester.plutoGateway.P2_ClpTempNotLow
        tempLowFilter = self.tester.plutoGateway.P2_ClpTempLowFilter
        tempLowOkLatch = self.tester.plutoGateway.P2_ClpTempLowOkLatch
        tempLowOkLatchStatus = self.tester.plutoGateway.P2_ClpTempLowOkLatchStatus
        tempLowOkLatchNeedsReset = self.tester.plutoGateway.P2_ClpTempLowOkLatchNeedsReset
        coldLight = self.tester.plutoGateway.P2_ClpColdLight
        coldLightPort = self.tester.testBox.plc.P2_IQ15

        resetTempLow_w = self.tester.plutoGateway.P2_ResetClpLow_w

        refPermitLockLight = self.tester.plutoGateway.P2_ClpFrigLockLight
        refPermitLockLightPort = self.tester.testBox.plc.P2_IQ17
        refPermit = self.tester.plutoGateway.P2_ClpRefPerm
        refPermitPort = self.tester.testBox.plc.P2_Q1

        noTempCurr = 2.5  # mA
        lowTempCurr = KtoC(200)
        normalTempCurr = KtoC(250)
        highTempCurr = KtoC(300)

        tmp0PortValues = [noTempCurr, lowTempCurr, normalTempCurr, highTempCurr]
        tmp1PortValues = [noTempCurr, lowTempCurr, normalTempCurr, highTempCurr]
        tmp2PortValues = [noTempCurr, lowTempCurr, normalTempCurr, highTempCurr]
        tmp3PortValues = [noTempCurr, lowTempCurr, normalTempCurr, highTempCurr]

        lowLimitCurr = KtoC(228)
        highLimitCurr = KtoC(295)
        zeroLimitCurr = 3

        # Cryo

        CRYtmp0Port = self.tester.testBox.plc.P3_IA0
        CRYtmp1Port = self.tester.testBox.plc.P3_IA1
        CRYtmp2Port = self.tester.testBox.plc.P3_IA2
        CRYtmp3Port = self.tester.testBox.plc.P3_IA3

        CRYtmp0Current = self.tester.plutoGateway.P3_CryRtd0Current
        CRYtmp1Current = self.tester.plutoGateway.P3_CryRtd1Current
        CRYtmp2Current = self.tester.plutoGateway.P3_CryRtd2Current
        CRYtmp3Current = self.tester.plutoGateway.P3_CryRtd3Current

        CRYtmp0Temp = self.tester.plutoGateway.P3_CryRtd0Temp
        CRYtmp1Temp = self.tester.plutoGateway.P3_CryRtd1Temp
        CRYtmp2Temp = self.tester.plutoGateway.P3_CryRtd2Temp
        CRYtmp3Temp = self.tester.plutoGateway.P3_CryRtd3Temp

        CRYtmp0NotLow = self.tester.plutoGateway.P3_CryTemp0NotLow
        CRYtmp1NotLow = self.tester.plutoGateway.P3_CryTemp1NotLow
        CRYtmp2NotLow = self.tester.plutoGateway.P3_CryTemp2NotLow
        CRYtmp3NotLow = self.tester.plutoGateway.P3_CryTemp3NotLow

        CRYtmp0NotHigh = self.tester.plutoGateway.P3_CryTemp0NotHigh
        CRYtmp1NotHigh = self.tester.plutoGateway.P3_CryTemp1NotHigh
        CRYtmp2NotHigh = self.tester.plutoGateway.P3_CryTemp2NotHigh
        CRYtmp3NotHigh = self.tester.plutoGateway.P3_CryTemp3NotHigh

        CRYtempNotHigh = self.tester.plutoGateway.P3_CryTempNotHigh
        CRYtempHighFilter = self.tester.plutoGateway.P3_CryTempHighFilter

        CRYtempHighOkLatch = self.tester.plutoGateway.P3_CryTempHighOkLatch
        CRYtempHighOkLatchStatus = self.tester.plutoGateway.P3_CryTempHighOkLatchStatus
        CRYtempHighOkLatchNeedsReset = self.tester.plutoGateway.P3_CryTempHighOkLatchNeedsReset
        CRYhotLight = self.tester.plutoGateway.P3_CryHotLight
        CRYhotLightPort = self.tester.testBox.plc.P3_IQ12

        CRYresetTempHigh_w = self.tester.plutoGateway.P3_ResetCryHigh_w

        CRYheatPermitLockLight = self.tester.plutoGateway.P3_CryHeatLockLight
        CRYheatPermitLockLightPort = self.tester.testBox.plc.P3_IQ16
        CRYheatPermit = self.tester.plutoGateway.P3_CryHeatPerm
        CRYheatPermitPort = self.tester.testBox.plc.P3_Q0

        CRYtempNotLow = self.tester.plutoGateway.P3_CryTempNotLow
        CRYtempLowFilter = self.tester.plutoGateway.P3_CryTempLowFilter
        CRYtempLowOkLatch = self.tester.plutoGateway.P3_CryTempLowOkLatch
        CRYtempLowOkLatchStatus = self.tester.plutoGateway.P3_CryTempLowOkLatchStatus
        CRYtempLowOkLatchNeedsReset = self.tester.plutoGateway.P3_CryTempLowOkLatchNeedsReset
        CRYcoldLight = self.tester.plutoGateway.P3_CryColdLight
        CRYcoldLightPort = self.tester.testBox.plc.P3_IQ13

        CRYresetTempLow_w = self.tester.plutoGateway.P3_ResetCryLow_w

        CRYrefPermitLockLight = self.tester.plutoGateway.P3_CryFrigLockLight
        CRYrefPermitLockLightPort = self.tester.testBox.plc.P3_IQ17
        CRYrefPermit = self.tester.plutoGateway.P3_CryRefPerm
        CRYrefPermitPort = self.tester.testBox.plc.P3_Q1

        CRYnoTempCurr = 2.5  # mA
        CRYlowTempCurr = KtoC(120)
        CRYnormalTempCurr = KtoC(200)
        CRYhighTempCurr = KtoC(275)

        CRYtmp0PortValues = [CRYnoTempCurr, CRYlowTempCurr, CRYnormalTempCurr, CRYhighTempCurr]
        CRYtmp1PortValues = [CRYnoTempCurr, CRYlowTempCurr, CRYnormalTempCurr, CRYhighTempCurr]
        CRYtmp2PortValues = [CRYnoTempCurr, CRYlowTempCurr, CRYnormalTempCurr, CRYhighTempCurr]
        CRYtmp3PortValues = [CRYnoTempCurr, CRYlowTempCurr, CRYnormalTempCurr, CRYhighTempCurr]

        CRYlowLimitCurr = KtoC(130)
        CRYhighLimitCurr = KtoC(270)
        CRYzeroLimitCurr = 3

        ## Both

        masterResetPort = self.tester.testBox.plc.P2_I7

        resetMode = True  # ["soft", "hard"]

        self.setDefault()

        n = 0
        a = 0
        try:
            for a in range(4):
                for b in range(4):
                    for c in range(4):
                        for d in range(4):

                            tmp0PortValue = tmp0PortValues[a]
                            tmp1PortValue = tmp1PortValues[b]
                            tmp2PortValue = tmp2PortValues[c]
                            tmp3PortValue = tmp3PortValues[d]

                            CRYtmp0PortValue = CRYtmp0PortValues[d]
                            CRYtmp1PortValue = CRYtmp1PortValues[c]
                            CRYtmp2PortValue = CRYtmp2PortValues[b]
                            CRYtmp3PortValue = CRYtmp3PortValues[a]

                            n = n + 1
                            print("--------------------------------------------------------------------------", n)

                            if n < 0:
                                continue

                            def moreThanAre(portsValues, values, thresold):
                                for value in values:
                                    n = 0
                                    for portValue in portsValues:
                                        if portValue == value:
                                            n += 1
                                    if n > thresold:
                                        return True

                            if moreThanAre([tmp0PortValue, tmp1PortValue, tmp2PortValue, tmp3PortValue],
                                           [noTempCurr, lowTempCurr, highTempCurr], 2):
                                continue

                            compare = self.readAllChannels()

                            tmp0Port.write(tmp0PortValue)
                            tmp1Port.write(tmp1PortValue)
                            tmp2Port.write(tmp2PortValue)
                            tmp3Port.write(tmp3PortValue)

                            tmp0NotLowValue = int(tmp0PortValue > lowLimitCurr)
                            tmp1NotLowValue = int(tmp1PortValue > lowLimitCurr)
                            tmp2NotLowValue = int(tmp2PortValue > lowLimitCurr)
                            tmp3NotLowValue = int(tmp3PortValue > lowLimitCurr)

                            tmp0NotHighValue = int(tmp0PortValue < highLimitCurr and tmp0PortValue > zeroLimitCurr)
                            tmp1NotHighValue = int(tmp1PortValue < highLimitCurr and tmp1PortValue > zeroLimitCurr)
                            tmp2NotHighValue = int(tmp2PortValue < highLimitCurr and tmp2PortValue > zeroLimitCurr)
                            tmp3NotHighValue = int(tmp3PortValue < highLimitCurr and tmp3PortValue > zeroLimitCurr)

                            tempNotHighValue = int((int(tmp0NotHighValue) + int(tmp1NotHighValue) + int(
                                tmp2NotHighValue) + int(tmp3NotHighValue)) >= 3)
                            tempHighFilterValue = not tempNotHighValue

                            tempHighOkLatchValue = tempNotHighValue
                            tempHighOkLatchStatusValue = not tempHighOkLatchValue
                            tempHighOkLatchNeedsResetValue = 0
                            hotLightValue = tempHighOkLatchStatusValue
                            hotLightPortValue = tempHighOkLatchStatusValue

                            heatPermitValue = tempNotHighValue
                            heatPermitPortValue = heatPermitValue
                            heatPermitLockLightValue = not heatPermitValue
                            heatPermitLockLightPortValue = not heatPermitValue

                            tempNotLowValue = int((int(tmp0NotLowValue) + int(tmp1NotLowValue) + int(
                                tmp2NotLowValue) + int(tmp3NotLowValue)) >= 3)
                            tempLowFilterValue = not tempNotLowValue

                            tempLowOkLatchValue = tempNotLowValue
                            tempLowOkLatchStatusValue = not tempLowOkLatchValue
                            tempLowOkLatchNeedsResetValue = 0
                            coldLightValue = tempLowOkLatchStatusValue
                            coldLightPortValue = tempLowOkLatchStatusValue

                            refPermitValue = tempNotLowValue and 1 and 1
                            refPermitPortValue = refPermitValue
                            refPermitLockLightValue = not refPermitValue
                            refPermitLockLightPortValue = not refPermitValue

                            # CRY

                            CRYtmp0Port.write(CRYtmp0PortValue)
                            CRYtmp1Port.write(CRYtmp1PortValue)
                            CRYtmp2Port.write(CRYtmp2PortValue)
                            CRYtmp3Port.write(CRYtmp3PortValue)

                            CRYtmp0NotLowValue = int(CRYtmp0PortValue > CRYlowLimitCurr)
                            CRYtmp1NotLowValue = int(CRYtmp1PortValue > CRYlowLimitCurr)
                            CRYtmp2NotLowValue = int(CRYtmp2PortValue > CRYlowLimitCurr)
                            CRYtmp3NotLowValue = int(CRYtmp3PortValue > CRYlowLimitCurr)

                            CRYtmp0NotHighValue = int(
                                CRYtmp0PortValue < CRYhighLimitCurr and CRYtmp0PortValue > CRYzeroLimitCurr)
                            CRYtmp1NotHighValue = int(
                                CRYtmp1PortValue < CRYhighLimitCurr and CRYtmp1PortValue > CRYzeroLimitCurr)
                            CRYtmp2NotHighValue = int(
                                CRYtmp2PortValue < CRYhighLimitCurr and CRYtmp2PortValue > CRYzeroLimitCurr)
                            CRYtmp3NotHighValue = int(
                                CRYtmp3PortValue < CRYhighLimitCurr and CRYtmp3PortValue > CRYzeroLimitCurr)

                            CRYtempNotHighValue = int((int(CRYtmp0NotHighValue) + int(CRYtmp1NotHighValue) + int(
                                CRYtmp2NotHighValue) + int(CRYtmp3NotHighValue)) >= 3)
                            CRYtempHighFilterValue = not CRYtempNotHighValue

                            CRYtempHighOkLatchValue = CRYtempNotHighValue
                            CRYtempHighOkLatchStatusValue = not CRYtempHighOkLatchValue
                            CRYtempHighOkLatchNeedsResetValue = 0
                            CRYhotLightValue = CRYtempHighOkLatchStatusValue
                            CRYhotLightPortValue = CRYtempHighOkLatchStatusValue

                            CRYheatPermitValue = CRYtempNotHighValue
                            CRYheatPermitPortValue = CRYheatPermitValue
                            CRYheatPermitLockLightValue = not CRYheatPermitValue
                            CRYheatPermitLockLightPortValue = not CRYheatPermitValue

                            CRYtempNotLowValue = int((int(CRYtmp0NotLowValue) + int(CRYtmp1NotLowValue) + int(
                                CRYtmp2NotLowValue) + int(CRYtmp3NotLowValue)) >= 3)
                            CRYtempLowFilterValue = not CRYtempNotLowValue

                            CRYtempLowOkLatchValue = CRYtempNotLowValue
                            CRYtempLowOkLatchStatusValue = not CRYtempLowOkLatchValue
                            CRYtempLowOkLatchNeedsResetValue = 0
                            CRYcoldLightValue = CRYtempLowOkLatchStatusValue
                            CRYcoldLightPortValue = CRYtempLowOkLatchStatusValue

                            CRYrefPermitValue = CRYtempNotLowValue and 1 and 1
                            CRYrefPermitPortValue = CRYrefPermitValue
                            CRYrefPermitLockLightValue = not CRYrefPermitValue
                            CRYrefPermitLockLightPortValue = not CRYrefPermitValue

                            print("WRITE")

                            # Should change immediately
                            self.checkChange([
                                (tmp0Port, tmp0PortValue),
                                (tmp1Port, tmp1PortValue),
                                (tmp2Port, tmp2PortValue),
                                (tmp3Port, tmp3PortValue),

                                (tmp0Current, tmp0PortValue * 1000),
                                (tmp1Current, tmp1PortValue * 1000),
                                (tmp2Current, tmp2PortValue * 1000),
                                (tmp3Current, tmp3PortValue * 1000),

                                (tmp0Temp, CtoK(tmp0PortValue)),
                                (tmp1Temp, CtoK(tmp1PortValue)),
                                (tmp2Temp, CtoK(tmp2PortValue)),
                                (tmp3Temp, CtoK(tmp3PortValue)),

                                (tmp0NotLow, tmp0NotLowValue),
                                (tmp1NotLow, tmp1NotLowValue),
                                (tmp2NotLow, tmp2NotLowValue),
                                (tmp3NotLow, tmp3NotLowValue),

                                (tmp0NotHigh, tmp0NotHighValue),
                                (tmp1NotHigh, tmp1NotHighValue),
                                (tmp2NotHigh, tmp2NotHighValue),
                                (tmp3NotHigh, tmp3NotHighValue),

                                (tempNotHigh, tempNotHighValue),

                                (tempNotLow, tempNotLowValue),

                                # CRY

                                (CRYtmp0Port, CRYtmp0PortValue),
                                (CRYtmp1Port, CRYtmp1PortValue),
                                (CRYtmp2Port, CRYtmp2PortValue),
                                (CRYtmp3Port, CRYtmp3PortValue),

                                (CRYtmp0Current, CRYtmp0PortValue * 1000),
                                (CRYtmp1Current, CRYtmp1PortValue * 1000),
                                (CRYtmp2Current, CRYtmp2PortValue * 1000),
                                (CRYtmp3Current, CRYtmp3PortValue * 1000),

                                (CRYtmp0Temp, CtoK(CRYtmp0PortValue)),
                                (CRYtmp1Temp, CtoK(CRYtmp1PortValue)),
                                (CRYtmp2Temp, CtoK(CRYtmp2PortValue)),
                                (CRYtmp3Temp, CtoK(CRYtmp3PortValue)),

                                (CRYtmp0NotLow, CRYtmp0NotLowValue),
                                (CRYtmp1NotLow, CRYtmp1NotLowValue),
                                (CRYtmp2NotLow, CRYtmp2NotLowValue),
                                (CRYtmp3NotLow, CRYtmp3NotLowValue),

                                (CRYtmp0NotHigh, CRYtmp0NotHighValue),
                                (CRYtmp1NotHigh, CRYtmp1NotHighValue),
                                (CRYtmp2NotHigh, CRYtmp2NotHighValue),
                                (CRYtmp3NotHigh, CRYtmp3NotHighValue),

                                (CRYtempNotHigh, CRYtempNotHighValue),

                                (CRYtempNotLow, CRYtempNotLowValue),

                            ], 2, compare)

                            print("IMEDIATO")

                            # Permits should not change during 9 seconds

                            self.checkDuring([(refPermitPort, 1),
                                              (refPermit, 1,),
                                              (heatPermitPort, 1),
                                              (heatPermit, 1),

                                              # CRY

                                              (CRYrefPermitPort, 1),
                                              (CRYrefPermit, 1,),
                                              (CRYheatPermitPort, 1),
                                              (CRYheatPermit, 1),
                                              ], 7)

                            print("6s")

                            self.pressChannels([resetTempHigh_w, resetTempLow_w, CRYresetTempHigh_w, CRYresetTempLow_w])

                            self.checkChange([
                                (tmp0Port, tmp0PortValue),
                                (tmp1Port, tmp1PortValue),
                                (tmp2Port, tmp2PortValue),
                                (tmp3Port, tmp3PortValue),

                                (tmp0Current, tmp0PortValue * 1000),
                                (tmp1Current, tmp1PortValue * 1000),
                                (tmp2Current, tmp2PortValue * 1000),
                                (tmp3Current, tmp3PortValue * 1000),

                                (tmp0Temp, CtoK(tmp0PortValue)),
                                (tmp1Temp, CtoK(tmp1PortValue)),
                                (tmp2Temp, CtoK(tmp2PortValue)),
                                (tmp3Temp, CtoK(tmp3PortValue)),

                                (tmp0NotLow, tmp0NotLowValue),
                                (tmp1NotLow, tmp1NotLowValue),
                                (tmp2NotLow, tmp2NotLowValue),
                                (tmp3NotLow, tmp3NotLowValue),

                                (tmp0NotHigh, tmp0NotHighValue),
                                (tmp1NotHigh, tmp1NotHighValue),
                                (tmp2NotHigh, tmp2NotHighValue),
                                (tmp3NotHigh, tmp3NotHighValue),

                                (tempNotHigh, tempNotHighValue),
                                (tempHighFilter, tempHighFilterValue),

                                (tempHighOkLatch, tempHighOkLatchValue),
                                (tempHighOkLatchStatus, tempHighOkLatchStatusValue),
                                (tempHighOkLatchNeedsReset, tempHighOkLatchNeedsResetValue),
                                (hotLight, hotLightValue),
                                (hotLightPort, hotLightPortValue),
                                (heatPermit, heatPermitValue),
                                (heatPermitPort, heatPermitPortValue),
                                (heatPermitLockLight, heatPermitLockLightValue),
                                (heatPermitLockLightPort, heatPermitLockLightPortValue),

                                (tempNotLow, tempNotLowValue),
                                (tempLowFilter, tempLowFilterValue),
                                (tempLowOkLatch, tempLowOkLatchValue),
                                (tempLowOkLatchStatus, tempLowOkLatchStatusValue),
                                (tempLowOkLatchNeedsReset, tempLowOkLatchNeedsResetValue),
                                (coldLight, coldLightValue),
                                (coldLightPort, coldLightPortValue),

                                (refPermit, refPermitValue),
                                (refPermitPort, refPermitPortValue),
                                (refPermitLockLight, refPermitLockLightValue),
                                (refPermitLockLightPort, refPermitLockLightPortValue),

                                # CRY

                                (CRYtmp0Port, CRYtmp0PortValue),
                                (CRYtmp1Port, CRYtmp1PortValue),
                                (CRYtmp2Port, CRYtmp2PortValue),
                                (CRYtmp3Port, CRYtmp3PortValue),

                                (CRYtmp0Current, CRYtmp0PortValue * 1000),
                                (CRYtmp1Current, CRYtmp1PortValue * 1000),
                                (CRYtmp2Current, CRYtmp2PortValue * 1000),
                                (CRYtmp3Current, CRYtmp3PortValue * 1000),

                                (CRYtmp0Temp, CtoK(CRYtmp0PortValue)),
                                (CRYtmp1Temp, CtoK(CRYtmp1PortValue)),
                                (CRYtmp2Temp, CtoK(CRYtmp2PortValue)),
                                (CRYtmp3Temp, CtoK(CRYtmp3PortValue)),

                                (CRYtmp0NotLow, CRYtmp0NotLowValue),
                                (CRYtmp1NotLow, CRYtmp1NotLowValue),
                                (CRYtmp2NotLow, CRYtmp2NotLowValue),
                                (CRYtmp3NotLow, CRYtmp3NotLowValue),

                                (CRYtmp0NotHigh, CRYtmp0NotHighValue),
                                (CRYtmp1NotHigh, CRYtmp1NotHighValue),
                                (CRYtmp2NotHigh, CRYtmp2NotHighValue),
                                (CRYtmp3NotHigh, CRYtmp3NotHighValue),

                                (CRYtempNotHigh, CRYtempNotHighValue),
                                (CRYtempHighFilter, CRYtempHighFilterValue),

                                (CRYtempHighOkLatch, CRYtempHighOkLatchValue),
                                (CRYtempHighOkLatchStatus, CRYtempHighOkLatchStatusValue),
                                (CRYtempHighOkLatchNeedsReset, CRYtempHighOkLatchNeedsResetValue),
                                (CRYhotLight, CRYhotLightValue),
                                (CRYhotLightPort, CRYhotLightPortValue),
                                (CRYheatPermit, CRYheatPermitValue),
                                (CRYheatPermitPort, CRYheatPermitPortValue),
                                (CRYheatPermitLockLight, CRYheatPermitLockLightValue),
                                (CRYheatPermitLockLightPort, CRYheatPermitLockLightPortValue),

                                (CRYtempNotLow, CRYtempNotLowValue),
                                (CRYtempLowFilter, CRYtempLowFilterValue),
                                (CRYtempLowOkLatch, CRYtempLowOkLatchValue),
                                (CRYtempLowOkLatchStatus, CRYtempLowOkLatchStatusValue),
                                (CRYtempLowOkLatchNeedsReset, CRYtempLowOkLatchNeedsResetValue),
                                (CRYcoldLight, CRYcoldLightValue),
                                (CRYcoldLightPort, CRYcoldLightPortValue),

                                (CRYrefPermit, CRYrefPermitValue),
                                (CRYrefPermitPort, CRYrefPermitPortValue),
                                (CRYrefPermitLockLight, CRYrefPermitLockLightValue),
                                (CRYrefPermitLockLightPort, CRYrefPermitLockLightPortValue),

                            ], 5, compare)

                            print("RESETS")

                            resets = []

                            if not tempNotHighValue:
                                compare = self.readAllChannels()
                                changeTemps = []

                                if not tmp0NotHighValue:
                                    tmp0Port.write(normalTempCurr)
                                    changeTemps.append((tmp0Port, normalTempCurr))
                                    changeTemps.append((tmp0Current, normalTempCurr * 1000))
                                    changeTemps.append((tmp0Temp, CtoK(normalTempCurr)))
                                if not tmp1NotHighValue:
                                    tmp1Port.write(normalTempCurr)
                                    changeTemps.append((tmp1Port, normalTempCurr))
                                    changeTemps.append((tmp1Current, normalTempCurr * 1000))
                                    changeTemps.append((tmp1Temp, CtoK(normalTempCurr)))
                                if not tmp2NotHighValue:
                                    tmp2Port.write(normalTempCurr)
                                    changeTemps.append((tmp2Port, normalTempCurr))
                                    changeTemps.append((tmp2Current, normalTempCurr * 1000))
                                    changeTemps.append((tmp2Temp, CtoK(normalTempCurr)))
                                if not tmp3NotHighValue:
                                    tmp3Port.write(normalTempCurr)
                                    changeTemps.append((tmp3Port, normalTempCurr))
                                    changeTemps.append((tmp3Current, normalTempCurr * 1000))
                                    changeTemps.append((tmp3Temp, CtoK(normalTempCurr)))

                                self.checkChange(changeTemps +
                                                 [(tmp0NotHigh, 1),
                                                  (tmp1NotHigh, 1),
                                                  (tmp2NotHigh, 1),
                                                  (tmp3NotHigh, 1),

                                                  (tempNotHigh, 1),

                                                  (tempHighFilter, 0),
                                                  (tempHighOkLatch, 0),
                                                  (tempHighOkLatchStatus, 2),
                                                  (tempHighOkLatchNeedsReset, 1),
                                                  (hotLight, 2),
                                                  (hotLightPort, 2),

                                                  ], 2, compare)
                                resets.append(resetTempHigh_w)

                            print("RESETS3")

                            if not tempNotLowValue:
                                compare = self.readAllChannels()
                                changeTemps = []
                                if not tmp0NotLowValue:
                                    tmp0Port.write(normalTempCurr)
                                    changeTemps.append((tmp0Port, normalTempCurr))
                                    changeTemps.append((tmp0Current, normalTempCurr * 1000))
                                    changeTemps.append((tmp0Temp, CtoK(normalTempCurr)))
                                if not tmp1NotLowValue:
                                    tmp1Port.write(normalTempCurr)
                                    changeTemps.append((tmp1Port, normalTempCurr))
                                    changeTemps.append((tmp1Current, normalTempCurr * 1000))
                                    changeTemps.append((tmp1Temp, CtoK(normalTempCurr)))
                                if not tmp2NotLowValue:
                                    tmp2Port.write(normalTempCurr)
                                    changeTemps.append((tmp2Port, normalTempCurr))
                                    changeTemps.append((tmp2Current, normalTempCurr * 1000))
                                    changeTemps.append((tmp2Temp, CtoK(normalTempCurr)))
                                if not tmp3NotLowValue:
                                    tmp3Port.write(normalTempCurr)
                                    changeTemps.append((tmp3Port, normalTempCurr))
                                    changeTemps.append((tmp3Current, normalTempCurr * 1000))
                                    changeTemps.append((tmp3Temp, CtoK(normalTempCurr)))

                                self.checkChange(changeTemps +
                                                 [(tmp0NotLow, 1),
                                                  (tmp1NotLow, 1),
                                                  (tmp2NotLow, 1),
                                                  (tmp3NotLow, 1),

                                                  (tempNotLow, 1),

                                                  (tempLowFilter, 0),
                                                  (tempLowOkLatch, 0),
                                                  (tempLowOkLatchStatus, 2),
                                                  (tempLowOkLatchNeedsReset, 1),
                                                  (coldLight, 2),
                                                  (coldLightPort, 2),

                                                  ], 1, compare)
                                resets.append(resetTempLow_w)

                            print("RESETS3 CRY")

                            # CRY

                            if not CRYtempNotHighValue:
                                compare = self.readAllChannels()
                                changeTemps = []

                                if not CRYtmp0NotHighValue:
                                    CRYtmp0Port.write(CRYnormalTempCurr)
                                    changeTemps.append((CRYtmp0Port, CRYnormalTempCurr))
                                    changeTemps.append((CRYtmp0Current, CRYnormalTempCurr * 1000))
                                    changeTemps.append((CRYtmp0Temp, CtoK(CRYnormalTempCurr)))
                                if not CRYtmp1NotHighValue:
                                    CRYtmp1Port.write(CRYnormalTempCurr)
                                    changeTemps.append((CRYtmp1Port, CRYnormalTempCurr))
                                    changeTemps.append((CRYtmp1Current, CRYnormalTempCurr * 1000))
                                    changeTemps.append((CRYtmp1Temp, CtoK(CRYnormalTempCurr)))
                                if not CRYtmp2NotHighValue:
                                    CRYtmp2Port.write(CRYnormalTempCurr)
                                    changeTemps.append((CRYtmp2Port, CRYnormalTempCurr))
                                    changeTemps.append((CRYtmp2Current, CRYnormalTempCurr * 1000))
                                    changeTemps.append((CRYtmp2Temp, CtoK(CRYnormalTempCurr)))
                                if not CRYtmp3NotHighValue:
                                    CRYtmp3Port.write(CRYnormalTempCurr)
                                    changeTemps.append((CRYtmp3Port, CRYnormalTempCurr))
                                    changeTemps.append((CRYtmp3Current, CRYnormalTempCurr * 1000))
                                    changeTemps.append((CRYtmp3Temp, CtoK(CRYnormalTempCurr)))

                                self.checkChange(changeTemps +
                                                 [(CRYtmp0NotHigh, 1),
                                                  (CRYtmp1NotHigh, 1),
                                                  (CRYtmp2NotHigh, 1),
                                                  (CRYtmp3NotHigh, 1),

                                                  (CRYtempNotHigh, 1),

                                                  (CRYtempHighFilter, 0),
                                                  (CRYtempHighOkLatch, 0),
                                                  (CRYtempHighOkLatchStatus, 2),
                                                  (CRYtempHighOkLatchNeedsReset, 1),
                                                  (CRYhotLight, 2),
                                                  (CRYhotLightPort, 2),

                                                  ], 2, compare)
                                resets.append(CRYresetTempHigh_w)

                            print("RESETS3.2 CRY")

                            if not CRYtempNotLowValue:
                                compare = self.readAllChannels()
                                changeTemps = []
                                if not CRYtmp0NotLowValue:
                                    CRYtmp0Port.write(CRYnormalTempCurr)
                                    changeTemps.append((CRYtmp0Port, CRYnormalTempCurr))
                                    changeTemps.append((CRYtmp0Current, CRYnormalTempCurr * 1000))
                                    changeTemps.append((CRYtmp0Temp, CtoK(CRYnormalTempCurr)))
                                if not CRYtmp1NotLowValue:
                                    CRYtmp1Port.write(CRYnormalTempCurr)
                                    changeTemps.append((CRYtmp1Port, CRYnormalTempCurr))
                                    changeTemps.append((CRYtmp1Current, CRYnormalTempCurr * 1000))
                                    changeTemps.append((CRYtmp1Temp, CtoK(CRYnormalTempCurr)))
                                if not CRYtmp2NotLowValue:
                                    CRYtmp2Port.write(CRYnormalTempCurr)
                                    changeTemps.append((CRYtmp2Port, CRYnormalTempCurr))
                                    changeTemps.append((CRYtmp2Current, CRYnormalTempCurr * 1000))
                                    changeTemps.append((CRYtmp2Temp, CtoK(CRYnormalTempCurr)))
                                if not CRYtmp3NotLowValue:
                                    CRYtmp3Port.write(CRYnormalTempCurr)
                                    changeTemps.append((CRYtmp3Port, CRYnormalTempCurr))
                                    changeTemps.append((CRYtmp3Current, CRYnormalTempCurr * 1000))
                                    changeTemps.append((CRYtmp3Temp, CtoK(CRYnormalTempCurr)))

                                self.checkChange(changeTemps +
                                                 [(CRYtmp0NotLow, 1),
                                                  (CRYtmp1NotLow, 1),
                                                  (CRYtmp2NotLow, 1),
                                                  (CRYtmp3NotLow, 1),

                                                  (CRYtempNotLow, 1),

                                                  (CRYtempLowFilter, 0),
                                                  (CRYtempLowOkLatch, 0),
                                                  (CRYtempLowOkLatchStatus, 2),
                                                  (CRYtempLowOkLatchNeedsReset, 1),
                                                  (CRYcoldLight, 2),
                                                  (CRYcoldLightPort, 2),

                                                  ], 1, compare)
                                resets.append(CRYresetTempLow_w)

                            print(resets)

                            print("RESETS4")

                            resetMode = not resetMode

                            if len(resets) > 0:
                                if resetMode:
                                    masterResetPort.write(1)
                                    self.sleep(1)
                                    masterResetPort.write(0)

                                else:
                                    self.pressChannels(resets)

                                resetMode = not resetMode

                            tmp0Port.write(normalTempCurr)
                            tmp1Port.write(normalTempCurr)
                            tmp2Port.write(normalTempCurr)
                            tmp3Port.write(normalTempCurr)

                            CRYtmp0Port.write(CRYnormalTempCurr)
                            CRYtmp1Port.write(CRYnormalTempCurr)
                            CRYtmp2Port.write(CRYnormalTempCurr)
                            CRYtmp3Port.write(CRYnormalTempCurr)

                            self.checkDefault()

            self.step("Cold Plate permits logic correct.")
            return True

        except ValueError as e:
            print(n)
            self.step("Cold Plate permits logic failed! Failed at %s. Error: %s " % (self.step_m, str(e)))
            return False


'''
class TestCryoPermits(Test):
    def __init__(self,tester,id):
        Test.__init__(self,tester,id)
        self.name = "TestCryoPermits"
        self.desc = "Test Cryo plate permits logic"

    def test(self):
            self.step(self.desc)


            tmp0Port = self.tester.testBox.plc.P2_IA0
            tmp1Port = self.tester.testBox.plc.P2_IA1
            tmp2Port = self.tester.testBox.plc.P2_IA2
            tmp3Port = self.tester.testBox.plc.P2_IA3

            tmp0Current = self.tester.plutoGateway.P2_ClpRtd0Current
            tmp1Current = self.tester.plutoGateway.P2_ClpRtd1Current
            tmp2Current = self.tester.plutoGateway.P2_ClpRtd2Current
            tmp3Current = self.tester.plutoGateway.P2_ClpRtd3Current

            tmp0Temp = self.tester.plutoGateway.P2_ClpRtd0Temp
            tmp1Temp = self.tester.plutoGateway.P2_ClpRtd1Temp
            tmp2Temp = self.tester.plutoGateway.P2_ClpRtd2Temp
            tmp3Temp = self.tester.plutoGateway.P2_ClpRtd3Temp

            tmp0NotLow = self.tester.plutoGateway.P2_ClpTemp0NotLow
            tmp1NotLow = self.tester.plutoGateway.P2_ClpTemp1NotLow
            tmp2NotLow = self.tester.plutoGateway.P2_ClpTemp2NotLow
            tmp3NotLow = self.tester.plutoGateway.P2_ClpTemp3NotLow

            tmp0NotHigh = self.tester.plutoGateway.P2_ClpTemp0NotHigh
            tmp1NotHigh = self.tester.plutoGateway.P2_ClpTemp1NotHigh
            tmp2NotHigh = self.tester.plutoGateway.P2_ClpTemp2NotHigh
            tmp3NotHigh = self.tester.plutoGateway.P2_ClpTemp3NotHigh

            tempNotHigh =  self.tester.plutoGateway.P2_ClpTempNotHigh
            tempHighFilter =  self.tester.plutoGateway.P2_ClpTempHighFilter

            tempHighOkLatch = self.tester.plutoGateway.P2_ClpTempHighOkLatch
            tempHighOkLatchStatus = self.tester.plutoGateway.P2_ClpTempHighOkLatchStatus
            tempHighOkLatchNeedsReset = self.tester.plutoGateway.P2_ClpTempHighOkLatchNeedsReset
            hotLight = self.tester.plutoGateway.P2_ClpHotLight
            hotLightPort =  self.tester.testBox.plc.P2_IQ14

            resetTempHigh_w =  self.tester.plutoGateway.P2_ResetClpHigh_w

            heatPermitLockLight = self.tester.plutoGateway.P2_ClpHeatLockLight
            heatPermitLockLightPort =  self.tester.testBox.plc.P2_IQ16
            heatPermit = self.tester.plutoGateway.P2_ClpHeatPerm
            heatPermitPort =  self.tester.testBox.plc.P2_Q0


            tempNotLow =  self.tester.plutoGateway.P2_ClpTempNotLow
            tempLowFilter =  self.tester.plutoGateway.P2_ClpTempLowFilter
            tempLowOkLatch = self.tester.plutoGateway.P2_ClpTempLowOkLatch
            tempLowOkLatchStatus = self.tester.plutoGateway.P2_ClpTempLowOkLatchStatus
            tempLowOkLatchNeedsReset = self.tester.plutoGateway.P2_ClpTempLowOkLatchNeedsReset
            coldLight = self.tester.plutoGateway.P2_ClpColdLight
            coldLightPort =  self.tester.testBox.plc.P2_IQ15


            resetTempLow_w =  self.tester.plutoGateway.P2_ResetClpLow_w

            refPermitLockLight = self.tester.plutoGateway.P2_ClpFrigLockLight
            refPermitLockLightPort = self.tester.testBox.plc.P2_IQ17
            refPermit = self.tester.plutoGateway.P2_ClpRefPerm
            refPermitPort =  self.tester.testBox.plc.P2_Q1



            hexVacReset_w = self.tester.plutoGateway.P3_ResetHexVac_w

            cryVacReset_w = self.tester.plutoGateway.P3_ResetCryVac_w


            masterResetPort = self.tester.testBox.plc.P2_I7


            noTempCurr= 2.5 #mA
            lowTempCurr = KtoC(200)
            normalTempCurr = KtoC(250)
            highTempCurr = KtoC(300)

            tmp0PortValues = [noTempCurr,lowTempCurr,normalTempCurr,highTempCurr]
            tmp1PortValues = [noTempCurr,lowTempCurr,normalTempCurr,highTempCurr]
            tmp2PortValues = [noTempCurr,lowTempCurr,normalTempCurr,highTempCurr]
            tmp3PortValues = [noTempCurr,lowTempCurr,normalTempCurr,highTempCurr]

            resetMode = True #["soft", "hard"]


            self.setDefault(check=False)


            lowLimitCurr = KtoC(228)
            highLimitCurr = KtoC(295)
            zeroLimitCurr = 3

            n =0
            a=0
            try:
                for tmp0PortValue in tmp0PortValues:
                    for tmp1PortValue in tmp1PortValues:
                        for tmp2PortValue in tmp2PortValues:
                            for tmp3PortValue in tmp3PortValues:

                                            n=n+1
                                            print("--------------------------------------------------------------------------",n)

                                            if n<18:
                                                continue

                                            def moreThanAre(portsValues,values,thresold):
                                                for value in values:
                                                    n=0
                                                    for portValue in portsValues:
                                                        if portValue==value:
                                                            n+=1
                                                    if n>thresold:
                                                        return True


                                            if moreThanAre([tmp0PortValue,tmp1PortValue,tmp2PortValue,tmp3PortValue],[noTempCurr,lowTempCurr,highTempCurr],2):
                                                continue

                                            #a+=1
                                            #print(a,a*15/60/60)
                                            #continue

                                            compare = self.readAllChannels()

                                            tmp0Port.write(tmp0PortValue)
                                            tmp1Port.write(tmp1PortValue)
                                            tmp2Port.write(tmp2PortValue)
                                            tmp3Port.write(tmp3PortValue)

                                            tmp0NotLowValue = int(tmp0PortValue > lowLimitCurr)
                                            tmp1NotLowValue = int(tmp1PortValue > lowLimitCurr)
                                            tmp2NotLowValue = int(tmp2PortValue > lowLimitCurr)
                                            tmp3NotLowValue = int(tmp3PortValue > lowLimitCurr)

                                            tmp0NotHighValue =int(tmp0PortValue < highLimitCurr and tmp0PortValue > zeroLimitCurr)
                                            tmp1NotHighValue =int(tmp1PortValue < highLimitCurr and tmp1PortValue > zeroLimitCurr)
                                            tmp2NotHighValue =int(tmp2PortValue < highLimitCurr and tmp2PortValue > zeroLimitCurr)
                                            tmp3NotHighValue =int(tmp3PortValue < highLimitCurr and tmp3PortValue > zeroLimitCurr)

                                            tempNotHighValue = int((int(tmp0NotHighValue) + int(tmp1NotHighValue) + int(tmp2NotHighValue) +int(tmp3NotHighValue)) >=3)
                                            tempHighFilterValue = not tempNotHighValue

                                            tempHighOkLatchValue = tempNotHighValue
                                            tempHighOkLatchStatusValue = not tempHighOkLatchValue
                                            tempHighOkLatchNeedsResetValue = 0
                                            hotLightValue = tempHighOkLatchStatusValue
                                            hotLightPortValue = tempHighOkLatchStatusValue

                                            heatPermitValue = tempNotHighValue
                                            heatPermitPortValue = heatPermitValue
                                            heatPermitLockLightValue = not heatPermitValue
                                            heatPermitLockLightPortValue =  not heatPermitValue

                                            tempNotLowValue = int((int(tmp0NotLowValue) + int(tmp1NotLowValue) + int(tmp2NotLowValue) +int(tmp3NotLowValue)) >=3)
                                            tempLowFilterValue = not tempNotLowValue

                                            tempLowOkLatchValue = tempNotLowValue
                                            tempLowOkLatchStatusValue = not tempLowOkLatchValue
                                            tempLowOkLatchNeedsResetValue = 0
                                            coldLightValue = tempLowOkLatchStatusValue
                                            coldLightPortValue = tempLowOkLatchStatusValue


                                            refPermitValue = tempNotLowValue and 1 and 1
                                            refPermitPortValue = refPermitValue
                                            refPermitLockLightValue = not refPermitValue
                                            refPermitLockLightPortValue = not refPermitValue



                                            print("WRITE")


                                            # Should change immediately
                                            self.checkChange([
                                                (tmp0Port, tmp0PortValue),
                                                (tmp1Port, tmp1PortValue),
                                                (tmp2Port, tmp2PortValue),
                                                (tmp3Port, tmp3PortValue),

                                                (tmp0Current, tmp0PortValue*1000),
                                                (tmp1Current, tmp1PortValue*1000),
                                                (tmp2Current, tmp2PortValue*1000),
                                                (tmp3Current, tmp3PortValue*1000),

                                                (tmp0Temp, CtoK(tmp0PortValue)),
                                                (tmp1Temp, CtoK(tmp1PortValue)),
                                                (tmp2Temp, CtoK(tmp2PortValue)),
                                                (tmp3Temp, CtoK(tmp3PortValue)),

                                                (tmp0NotLow,tmp0NotLowValue ),
                                                (tmp1NotLow,     tmp1NotLowValue ),
                                                (tmp2NotLow,   tmp2NotLowValue),
                                                (tmp3NotLow,       tmp3NotLowValue),

                                                (tmp0NotHigh,       tmp0NotHighValue),
                                                (tmp1NotHigh,    tmp1NotHighValue),
                                                (tmp2NotHigh, tmp2NotHighValue),
                                                (tmp3NotHigh, tmp3NotHighValue),

                                                (tempNotHigh, tempNotHighValue),

                                                (tempNotLow, tempNotLowValue),


                                                ], 1, compare)

                                            print("IMEDIATO")


                                            # Permits should not change during 9 seconds
                                            self.checkDuring([(refPermitPort, 1),
                                                              (refPermit,1,),
                                                              (heatPermitPort,1),
                                                              (heatPermit,1),
                                                              ], 6)

                                            print("6s")

                                            self.pressChannels([resetTempHigh_w, resetTempLow_w, hexVacReset_w, cryVacReset_w])


                                            self.checkChange([
                                                (tmp0Port, tmp0PortValue),
                                                (tmp1Port, tmp1PortValue),
                                                (tmp2Port, tmp2PortValue),
                                                (tmp3Port, tmp3PortValue),

                                                (tmp0Current, tmp0PortValue*1000),
                                                (tmp1Current, tmp1PortValue*1000),
                                                (tmp2Current, tmp2PortValue*1000),
                                                (tmp3Current, tmp3PortValue*1000),

                                                (tmp0Temp, CtoK(tmp0PortValue)),
                                                (tmp1Temp, CtoK(tmp1PortValue)),
                                                (tmp2Temp, CtoK(tmp2PortValue)),
                                                (tmp3Temp, CtoK(tmp3PortValue)),

                                                (tmp0NotLow,tmp0NotLowValue ),
                                                (tmp1NotLow,     tmp1NotLowValue ),
                                                (tmp2NotLow,   tmp2NotLowValue),
                                                (tmp3NotLow,       tmp3NotLowValue),

                                                (tmp0NotHigh, tmp0NotHighValue),
                                                (tmp1NotHigh, tmp1NotHighValue),
                                                (tmp2NotHigh, tmp2NotHighValue),
                                                (tmp3NotHigh, tmp3NotHighValue),

                                                (tempNotHigh, tempNotHighValue),
                                                (tempHighFilter,   tempHighFilterValue),

                                                (tempHighOkLatch,  tempHighOkLatchValue),
                                                (tempHighOkLatchStatus,   tempHighOkLatchStatusValue),
                                                (tempHighOkLatchNeedsReset, tempHighOkLatchNeedsResetValue),
                                                (hotLight,  hotLightValue),
                                                (hotLightPort,   hotLightPortValue),
                                                (heatPermit,   heatPermitValue),
                                                (heatPermitPort,   heatPermitPortValue),
                                                (heatPermitLockLight,   heatPermitLockLightValue),
                                                (heatPermitLockLightPort, heatPermitLockLightPortValue),

                                                (tempNotLow, tempNotLowValue),
                                                (tempLowFilter,  tempLowFilterValue),
                                                (tempLowOkLatch,  tempLowOkLatchValue),
                                                (tempLowOkLatchStatus,  tempLowOkLatchStatusValue),
                                                (tempLowOkLatchNeedsReset, tempLowOkLatchNeedsResetValue),
                                                (coldLight,  coldLightValue),
                                                (coldLightPort, coldLightPortValue),

                                                (refPermit,  refPermitValue),
                                                (refPermitPort, refPermitPortValue),
                                                (refPermitLockLight, refPermitLockLightValue),
                                                (refPermitLockLightPort, refPermitLockLightPortValue),


                                                ], 5, compare)

                                            print("RESETS")


                                            resets=[]



                                            if not tempNotHighValue:
                                                compare = self.readAllChannels()
                                                changeTemps = []

                                                if not tmp0NotHighValue:
                                                    tmp0Port.write(normalTempCurr)
                                                    changeTemps.append((tmp0Port, normalTempCurr))
                                                    changeTemps.append((tmp0Current, normalTempCurr*1000))
                                                    changeTemps.append((tmp0Temp, CtoK(normalTempCurr)))
                                                if not tmp1NotHighValue:
                                                    tmp1Port.write(normalTempCurr)
                                                    changeTemps.append((tmp1Port, normalTempCurr))
                                                    changeTemps.append((tmp1Current, normalTempCurr*1000))
                                                    changeTemps.append((tmp1Temp, CtoK(normalTempCurr)))
                                                if not tmp2NotHighValue:
                                                    tmp2Port.write(normalTempCurr)
                                                    changeTemps.append((tmp2Port, normalTempCurr))
                                                    changeTemps.append((tmp2Current, normalTempCurr*1000))
                                                    changeTemps.append((tmp2Temp, CtoK(normalTempCurr)))
                                                if not tmp3NotHighValue:
                                                    tmp3Port.write(normalTempCurr)
                                                    changeTemps.append((tmp3Port, normalTempCurr))
                                                    changeTemps.append((tmp3Current, normalTempCurr*1000))
                                                    changeTemps.append((tmp3Temp, CtoK(normalTempCurr)))

                                                self.checkChange(changeTemps +
                                                                 [  (tmp0NotHigh, 1),
                                                                    (tmp1NotHigh, 1),
                                                                    (tmp2NotHigh, 1),
                                                                    (tmp3NotHigh, 1),

                                                                    (tempNotHigh, 1),

                                                                    (tempHighFilter,0),
                                                                    (tempHighOkLatch,0),
                                                                    (tempHighOkLatchStatus,2),
                                                                    (tempHighOkLatchNeedsReset, 1),
                                                                    (hotLight,2),
                                                                    (hotLightPort,2),

                                                                  ], 2, compare)
                                                resets.append(resetTempHigh_w)

                                            print("RESETS3")

                                            if not tempNotLowValue:
                                                compare = self.readAllChannels()
                                                changeTemps = []
                                                if not tmp0NotLowValue:
                                                    tmp0Port.write(normalTempCurr)
                                                    changeTemps.append((tmp0Port, normalTempCurr))
                                                    changeTemps.append((tmp0Current, normalTempCurr*1000))
                                                    changeTemps.append((tmp0Temp, CtoK(normalTempCurr)))
                                                if not tmp1NotLowValue:
                                                    tmp1Port.write(normalTempCurr)
                                                    changeTemps.append((tmp1Port, normalTempCurr))
                                                    changeTemps.append((tmp1Current, normalTempCurr*1000))
                                                    changeTemps.append((tmp1Temp, CtoK(normalTempCurr)))
                                                if not tmp2NotLowValue:
                                                    tmp2Port.write(normalTempCurr)
                                                    changeTemps.append((tmp2Port, normalTempCurr))
                                                    changeTemps.append((tmp2Current, normalTempCurr*1000))
                                                    changeTemps.append((tmp2Temp, CtoK(normalTempCurr)))
                                                if not tmp3NotLowValue:
                                                    tmp3Port.write(normalTempCurr)
                                                    changeTemps.append((tmp3Port, normalTempCurr))
                                                    changeTemps.append((tmp3Current, normalTempCurr*1000))
                                                    changeTemps.append((tmp3Temp, CtoK(normalTempCurr)))

                                                self.checkChange(changeTemps +
                                                                 [(tmp0NotLow, 1),
                                                                  (tmp1NotLow, 1),
                                                                  (tmp2NotLow, 1),
                                                                  (tmp3NotLow, 1),

                                                                  (tempNotLow, 1),

                                                                  (tempLowFilter, 0),
                                                                  (tempLowOkLatch, 0),
                                                                  (tempLowOkLatchStatus, 2),
                                                                  (tempLowOkLatchNeedsReset, 1),
                                                                  (coldLight, 2),
                                                                  (coldLightPort, 2),

                                                                  ], 1, compare)
                                                resets.append(resetTempLow_w)


                                            print(resets)

                                            print("RESETS4")

                                            resetMode=not resetMode


                                            if len(resets)>0:
                                                if resetMode == "hard":
                                                    masterResetPort.write(1)
                                                    self.sleep(1)
                                                    masterResetPort.write(0)

                                                else:
                                                    self.pressChannels(resets)

                                            tmp0Port.write(normalTempCurr)
                                            tmp1Port.write(normalTempCurr)
                                            tmp2Port.write(normalTempCurr)
                                            tmp3Port.write(normalTempCurr)

                                            self.checkDefault()


                self.step("Cold Plate permits logic correct.")
                return True

            except ValueError as e:
                print (n)
                self.step("Cold Plate permits logic failed! Failed at %s. Error: %s "%(self.step_m,str(e)))
                return False
'''


class TestVacuumToRefPermits(Test):
    def __init__(self, tester, id):
        Test.__init__(self, tester, id)
        self.name = "TestVacuumToRefPermits"
        self.desc = "Test Vacuum to refrigeration permits logic"

    def test(self):
        self.step(self.desc)

        resetTempHigh_w = self.tester.plutoGateway.P2_ResetClpHigh_w

        resetTempLow_w = self.tester.plutoGateway.P2_ResetClpLow_w

        coldRefPermitLockLight = self.tester.plutoGateway.P2_ClpFrigLockLight
        coldRefPermitLockLightPort = self.tester.testBox.plc.P2_IQ17
        coldRefPermit = self.tester.plutoGateway.P2_ClpRefPerm
        coldRefPermitPort = self.tester.testBox.plc.P2_Q1

        cryRefPermitLockLight = self.tester.plutoGateway.P3_CryFrigLockLight
        cryRefPermitLockLightPort = self.tester.testBox.plc.P3_IQ17
        cryRefPermit = self.tester.plutoGateway.P3_CryRefPerm
        cryRefPermitPort = self.tester.testBox.plc.P3_Q1

        hexVacOk = self.tester.plutoGateway.P3_HexVacOk
        hexVacOkPort = self.tester.testBox.plc.P3_I5
        hexVacOkLatch = self.tester.plutoGateway.P3_HexVacOkLatch
        hexVacLatchStatus = self.tester.plutoGateway.P3_HexVacOkLatchStatus
        hexVacLatchNeedsReset = self.tester.plutoGateway.P3_HexVacOkLatchNeedsReset
        hexVavBadLight = self.tester.plutoGateway.P3_HexVacBadLight
        hexVacReset_w = self.tester.plutoGateway.P3_ResetHexVac_w

        cryVacOk = self.tester.plutoGateway.P3_CryVacOk
        cryVacOkPort = self.tester.testBox.plc.P3_I6
        cryVacOkLatch = self.tester.plutoGateway.P3_CryVacOkLatch
        cryVacLatchStatus = self.tester.plutoGateway.P3_CryVacOkLatchStatus
        cryVacLatchNeedsReset = self.tester.plutoGateway.P3_CryVacOkLatchNeedsReset
        cryVavBadLight = self.tester.plutoGateway.P3_CryVacBadLight
        cryVacReset_w = self.tester.plutoGateway.P3_ResetCryVac_w

        masterResetPort = self.tester.testBox.plc.P2_I7

        hexVacOkPortValues = [0, 1]
        cryVacOkPortValues = [0, 1]

        resetMode = True  # ["soft", "hard"]

        self.setDefault(check=False)

        n = 0

        try:
            for hexVacOkPortValue in hexVacOkPortValues:
                for cryVacOkPortValue in cryVacOkPortValues:

                    n = n + 1
                    print("--------------------------------------------------------------------------", n)

                    compare = self.readAllChannels()

                    hexVacOkPort.write(hexVacOkPortValue)
                    cryVacOkPort.write(cryVacOkPortValue)

                    hexVacOkLatchValue = hexVacOkPortValue
                    hexVacLatchStatusValue = not hexVacOkPortValue
                    hexVacLatchNeedsResetValue = 0
                    hexVavBadLightValue = not hexVacOkPortValue

                    cryVacOkLatchValue = cryVacOkPortValue
                    cryVacLatchStatusValue = not cryVacOkPortValue
                    cryVacLatchNeedsResetValue = 0
                    cryVavBadLightValue = not cryVacOkPortValue

                    refPermitValue = 1 and hexVacOkPortValue and cryVacOkPortValue
                    refPermitPortValue = refPermitValue
                    refPermitLockLightValue = not refPermitValue
                    refPermitLockLightPortValue = not refPermitValue

                    self.pressChannels([resetTempHigh_w, resetTempLow_w, hexVacReset_w, cryVacReset_w])

                    # Should change immediately
                    self.checkChange([

                        (hexVacOkPort, hexVacOkPortValue),
                        (hexVacOk, hexVacOkPortValue),
                        (hexVacOkLatch, hexVacOkLatchValue),
                        (hexVacLatchStatus, hexVacLatchStatusValue),
                        (hexVacLatchNeedsReset, hexVacLatchNeedsResetValue),
                        (hexVavBadLight, hexVavBadLightValue),

                        (cryVacOkPort, cryVacOkPortValue),
                        (cryVacOk, cryVacOkPortValue),
                        (cryVacOkLatch, cryVacOkLatchValue),
                        (cryVacLatchStatus, cryVacLatchStatusValue),
                        (cryVacLatchNeedsReset, cryVacLatchNeedsResetValue),
                        (cryVavBadLight, cryVavBadLightValue),

                        (coldRefPermit, refPermitValue),
                        (coldRefPermitPort, refPermitPortValue),
                        (coldRefPermitLockLight, refPermitLockLightValue),
                        (coldRefPermitLockLightPort, refPermitLockLightPortValue),

                        (cryRefPermit, refPermitValue),
                        (cryRefPermitPort, refPermitPortValue),
                        (cryRefPermitLockLight, refPermitLockLightValue),
                        (cryRefPermitLockLightPort, refPermitLockLightPortValue),

                    ], 1, compare)

                    resets = []

                    if not hexVacOkPortValue:
                        compare = self.readAllChannels()
                        hexVacOkPort.write(1)

                        self.checkChange([(hexVacOkPort, 1),
                                          (hexVacOk, 1),

                                          (hexVacOkLatch, 0),
                                          (hexVacLatchStatus, 2),
                                          (hexVacLatchNeedsReset, 1),
                                          (hexVavBadLight, 2),

                                          ], 1, compare)
                        resets.append(hexVacReset_w)

                    if not cryVacOkPortValue:
                        compare = self.readAllChannels()
                        cryVacOkPort.write(1)

                        self.checkChange([(cryVacOkPort, 1),
                                          (cryVacOk, 1),

                                          (cryVacOkLatch, 0),
                                          (cryVacLatchStatus, 2),
                                          (cryVacLatchNeedsReset, 1),
                                          (cryVavBadLight, 2),

                                          ], 1, compare)
                        resets.append(cryVacReset_w)

                    resetMode = not resetMode

                    if len(resets) > 0:
                        if resetMode == "hard":
                            masterResetPort.write(1)
                            self.sleep(1)
                            masterResetPort.write(0)

                        else:
                            self.pressChannels(resets)

                    self.checkDefault()

            self.step("Vacuum to refrigeration permits logiccorrect.")

            return True

        except ValueError as e:
            print(n)
            self.step("Vacuum to refrigeration permits logic failed! Failed at %s. Error: %s " % (self.step_m, str(e)))
            return False


class TestPermitsBlock(Test):
    def __init__(self, tester, id):
        Test.__init__(self, tester, id)
        self.name = "TestPermitsBlock"
        self.desc = "Test Permits Block logic"

    def test(self):
        self.step(self.desc)

        blocks = [[self.tester.plutoGateway.P1_UtPowerPermBlockSet,
                   self.tester.plutoGateway.P1_UtPowerPermBlockSet_w,
                   self.tester.plutoGateway.P1_UtPowerPermBlockReset,
                   self.tester.plutoGateway.P1_UtPowerPermBlockReset_w,
                   self.tester.plutoGateway.P1_UtPowerPermBlock,
                   self.tester.plutoGateway.P1_UtPowerPerm,
                   self.tester.testBox.plc.P1_IQ16,
                   self.tester.testBox.plc.P1_Q0],

                  [self.tester.plutoGateway.P1_RebPowerPermBlockSet,
                   self.tester.plutoGateway.P1_RebPowerPermBlockSet_w,
                   self.tester.plutoGateway.P1_RebPowerPermBlockReset,
                   self.tester.plutoGateway.P1_RebPowerPermBlockReset_w,
                   self.tester.plutoGateway.P1_RebPowerPermBlock,
                   self.tester.plutoGateway.P1_RebPowerPerm,
                   self.tester.testBox.plc.P1_IQ17,
                   self.tester.testBox.plc.P1_Q1],

                  [self.tester.plutoGateway.P1_CoolantValveBlockSet,
                   self.tester.plutoGateway.P1_CoolantValveBlockSet_w,
                   self.tester.plutoGateway.P1_CoolantValveBlockReset,
                   self.tester.plutoGateway.P1_CoolantValveBlockReset_w,
                   self.tester.plutoGateway.P1_CoolantValveBlock,
                   self.tester.plutoGateway.P1_CoolantValve,
                   self.tester.testBox.plc.P1_Q2,
                   self.tester.testBox.plc.P1_Q2]]

        try:

            self.setDefault()

            for block in blocks:
                set_w = block[1]
                reset_w = block[3]
                blockStatus = block[4]
                perm = block[5]
                permLight = block[6]
                permPort = block[6]

                compare = self.readAllChannels()
                set_w.press()
                self.checkChange([(blockStatus, 1), (perm, 0), (permLight, 0), (permPort, 0)], 1, compare)

                reset_w.press()

                self.checkDefault()



        except Exception as e:
            self.step("Permits Block logic failed! Failed at %s. Error: %s " % (self.step_m, str(e)))
            return False

        blocks = [[self.tester.plutoGateway.P2_ClpHeatPermBlockSet,
                   self.tester.plutoGateway.P2_ClpHeatPermBlockSet_w,
                   self.tester.plutoGateway.P2_ClpHeatPermBlockReset,
                   self.tester.plutoGateway.P2_ClpHeatPermBlockReset_w,
                   self.tester.plutoGateway.P2_ClpHeatPermBlock,
                   self.tester.plutoGateway.P2_ClpHeatLockLight,
                   self.tester.plutoGateway.P2_ClpHeatPerm,
                   self.tester.testBox.plc.P2_IQ16,
                   self.tester.testBox.plc.P2_Q0],

                  [self.tester.plutoGateway.P2_ClpRefPermBlockSet,
                   self.tester.plutoGateway.P2_ClpRefPermBlockSet_w,
                   self.tester.plutoGateway.P2_ClpRefPermBlockReset,
                   self.tester.plutoGateway.P2_ClpRefPermBlockReset_w,
                   self.tester.plutoGateway.P2_ClpRefPermBlock,
                   self.tester.plutoGateway.P2_ClpFrigLockLight,
                   self.tester.plutoGateway.P2_ClpRefPerm,
                   self.tester.testBox.plc.P2_IQ17,
                   self.tester.testBox.plc.P2_Q1],

                  [self.tester.plutoGateway.P3_CryHeatPermBlockSet,
                   self.tester.plutoGateway.P3_CryHeatPermBlockSet_w,
                   self.tester.plutoGateway.P3_CryHeatPermBlockReset,
                   self.tester.plutoGateway.P3_CryHeatPermBlockReset_w,
                   self.tester.plutoGateway.P3_CryHeatPermBlock,
                   self.tester.plutoGateway.P3_CryHeatLockLight,
                   self.tester.plutoGateway.P3_CryHeatPerm,
                   self.tester.testBox.plc.P3_IQ16,
                   self.tester.testBox.plc.P3_Q0],

                  [self.tester.plutoGateway.P3_CryRefPermBlockSet,
                   self.tester.plutoGateway.P3_CryRefPermBlockSet_w,
                   self.tester.plutoGateway.P3_CryRefPermBlockReset,
                   self.tester.plutoGateway.P3_CryRefPermBlockReset_w,
                   self.tester.plutoGateway.P3_CryRefPermBlock,
                   self.tester.plutoGateway.P3_CryFrigLockLight,
                   self.tester.plutoGateway.P3_CryRefPerm,
                   self.tester.testBox.plc.P3_IQ17,
                   self.tester.testBox.plc.P3_Q1]
                  ]

        try:

            self.setDefault()

            for block in blocks:
                set_w = block[1]
                reset_w = block[3]
                blockStatus = block[4]
                lockLight = block[5]
                perm = block[6]
                lockLightPort = block[7]
                permPort = block[8]

                compare = self.readAllChannels()
                set_w.press()
                self.checkChange([(blockStatus, 1), (lockLight, 1), (perm, 0), (lockLightPort, 1), (permPort, 0)], 1,
                                 compare)

                reset_w.press()

                self.checkDefault()

            self.step("Permits Block logic correct.")
            return True

        except Exception as e:
            self.step("Permits Block logic failed! Failed at %s. Error: %s " % (self.step_m, str(e)))
            return False
