from tester import Test
import random



class TestPlutoGatewayConfig(Test):
    def __init__(self, tester, id):
        Test.__init__(self, tester, id)
        self.name = "TestPlutoGatewayConfig"
        self.expected_config = [0, 7, 0, 0, 0, 257, 258, 259, 260, 0, 0, 0, 0, 0, 356, 513, 514, 515, 516, 517, 518,
                                519, 520, 0, 612, 769,
                                770, 771, 772, 773, 774, 775, 776, 777, 868, 0, 0, 100, 0, 0, 0, 1]



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
        self.desc = "Check Pluto Gateway sees Pluto D20 as node 1 and 3."

    def test(self):
        good = True
        for n in [1, 3]:
            plc = self.tester.plutoGateway.read_bit(36, 1, n)

            if plc == 0:
                self.step("Pluto Gateway doens't see PLC %d as node %d" % (n, n))
                good = False

        if not good:
            return False

        self.step(("Pluto Gateway sees all 3 D20 PLCs as nodes 1,3."))
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


        resetLeak_w = self.tester.plutoGateway.P1_ResetLeak_w

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

        resetTemp_w = self.tester.plutoGateway.P1_ResetTemp_w

        #TODO test hard reset mode masterResetPort = self.tester.testBox.plc.P3_I7
        masterResetPort = self.tester.testBox.plc.P3_IA0
        masterReset = self.tester.plutoGateway.P3_MasterResetButton

        valvePort = self.tester.testBox.plc.P1_Q2
        valve = self.tester.plutoGateway.P1_CoolantValve

        utPermitPort = self.tester.testBox.plc.P1_Q0
        utPermit = self.tester.plutoGateway.P1_UtPowerPerm

        noLeakPortValues = [0, 1]
        noLeakFaultPortValues = [0, 1]

        tmp0PortValues = [0, 1]
        tmp1PortValues = [0, 1]
        tmp2PortValues = [0, 1]
        tmp3PortValues = [0, 1]

        resetMode = False  # ["soft", "hard"]

        self.setDefault(check=False)

        hexVacReset_w = self.tester.plutoGateway.P3_ResetHexVac_w
        cryVacReset_w = self.tester.plutoGateway.P3_ResetCryVac_w

        hexVacReset_w.press()
        cryVacReset_w.press()

        n = 0

        try:
            for noLeakPortValue in noLeakPortValues:
                for noLeakFaultPortValue in noLeakFaultPortValues:
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

                                            compare = []

                                            noLeakPort.write(noLeakPortValue)
                                            noLeakFaultPort.write(noLeakFaultPortValue)
                                            tmp0Port.write(tmp0PortValue)
                                            tmp1Port.write(tmp1PortValue)
                                            tmp2Port.write(tmp2PortValue)
                                            tmp3Port.write(tmp3PortValue)

                                            # No permit output should change during 7 seconds

                                            self.checkDuring([(valvePort, 1),
                                                              (valve, 1,),
                                                              (utPermitPort, 1),
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


                                            tempOkValue = (
                                                                      tmp0PortValue + tmp1PortValue + tmp2PortValue + tmp3PortValue) >= 3
                                            tempHighFilterValue = not tempOkValue
                                            tempOkLatchValue = tempOkValue
                                            tempOkLatcStatusValue = not tempOkValue
                                            tempOkLatchNeedsResetValue = 0

                                            tempIndicatorValue = tempOkLatcStatusValue

                                            valvePortValue = leakFaultOkLatchValue and leakOkLatchValue
                                            valveValue = valvePortValue

                                            utPermitPortValue = tempOkLatchValue and leakFaultOkLatchValue and leakOkLatchValue
                                            utPermitValue = utPermitPortValue

                                            # Try to reset but this must have no effect
                                            self.pressChannels(
                                                [resetTemp_w, resetLeak_w, masterResetPort])


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

                                                # Outputs

                                                (valvePort, valvePortValue),
                                                (valve, valveValue),
                                                (utPermitPort, utPermitPortValue),
                                                (utPermit, utPermitValue),

                                            ], 5, compare)

                                            print("NICE2")
                                            resets = []

                                            if not noLeakPortValue:
                                                compare = []
                                                 
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

                                                                  (valvePort, 0),
                                                                  (valve, 0),
                                                                  (utPermitPort, 0),
                                                                  (utPermit, 0),

                                                                  ], 1, compare)
                                                resets.append(resetLeak_w)

                                            print("NICE3")

                                            if not noLeakFaultPortValue:
                                                compare = []
                                                 
                                                noLeakFaultPort.write(1)
                                                self.checkChange([(noLeakFaultPort, 1),
                                                                  (noLeakFault, 1),

                                                                  (leakFaultFilter, 0),
                                                                  (leakFaultOkLatch, 0),
                                                                  (leakFaultOkLatchStatus, 2),
                                                                  (leakFaultOkLatchNeedsReset, 1),

                                                                  (valvePort, 0),
                                                                  (valve, 0),
                                                                  (utPermitPort, 0),
                                                                  (utPermit, 0),

                                                                  ], 1, compare)
                                                resets.append(resetLeak_w)

                                            print("NICE4")


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

                                                                  (utPermitPort, 0),
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

                                                #TODO test hard reset mode resetMode = not resetMode

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


class TestVacuumToRefPermits(Test):
    def __init__(self, tester, id):
        Test.__init__(self, tester, id)
        self.name = "TestVacuumToRefPermits"
        self.desc = "Test Vacuum to refrigeration permits logic"

    def test(self):
        self.step(self.desc)

        coldRefPermitLockLight = self.tester.plutoGateway.P3_ClpFrigLockLight
        coldRefPermit = self.tester.plutoGateway.P3_ClpRefPerm
        coldRefPermitPort = self.tester.testBox.plc.P3_Q0

        cryRefPermitLockLight = self.tester.plutoGateway.P3_CryFrigLockLight
        cryRefPermit = self.tester.plutoGateway.P3_CryRefPerm
        cryRefPermitPort = self.tester.testBox.plc.P3_Q1



        hexVacOk = self.tester.plutoGateway.P3_HexVacOk
        hexVacOkPort = self.tester.testBox.plc.P3_I5
        hexVacOkLatch = self.tester.plutoGateway.P3_HexVacOkLatch
        hexVacLatchStatus = self.tester.plutoGateway.P3_HexVacOkLatchStatus
        hexVacLatchNeedsReset = self.tester.plutoGateway.P3_HexVacOkLatchNeedsReset
        hexVacReset_w = self.tester.plutoGateway.P3_ResetHexVac_w

        cryVacOk = self.tester.plutoGateway.P3_CryVacOk
        cryVacOkPort = self.tester.testBox.plc.P3_I6
        cryVacOkLatch = self.tester.plutoGateway.P3_CryVacOkLatch
        cryVacLatchStatus = self.tester.plutoGateway.P3_CryVacOkLatchStatus
        cryVacLatchNeedsReset = self.tester.plutoGateway.P3_CryVacOkLatchNeedsReset
        cryVacReset_w = self.tester.plutoGateway.P3_ResetCryVac_w

        #TODO test hard reset mode masterResetPort = self.tester.testBox.plc.P3_I7
        masterResetPort = self.tester.testBox.plc.P3_IA0
        masterReset = self.tester.plutoGateway.P3_MasterResetButton

        hexVacOkPortValues = [0, 1]
        cryVacOkPortValues = [0, 1]

        resetMode = False  # ["soft", "hard"]

        self.setDefault(check=False)
        hexVacReset_w.press()
        cryVacReset_w.press()

        n = 0

        try:
            for hexVacOkPortValue in hexVacOkPortValues:
                for cryVacOkPortValue in cryVacOkPortValues:

                    n = n + 1
                    print("--------------------------------------------------------------------------", n)

                    compare = []
                     

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

                    self.pressChannels([ hexVacReset_w, cryVacReset_w])

                    # Should change immediately
                    self.checkChange([

                        (hexVacOkPort, hexVacOkPortValue),
                        (hexVacOk, hexVacOkPortValue),
                        (hexVacOkLatch, hexVacOkLatchValue),
                        (hexVacLatchStatus, hexVacLatchStatusValue),
                        (hexVacLatchNeedsReset, hexVacLatchNeedsResetValue),


                        (cryVacOkPort, cryVacOkPortValue),
                        (cryVacOk, cryVacOkPortValue),
                        (cryVacOkLatch, cryVacOkLatchValue),
                        (cryVacLatchStatus, cryVacLatchStatusValue),
                        (cryVacLatchNeedsReset, cryVacLatchNeedsResetValue),


                        (coldRefPermit, refPermitValue),
                        (coldRefPermitPort, refPermitPortValue),
                        (coldRefPermitLockLight, refPermitLockLightValue),

                        (cryRefPermit, refPermitValue),
                        (cryRefPermitPort, refPermitPortValue),
                        (cryRefPermitLockLight, refPermitLockLightValue),


                    ], 1, compare)

                    resets = []

                    if not hexVacOkPortValue:
                        compare = []
                        hexVacOkPort.write(1)

                        self.checkChange([(hexVacOkPort, 1),
                                          (hexVacOk, 1),

                                          (hexVacOkLatch, 0),
                                          (hexVacLatchStatus, 2),
                                          (hexVacLatchNeedsReset, 1),


                                          ], 1, compare)
                        resets.append(hexVacReset_w)

                    if not cryVacOkPortValue:
                        compare=[]
                        cryVacOkPort.write(1)

                        self.checkChange([(cryVacOkPort, 1),
                                          (cryVacOk, 1),

                                          (cryVacOkLatch, 0),
                                          (cryVacLatchStatus, 2),
                                          (cryVacLatchNeedsReset, 1),


                                          ], 1, compare)
                        resets.append(cryVacReset_w)

                    #TODO test hard reset mode resetMode = not resetMode

                    if len(resets) > 0:
                        if resetMode:
                            masterResetPort.write(1)
                            self.sleep(1)
                            masterResetPort.write(0)

                        else:
                            self.pressChannels(resets)

                    self.checkDefault()

            self.step("Vacuum to refrigeration permits logic correct.")

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
                   self.tester.plutoGateway.P1_UtPowerLight,
                   self.tester.testBox.plc.P1_Q0,
                   self.tester.testBox.plc.P1_Q0],

                  [self.tester.plutoGateway.P1_RebPowerPermBlockSet,
                   self.tester.plutoGateway.P1_RebPowerPermBlockSet_w,
                   self.tester.plutoGateway.P1_RebPowerPermBlockReset,
                   self.tester.plutoGateway.P1_RebPowerPermBlockReset_w,
                   self.tester.plutoGateway.P1_RebPowerPermBlock,
                   self.tester.plutoGateway.P1_RebPowerPerm,
                   self.tester.plutoGateway.P1_RebPowerLight,
                   self.tester.testBox.plc.P1_Q1,
                   self.tester.testBox.plc.P1_Q1],

                  [self.tester.plutoGateway.P1_CoolantValveBlockSet,
                   self.tester.plutoGateway.P1_CoolantValveBlockSet_w,
                   self.tester.plutoGateway.P1_CoolantValveBlockReset,
                   self.tester.plutoGateway.P1_CoolantValveBlockReset_w,
                   self.tester.plutoGateway.P1_CoolantValveBlock,
                   self.tester.plutoGateway.P1_CoolantValve,
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
                permLightGateway = block[6]
                permLight = block[7]
                permPort = block[8]

                compare = []
                 

                set_w.press()

                self.checkChange([(blockStatus, 1), (perm, 0), (permLight, 0), (permPort, 0),(permLightGateway,0)], 3, compare)


                reset_w.press()

                self.checkDefault()



        except Exception as e:
            self.step("Permits Block logic failed! Failed at %s. Error: %s " % (self.step_m, str(e)))
            return False

        blocks = [
                  [self.tester.plutoGateway.P3_ClpRefPermBlockSet,
                   self.tester.plutoGateway.P3_ClpRefPermBlockSet_w,
                   self.tester.plutoGateway.P3_ClpRefPermBlockReset,
                   self.tester.plutoGateway.P3_ClpRefPermBlockReset_w,
                   self.tester.plutoGateway.P3_ClpRefPermBlock,
                   None,
                   self.tester.plutoGateway.P3_ClpRefPerm,
                   None,
                   self.tester.testBox.plc.P3_Q0],

                  [self.tester.plutoGateway.P3_CryRefPermBlockSet,
                   self.tester.plutoGateway.P3_CryRefPermBlockSet_w,
                   self.tester.plutoGateway.P3_CryRefPermBlockReset,
                   self.tester.plutoGateway.P3_CryRefPermBlockReset_w,
                   self.tester.plutoGateway.P3_CryRefPermBlock,
                   None,
                   self.tester.plutoGateway.P3_CryRefPerm,
                   None,
                   self.tester.testBox.plc.P3_Q1]
                  ]

        try:

            self.setDefault()

            for block in blocks:
                set_w = block[1]
                reset_w = block[3]
                blockStatus = block[4]
                perm = block[6]
                permPort = block[8]

                compare = []

                set_w.press()
                self.checkChange([(blockStatus, 1), (perm, 0), (permPort, 0)], 3,
                                 compare)

                reset_w.press()

                self.checkDefault()

            self.step("Permits Block logic correct.")
            return True

        except Exception as e:
            self.step("Permits Block logic failed! Failed at %s. Error: %s " % (self.step_m, str(e)))
            return False
