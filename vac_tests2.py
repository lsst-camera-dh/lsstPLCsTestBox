from tester import Test
import random
import time


class TestTemplate(Test):
    def __init__(self,tester,id):
        Test.__init__(self,tester,id)
        self.name = "Template"
        self.desc = "Template"

    def test(self):
        self.step("Initial message.")
        if False:
            self.step("Failure message.")
            return False
        self.step("Success message")
        return True


class TestPlutoGatewayConfig(Test):
    def __init__(self,tester,id):
        Test.__init__(self,tester,id)
        self.name = "TestPlutoGatewayConfig"
        self.expected_config = [0, 3, 0, 0, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.desc = "Check Pluto Gateway configuration registers. Expected:" + str(self.expected_config)

    def test(self):
        config = self.tester.plutoGateway.read_holding_registers(4, 0, 42)
        for i in range(len(self.expected_config)):
            if config[i] != self.expected_config[i]:
                self.step(("Pluto Gateway Config doesn't match expected values.\nConfig:\t\t%s\nExpected config:%s" % (
                str(config), str(self.expected_config))))
                return False
        self.step(("Pluto Gateway Config match expected values.\nConfig:\t\t%s \nExpected config:%s"%(str(config),str(self.expected_config))))
        return True


class TestPlutoPLCsPresent(Test):
    def __init__(self,tester,id):
        Test.__init__(self,tester,id)
        self.name = "TestPlutoPLCsPresent"
        self.desc = "Check Pluto Gateway sees Pluto D45 as node 0."

    def test(self):
        mask = self.tester.plutoGateway.read_holding_registers(36, 1, 1)[0]

        if mask == 0:
            self.step("Pluto Gateway doens't see any PLC")
            return False
        elif mask != 1:
            self.step(
                "Pluto Gateway see a PLC(s) in  unexpected nodes adds. Binary mask for detected PLCs:{0:b}".format(
                    mask))
            return False

        self.step(("Pluto Gateway sees D45 PLC as node 0"))
        return True


class TestChannelsBootDefault(Test):
    def __init__(self,tester,id):
        Test.__init__(self,tester,id)
        self.name = "TestChannelsBootDefault"
        self.desc = "Check if all channels are as expected when the PLC is powered"

    def test(self):
        self.step(self.desc)

        self.setDefault(gateway=False,check=False)

        self.step("Checking boot default values.")
        chs = []
        for ch in self.tester.testBox.plc.channels:
            if ch.boot_value != "":
                chs.append((ch, ch.boot_value))


        if self.checkChannels(chs):
            self.step("Boot default values Ok.")
            return True

        self.step("Boot values do not match defaults.")
        return False


class TestPlutoWriteReadback(Test):
    def __init__(self,tester,id):
        Test.__init__(self,tester,id)
        self.name = "TestePlutoWriteReadback"
        self.desc = "Test write and rbv Pluto adds"

    def test(self):
        self.step(self.desc)

        plutoGateway = self.tester.plutoGateway.dict

        for ch in plutoGateway.keys():

            if plutoGateway[ch]["permissions"] == "RW":

                ch_rbv = ch.replace("_w","")
                sleep=0.1

                self.step("Testing %s (%s) and %s (%s)."%(ch,"%d:%d.%d"%(plutoGateway[ch]["unit_id"],plutoGateway[ch]["addr"],plutoGateway[ch]["bit"]),ch_rbv,"%d:%d.%d"%(plutoGateway[ch_rbv]["unit_id"],plutoGateway[ch_rbv]["addr"],plutoGateway[ch_rbv]["bit"])))


                original_write = self.tester.plutoGateway.read_ch(ch)
                read = self.tester.plutoGateway.read_ch( ch_rbv)
                if original_write != read:
                    self.step("Failed on %s (%s) and %s (%s)." % (
                    ch, "%d:%d.%d" % (plutoGateway[ch]["unit_id"], plutoGateway[ch]["addr"], plutoGateway[ch]["bit"]),
                    ch_rbv, "%d:%d.%d" % (
                    plutoGateway[ch_rbv]["unit_id"], plutoGateway[ch_rbv]["addr"], plutoGateway[ch_rbv]["bit"])))
                    return False

                write = 1
                self.tester.plutoGateway.write_ch( ch,write)
                self.sleep(sleep)
                read = self.tester.plutoGateway.read_ch( ch_rbv)
                if write != read:
                    self.step("Failed on %s (%s) and %s (%s)." % (
                    ch, "%d:%d.%d" % (plutoGateway[ch]["unit_id"], plutoGateway[ch]["addr"], plutoGateway[ch]["bit"]),
                    ch_rbv, "%d:%d.%d" % (
                    plutoGateway[ch_rbv]["unit_id"], plutoGateway[ch_rbv]["addr"], plutoGateway[ch_rbv]["bit"])))
                    return False

                write = 0
                self.tester.plutoGateway.write_ch( ch,write)
                self.sleep(sleep)
                read = self.tester.plutoGateway.read_ch( ch_rbv)
                if write != read:
                    self.step("Failed on %s (%s) and %s (%s)." % (
                    ch, "%d:%d.%d" % (plutoGateway[ch]["unit_id"], plutoGateway[ch]["addr"], plutoGateway[ch]["bit"]),
                    ch_rbv, "%d:%d.%d" % (
                    plutoGateway[ch_rbv]["unit_id"], plutoGateway[ch_rbv]["addr"], plutoGateway[ch_rbv]["bit"])))
                    return False

                write = 1
                self.tester.plutoGateway.write_ch( ch,write)
                self.sleep(sleep)
                read = self.tester.plutoGateway.read_ch( ch_rbv)
                if write != read:
                    self.step("Failed on %s (%s) and %s (%s)." % (
                    ch, "%d:%d.%d" % (plutoGateway[ch]["unit_id"], plutoGateway[ch]["addr"], plutoGateway[ch]["bit"]),
                    ch_rbv, "%d:%d.%d" % (
                    plutoGateway[ch_rbv]["unit_id"], plutoGateway[ch_rbv]["addr"], plutoGateway[ch_rbv]["bit"])))
                    return False

                write = original_write
                self.tester.plutoGateway.write_ch( ch,write)
                self.sleep(sleep)
                read = self.tester.plutoGateway.read_ch( ch_rbv)
                if write != read:
                    self.step("Failed on %s (%s) and %s (%s)." % (
                    ch, "%d:%d.%d" % (plutoGateway[ch]["unit_id"], plutoGateway[ch]["addr"], plutoGateway[ch]["bit"]),
                    ch_rbv, "%d:%d.%d" % (
                    plutoGateway[ch_rbv]["unit_id"], plutoGateway[ch_rbv]["addr"], plutoGateway[ch_rbv]["bit"])))
                    return False



        self.step("All write adds are connected with the respective readback values addrs")
        return True


class TestValveMonitors(Test):
    def __init__(self,tester,id):
        Test.__init__(self,tester,id)
        self.name = "TestValveMonitors"
        self.desc = "Test TestValveMonitors"

    def test(self):
            self.step(self.desc)

            try:

                self.setDefault()
                self.checkDefault()

                valves=[[self.tester.testBox.plc.I32,self.tester.plutoGateway.MainVhxVgcOpen],
                        [self.tester.testBox.plc.I33, self.tester.plutoGateway.MainVhxVgcClose],
                        [self.tester.testBox.plc.I30, self.tester.plutoGateway.MainVcrVgcOpen],
                        [self.tester.testBox.plc.I31, self.tester.plutoGateway.MainVcrVgcClose]
                        ]

                for valve in valves:
                    monitorPort = valve[0]
                    monitor = valve[1]

                    compare = self.readAllChannels()
                    val = 1
                    monitorPort.write(val)
                    self.checkChange([(monitorPort, val),
                                      (monitor, val)
                                      ],
                                     1, compare)

                    compare = self.readAllChannels()
                    val = 0
                    monitorPort.write(val)
                    self.checkChange([(monitorPort, val),
                                      (monitor, val)
                                      ],
                                     1, compare)

                    compare = self.readAllChannels()
                    val = 1
                    monitorPort.write(val)
                    self.checkChange([(monitorPort, val),
                                      (monitor, val)
                                      ],
                                     1, compare)

                    compare = self.readAllChannels()
                    val = 0
                    monitorPort.write(val)
                    self.checkChange([(monitorPort, val),
                                      (monitor, val)
                                      ],
                                     1, compare)

                self.step("Success message")
                return True





            except Exception as e:
                self.step("CvForceClose permit logic failed!"+str(e))
                return False


class TestCvValves(Test):
        def __init__(self, tester, id):
            Test.__init__(self, tester, id)
            self.name = "TestCvValves"
            self.desc = "Test CvValves"

        def test(self):
            self.step(self.desc)

            try:

                self.setDefault()
                self.checkDefault()

                valves = [[self.tester.testBox.plc.IQ20, self.tester.plutoGateway.VcrVcc01,
                           self.tester.plutoGateway.VcrVcc01Open_w, self.tester.plutoGateway.VcrVcc01Open,
                           self.tester.plutoGateway.VcrVcc01Close_w, self.tester.plutoGateway.VcrVcc01Close],
                          [self.tester.testBox.plc.IQ21, self.tester.plutoGateway.VcrVcc02,
                           self.tester.plutoGateway.VcrVcc02Open_w, self.tester.plutoGateway.VcrVcc02Open,
                           self.tester.plutoGateway.VcrVcc02Close_w, self.tester.plutoGateway.VcrVcc02Close],
                          [self.tester.testBox.plc.IQ22, self.tester.plutoGateway.VcrVcc03,
                           self.tester.plutoGateway.VcrVcc03Open_w, self.tester.plutoGateway.VcrVcc03Open,
                           self.tester.plutoGateway.VcrVcc03Close_w, self.tester.plutoGateway.VcrVcc03Close],
                          [self.tester.testBox.plc.IQ23, self.tester.plutoGateway.VcrVcc04,
                           self.tester.plutoGateway.VcrVcc04Open_w, self.tester.plutoGateway.VcrVcc04Open,
                           self.tester.plutoGateway.VcrVcc04Close_w, self.tester.plutoGateway.VcrVcc04Close]
                          ]

                for valve in valves:
                    vccPort = valve[0]
                    vcc = valve[1]
                    open_w = valve[2]
                    open = valve[3]
                    close_w = valve[4]
                    close = valve[5]

                    compare = self.readAllChannels()
                    open_w.press()
                    self.checkChange([(vcc, 1),
                                      (vccPort, 1)
                                      ],
                                     1, compare)

                    compare = self.readAllChannels()
                    close_w.press()
                    self.checkChange([(vcc, 0),
                                      (vccPort, 0)
                                      ],
                                     1, compare)

                    compare = self.readAllChannels()
                    close_w.write(1)
                    self.checkChange([(vcc, 0),
                                      (vccPort, 0),
                                      (close, 1),
                                      (close_w, 1),
                                      ],
                                     1, compare)

                    compare = self.readAllChannels()
                    open_w.press()
                    self.checkChange([(vcc, 0),
                                      (vccPort, 0)
                                      ],
                                     1, compare)

                    compare = self.readAllChannels()
                    close_w.write(0)
                    self.checkChange([(vcc, 0),
                                      (vccPort, 0),
                                      (close, 0),
                                      (close_w, 0),
                                      ],
                                     1, compare)

                self.step("Success message")
                return True


            except Exception as e:
                self.step("CvForceClose permit logic failed!" + str(e))
                return False


class TestHvStat(Test):
    def __init__(self,tester,id):
        Test.__init__(self,tester,id)
        self.name = "TestHvStat"
        self.desc = "Test HvStat permit logic"

    def test(self):
            self.step(self.desc)

            try:
                self.setDefault()
                self.checkDefault()

                self.step("Simulate pressure over 0.001 Torr for less than 10 s. Nothing should happen.")
                compare  =self.readAllChannels()
                self.tester.testBox.write_port("plc","I40",0)
                self.checkChange([(self.tester.plutoGateway.HV001,0), (self.tester.plutoGateway.HVInterlockHigh,1),(self.tester.testBox.plc.I40,0)], 1,compare)
                self.checkDuring([(self.tester.testBox.plc.Q1,1), (self.tester.plutoGateway.HVStat,1), (self.tester.plutoGateway.HVInterlockHighLatchStatus,0)], 3)

                compare = self.readAllChannels()
                self.tester.testBox.write_port("plc", "I40", 1)
                self.checkChange([(self.tester.plutoGateway.HV001,1),(self.tester.plutoGateway.HVInterlockHigh,0),(self.tester.testBox.plc.I40,1)], 1,compare)
                self.checkDuring([(self.tester.testBox.plc.Q1, 1), (self.tester.plutoGateway.HVStat, 1),(self.tester.plutoGateway.HVInterlockHighLatchStatus, 0)], 1)

                self.step("Simulate pressure over 0.001 Torr for more than 10 s. Permit should disable after 10s.")
                compare = self.readAllChannels()
                start = time.time()
                self.tester.testBox.write_port("plc", "I40", 0)
                self.checkChange([(self.tester.plutoGateway.HV001,0), (self.tester.plutoGateway.HVInterlockHigh,1),(self.tester.testBox.plc.I40,0)], 1,compare)
                toTen = 10 - (time.time() - start)
                self.checkDuring([(self.tester.testBox.plc.Q1,1),( self.tester.plutoGateway.HVStat,1),(self.tester.plutoGateway.HVInterlockHighLatchStatus,0)], toTen-1)
                self.step("Nothing happened during 9 seconds, as expected.")
                compare = self.readAllChannels()
                toTen = 10 - (time.time() - start)
                self.checkChange([(self.tester.testBox.plc.Q1,0),(self.tester.plutoGateway.HVStat,0),(self.tester.plutoGateway.HVInterlockHighLatchStatus,1)], toTen+1,compare)
                self.step("Permit was removed.")

                self.step("Try to reset while the pressure is above the limit. This must have no result.")
                compare = self.readAllChannels()
                self.tester.plutoGateway.press_ch("HVStatLatchReset_w")
                self.checkChange([], 1, compare)
                self.step("Nothing changed as expected.")

                self.step("Simulate a pressure under the 0.001 Torr limit.")
                compare = self.readAllChannels()
                self.tester.testBox.write_port("plc", "I40", 1)
                self.checkChange([(self.tester.plutoGateway.HV001,1),(self.tester.plutoGateway.HVInterlockHigh,0),(self.tester.testBox.plc.I40,1),(self.tester.plutoGateway.HVInterlockHighLatchStatus, 2),(self.tester.plutoGateway.HVInterlockHighLatchNeedsReset, 1)], 1,compare)

                self.sleep(1)

                self.step("Try to reset the permit latch.")
                compare = self.readAllChannels()
                self.tester.plutoGateway.press_ch("HVStatLatchReset_w")
                self.checkChange([(self.tester.testBox.plc.Q1,1),(self.tester.plutoGateway.HVStat,1),(self.tester.plutoGateway.HVInterlockHighLatchStatus,0),(self.tester.plutoGateway.HVInterlockHighLatchNeedsReset, 0)], 2,compare)
                self.step("Permit reset ans lacth indicator off as expected.")

                self.checkDefault()

                self.step("Test the permit block signal.")
                compare = self.readAllChannels()
                self.tester.plutoGateway.HVStatBlock_w.write(1)
                self.checkChange([ (self.tester.plutoGateway.HVStatBlock,1),(self.tester.testBox.plc.Q1,0),(self.tester.plutoGateway.HVStat,0),(self.tester.plutoGateway.HVInterlockHighLatchStatus,1),(self.tester.plutoGateway.HVStatBlock_w,1)], 1,compare)

                self.step("Try to reset while the permit block is on. This must have no result.")
                compare = self.readAllChannels()
                self.tester.plutoGateway.press_ch("HVStatLatchReset_w")
                self.checkChange([(self.tester.testBox.plc.Q1,0),(self.tester.plutoGateway.HVStat,0),(self.tester.plutoGateway.HVInterlockHighLatchStatus,1)], 2,compare)

                self.step("Disable the permit block signal.")
                compare = self.readAllChannels()
                self.tester.plutoGateway.HVStatBlock_w.write(0)
                self.checkChange([ (self.tester.plutoGateway.HVStatBlock,0),(self.tester.testBox.plc.Q1,0),(self.tester.plutoGateway.HVStat,0),(self.tester.plutoGateway.HVStatBlock_w,0),(self.tester.plutoGateway.HVInterlockHighLatchStatus, 2),(self.tester.plutoGateway.HVInterlockHighLatchNeedsReset, 1)], 1,compare)

                self.sleep(1)

                self.step("Reset the permit latch.")
                compare = self.readAllChannels()
                self.tester.plutoGateway.press_ch("HVStatLatchReset_w")
                self.checkChange([(self.tester.testBox.plc.Q1,1),(self.tester.plutoGateway.HVStat,1),(self.tester.plutoGateway.HVInterlockHighLatchStatus,0),(self.tester.plutoGateway.HVInterlockHighLatchNeedsReset,0)], 2,compare)

                self.checkDefault()

                self.step("HvStat permit logic correct.")
                return True

            except Exception as e:
                self.step("HvStat permit logic failed!"+str(e))
                return False


class TestCvStat(Test):
    def __init__(self,tester,id):
        Test.__init__(self,tester,id)
        self.name = "TestCvStat"
        self.desc = "Test CvStat permit logic"

    def test(self):
            self.step(self.desc)

            try:

                self.setDefault()
                self.checkDefault()

                self.step("Simulate pressure over 0.001 Torr for less than 10 s. Nothing should happen.")
                compare  =self.readAllChannels()
                self.tester.testBox.write_port("plc","I36",0)
                self.checkChange([(self.tester.plutoGateway.CV001,0), (self.tester.plutoGateway.CVInterlockHigh,1),(self.tester.testBox.plc.I36,0)], 1,compare)
                self.checkDuring([(self.tester.testBox.plc.Q0,1), (self.tester.plutoGateway.CVStat,1), (self.tester.plutoGateway.CVInterlockHighLatchStatus,0)], 3)

                compare = self.readAllChannels()
                self.tester.testBox.write_port("plc", "I36", 1)
                self.checkChange([(self.tester.plutoGateway.CV001,1),(self.tester.plutoGateway.CVInterlockHigh,0),(self.tester.testBox.plc.I36,1)], 1,compare)
                self.checkDuring([(self.tester.testBox.plc.Q0,1),( self.tester.plutoGateway.CVStat,1),(self.tester.plutoGateway.CVInterlockHighLatchStatus,0)],2)

                self.step("Simulate pressure over 0.001 Torr for more than 10 s. Permit should disable after 10s.")
                compare = self.readAllChannels()
                self.tester.testBox.write_port("plc", "I36", 0)
                start = time.time()
                self.checkChange([(self.tester.plutoGateway.CV001,0), (self.tester.plutoGateway.CVInterlockHigh,1),(self.tester.testBox.plc.I36,0)], 1,compare)
                toTen = 10 - (time.time() - start)
                self.checkDuring([(self.tester.testBox.plc.Q0,1),( self.tester.plutoGateway.CVStat,1),(self.tester.plutoGateway.CVInterlockHighLatchStatus,0)], toTen-1)
                self.step("Nothing happened during 9 seconds, as expected.")
                compare = self.readAllChannels()
                toTen = 10 - (time.time() - start)
                self.checkChange([(self.tester.testBox.plc.Q0,0),(self.tester.plutoGateway.CVStat,0),(self.tester.plutoGateway.CVInterlockHighLatchStatus,1)], toTen+1,compare)
                self.step("Permit turned was removed.")

                self.step("Try to reset while the pressure is above the limit. This must have no result.")
                compare = self.readAllChannels()
                self.tester.plutoGateway.press_ch("CVStatLatchReset_w")
                self.checkChange([], 1, compare)
                self.step("Nothing changed as expected.")

                self.step("Simulate a pressure under the 0.001 Torr limit.")
                compare = self.readAllChannels()
                self.tester.testBox.write_port("plc", "I36", 1)
                self.checkChange([(self.tester.plutoGateway.CV001,1),(self.tester.plutoGateway.CVInterlockHigh,0),(self.tester.testBox.plc.I36,1),(self.tester.plutoGateway.CVInterlockHighLatchStatus, 2),(self.tester.plutoGateway.CVInterlockHighLatchNeedsReset, 1)], 1,compare)

                self.sleep(1)

                self.step("Try to reset the permit latch.")
                compare = self.readAllChannels()
                self.tester.plutoGateway.press_ch("CVStatLatchReset_w")
                self.checkChange([(self.tester.testBox.plc.Q0,1),(self.tester.plutoGateway.CVStat,1),(self.tester.plutoGateway.CVInterlockHighLatchStatus,0),(self.tester.plutoGateway.CVInterlockHighLatchNeedsReset,0)], 2,compare)
                self.step("Permit reset ans lacth indicator off as expected.")

                self.checkDefault()

                self.step("Test the permit block signal.")
                compare = self.readAllChannels()
                self.tester.plutoGateway.CVStatBlock_w.write(1)
                self.checkChange([ (self.tester.plutoGateway.CVStatBlock,1),(self.tester.testBox.plc.Q0,0),(self.tester.plutoGateway.CVStat,0),(self.tester.plutoGateway.CVInterlockHighLatchStatus,1),(self.tester.plutoGateway.CVStatBlock_w,1)], 1,compare)

                self.step("Try to reset while the permit block is on. This must have no result.")
                compare = self.readAllChannels()
                self.tester.plutoGateway.press_ch("CVStatLatchReset_w")
                self.checkChange([(self.tester.testBox.plc.Q0,0),(self.tester.plutoGateway.CVStat,0),(self.tester.plutoGateway.CVInterlockHighLatchStatus,1)], 2,compare)

                self.step("Disable the permit block signal.")
                compare = self.readAllChannels()
                self.tester.plutoGateway.CVStatBlock_w.write(0)
                self.checkChange([ (self.tester.plutoGateway.CVStatBlock,0),(self.tester.testBox.plc.Q0,0),(self.tester.plutoGateway.CVStat,0),(self.tester.plutoGateway.CVStatBlock_w,0),(self.tester.plutoGateway.CVInterlockHighLatchStatus, 2),(self.tester.plutoGateway.CVInterlockHighLatchNeedsReset,1)], 1,compare)

                self.sleep(1)

                self.step("Reset the permit latch.")
                compare = self.readAllChannels()
                self.tester.plutoGateway.press_ch("CVStatLatchReset_w")
                self.checkChange([(self.tester.testBox.plc.Q0,1),(self.tester.plutoGateway.CVStat,1),(self.tester.plutoGateway.CVInterlockHighLatchStatus,0),(self.tester.plutoGateway.CVInterlockHighLatchNeedsReset,0)], 2,compare)

                self.checkDefault()

                self.step("CvStat permit logic correct.")
                return True

            except Exception as e:
                self.step("CvStat permit logic failed!"+str(e))
                return False


class TestCvTurboPermitBlock(Test):
    def __init__(self,tester,id):
        Test.__init__(self,tester,id)
        self.name = "TestCvTurboPermitBlock"
        self.desc = "Test TestCvTurboPermitBlock permit logic"

    def test(self):
            self.step(self.desc)


            turboPumpPermitPort = self.tester.testBox.plc.Q4
            turboPumpPermit = self.tester.plutoGateway.VcrPumpPerm
            turboPumpPermitLatchStatus = self.tester.plutoGateway.VcrPumpPermLatchStatus
            turboPumpPermitLatchNeedsReset = self.tester.plutoGateway.VcrPumpPermLatchNeedsReset
            turboPumpPermitReset = self.tester.plutoGateway.VcrPumpPermReset_w

            permitBlock_w = self.tester.plutoGateway.VcrPumpPermBlock_w
            permitBlock = self.tester.plutoGateway.VcrPumpPermBlock


            try:

                self.setDefault()
                self.checkDefault()

                self.step("Test Turbo Pump Permit Block")
                compare = self.readAllChannels()
                permitBlock_w.write(1)
                self.checkChange([(turboPumpPermitPort, 0),(turboPumpPermit, 0),(turboPumpPermitLatchStatus, 1),(permitBlock,1),(permitBlock_w,1)], 1, compare)

                compare = self.readAllChannels()
                turboPumpPermitReset.press()
                self.checkChange([(turboPumpPermitPort, 0), (turboPumpPermit, 0), (turboPumpPermitLatchStatus, 1)], 1,compare)

                compare = self.readAllChannels()
                permitBlock_w.write(0)
                self.checkChange([(turboPumpPermitPort, 0),(turboPumpPermit, 0),(turboPumpPermitLatchStatus, 2),(turboPumpPermitLatchNeedsReset, 1),(permitBlock,0),(permitBlock_w,0)], 1, compare)

                compare = self.readAllChannels()
                turboPumpPermitReset.press()
                self.checkChange([(turboPumpPermitPort, 1), (turboPumpPermit, 1), (turboPumpPermitLatchStatus, 0),(turboPumpPermitLatchNeedsReset, 0)], 1,compare)



                self.step("TestCvTurboPermitBlock permit logic correct.")
                return True

            except Exception as e:
                self.step("TestCvTurboPermitBlock permit logic failed! Failed at %s. Error: %s "%(self.step_m,str(e)))
                return False


class TestHvTurboPermitBlock(Test):
    def __init__(self,tester,id):
        Test.__init__(self,tester,id)
        self.name = "TestHvTurboPermitBlock"
        self.desc = "Test TestHvTurboPermitBlock permit logic"

    def test(self):
            self.step(self.desc)


            turboPumpPermitPort = self.tester.testBox.plc.Q5
            turboPumpPermit = self.tester.plutoGateway.VhxPumpPerm
            turboPumpPermitLatchStatus = self.tester.plutoGateway.VhxPumpPermLatchStatus
            turboPumpPermitLatchNeedsReset = self.tester.plutoGateway.VhxPumpPermLatchNeedsReset
            turboPumpPermitReset = self.tester.plutoGateway.VhxPumpPermReset_w

            permitBlock_w = self.tester.plutoGateway.VhxPumpPermBlock_w
            permitBlock = self.tester.plutoGateway.VhxPumpPermBlock


            try:

                self.setDefault()
                self.checkDefault()

                self.step("Test Turbo Pump Permit Block")
                compare = self.readAllChannels()
                permitBlock_w.write(1)
                self.checkChange([(turboPumpPermitPort, 0),(turboPumpPermit, 0),(turboPumpPermitLatchStatus, 1),(permitBlock,1),(permitBlock_w,1)], 1, compare)

                compare = self.readAllChannels()
                turboPumpPermitReset.press()
                self.checkChange([(turboPumpPermitPort, 0), (turboPumpPermit, 0), (turboPumpPermitLatchStatus, 1)], 1,compare)

                compare = self.readAllChannels()
                permitBlock_w.write(0)
                self.checkChange([(turboPumpPermitPort, 0),(turboPumpPermit, 0),(turboPumpPermitLatchStatus, 2),(turboPumpPermitLatchNeedsReset, 1),(permitBlock,0),(permitBlock_w,0)], 1, compare)

                compare = self.readAllChannels()
                turboPumpPermitReset.press()
                self.checkChange([(turboPumpPermitPort, 1), (turboPumpPermit, 1), (turboPumpPermitLatchStatus, 0),(turboPumpPermitLatchNeedsReset, 0)], 1,compare)



                self.step("TestHvTurboPermitBlock permit logic correct.")
                return True

            except Exception as e:
                self.step("TestHvTurboPermitBlock permit logic failed! Failed at %s. Error: %s "%(self.step_m,str(e)))
                return False


class TestCvTurboPermitAuto(Test):
    def __init__(self,tester,id):
        Test.__init__(self,tester,id)
        self.name = "TestCvTurboPermitAuto"
        self.desc = "Test TestCvTurboPermitAuto permit logic"

    def test(self):
            self.step(self.desc)


            turboPressureUnder10Port = self.tester.testBox.plc.IA3

            turboPressureUnder10 = self.tester.plutoGateway.CVTurboUnder10


            turboPumpOffPort = self.tester.testBox.plc.IA7
            turboPumpOff = self.tester.plutoGateway.CVTurboPumpOFF


            turboPumpPermitPort = self.tester.testBox.plc.Q4
            turboPumpPermit = self.tester.plutoGateway.VcrPumpPerm
            turboPumpPermitLatchStatus = self.tester.plutoGateway.VcrPumpPermLatchStatus
            turboPumpPermitReset_w = self.tester.plutoGateway.VcrPumpPermReset_w

            mksPort = self.tester.testBox.plc.I34
            mks = self.tester.plutoGateway.MKS925


            vccAllowedOpenLatch = self.tester.plutoGateway.MainVcrVccAllowedOpenLatch
            vccAllowedOpenLatchStatus = self.tester.plutoGateway.MainVcrVccAllowedOpenLatchStatus
            vccAllowedOpenLatchReset_w = self.tester.plutoGateway.MainVcrVccAllowedOpenLatchReset_w

            vccNotForcedCloseLatch = self.tester.plutoGateway.MainVcrVccNotForcedCloseLatch
            vccNotForcedCloseLatchStatus = self.tester.plutoGateway.MainVcrVccNotForcedCloseLatchStatus
            vccNotForcedCloseLatchReset_w = self.tester.plutoGateway.MainVcrVccNotForcedCloseReset_w

            turboPumpPermitLatchNeedsReset = self.tester.plutoGateway.VcrPumpPermLatchNeedsReset
            vccNotForcedCloseLatchNeedsReset = self.tester.plutoGateway.MainVcrVccNotForcedCloseLatchNeedsReset
            vccAllowedOpenLatchNeedsReset = self.tester.plutoGateway.MainVcrVccAllowedOpenLatchNeedsReset

            statPort = self.tester.testBox.plc.Q0
            stat = self.tester.plutoGateway.CVStat
            statInterlockHigh = self.tester.plutoGateway.CVInterlockHigh
            statInterlockHighLatchStatus = self.tester.plutoGateway.CVInterlockHighLatchStatus


            vccPort = self.tester.testBox.plc.Q2
            vcc = self.tester.plutoGateway.MainVcrVcc
            vccOpen_w = self.tester.plutoGateway.OpenMainVcrVcc_w
            vccClose_w = self.tester.plutoGateway.CloseMainVcrVcc_w

            CV01Port = self.tester.testBox.plc.I35
            CV01 = self.tester.plutoGateway.CV01

            turboPressureUnder10PortValues = [0,1]
            turboPumpOffPortValues = [0,1]

            mksPortValues = [0,1]

            CV01PortValues = [0,1]


            self.setDefault()
            vccOpen_w.press()

            self.sleep(1)

            n = 0

            try:
                for turboPressureUnder10PortValue in turboPressureUnder10PortValues:
                    for turboPumpOffPortValue in turboPumpOffPortValues:
                                        for mksPortValue in mksPortValues:
                                            for CV01PortValue in CV01PortValues:
                                                n=n+1
                                                print("--------------------------------------------------------------------------")

                                                if n<0:
                                                    continue

                                                # Pump Permit (24V) =  (VCR-UTT-GCC-01 Relay 2 Closed)  AND  ( (Cryostat TurboPumpOff OFF AND Relay Output of MKS925 is Closed) OR Cryostat TurboPumpOff ON)
                                                turboPumpPermitValue = turboPressureUnder10PortValue and ( ( turboPumpOffPortValue==0 and mksPortValue==1) or turboPumpOffPortValue==1)

                                                # Close VCR-UTT-VGC-00 (Set PLC output to 0v)  = Cryostat TurboPumpOff OFF  AND (Relay Output of MKS925 is Open)
                                                if (turboPumpOffPortValue == 0) and (mksPortValue == 0):
                                                    vccNotForcedCloseLatchValue = 0
                                                else:
                                                    vccNotForcedCloseLatchValue = 1


                                                if vccNotForcedCloseLatchValue == 0:
                                                    vccNotForcedCloseLatchStatusValue =1
                                                else:
                                                    vccNotForcedCloseLatchStatusValue = 0
                                                vccNotForcedCloseLatchNeedsResetValue = vccNotForcedCloseLatchStatusValue == 2


                                                turboPumpPermitPortValue = turboPumpPermitValue
                                                turboPumpPermitLatchStatusValue = int(not bool(turboPumpPermitPortValue))
                                                turboPumpPermitLatchNeedsResetValue= turboPumpPermitLatchStatusValue ==2

                                                #VCR-UTT-VGC-00 allowed to open  = Cryostat TurboPumpOff ON OR (Cryostat TurboPumpOff OFF AND (VCR-UTT-GCC-00 Relay 1 AND VCR-UTT-GCC-01 Relay 1))
                                                vccAllowedOpenLatchValue = (turboPumpOffPortValue==1 or (turboPumpOffPortValue==0 and CV01PortValue == 1)) and vccNotForcedCloseLatchValue

                                                if vccAllowedOpenLatchValue ==0:
                                                    vccAllowedOpenLatchStatusValue = 2
                                                    vccAllowedOpenLatchNeedsResetValue = 1
                                                else:
                                                    vccAllowedOpenLatchStatusValue = 0
                                                    vccAllowedOpenLatchNeedsResetValue = 0


                                                ##################

                                                compare = self.readAllChannels()


                                                CV01Port.write(CV01PortValue)
                                                mksPort.write(mksPortValue)

                                                turboPressureUnder10Port.write(turboPressureUnder10PortValue)
                                                turboPumpOffPort.write(turboPumpOffPortValue)

                                                #self.sleep(.6)

                                                self.pressChannels([turboPumpPermitReset_w,vccAllowedOpenLatchReset_w,vccNotForcedCloseLatchReset_w])

                                                #Try to opem
                                                vccOpen_w.press()

                                                print("AAA 1")


                                                self.checkChange([(mksPort, mksPortValue),
                                                                  (mks, mksPortValue),

                                                                  (CV01Port,CV01PortValue),
                                                                  (CV01,CV01PortValue),

                                                                  (turboPressureUnder10Port, turboPressureUnder10PortValue),
                                                                  (turboPressureUnder10,turboPressureUnder10PortValue),

                                                                  (turboPumpOffPort, turboPumpOffPortValue),
                                                                  (turboPumpOff, turboPumpOffPortValue),


                                                                  (turboPumpPermitPort, turboPumpPermitPortValue),
                                                                  (turboPumpPermit, turboPumpPermitValue),
                                                                  (turboPumpPermitLatchStatus, turboPumpPermitLatchStatusValue),
                                                                  (turboPumpPermitLatchNeedsReset,turboPumpPermitLatchNeedsResetValue),

                                                                  (vccAllowedOpenLatch,vccAllowedOpenLatchValue),
                                                                  (vccAllowedOpenLatchStatus,vccAllowedOpenLatchStatusValue),
                                                                  (vccAllowedOpenLatchNeedsReset,vccAllowedOpenLatchNeedsResetValue),

                                                                  (vccNotForcedCloseLatch,vccNotForcedCloseLatchValue),
                                                                  (vccNotForcedCloseLatchStatus,vccNotForcedCloseLatchStatusValue),
                                                                  (vccNotForcedCloseLatchNeedsReset,vccNotForcedCloseLatchNeedsResetValue),

                                                                  (vcc,vccNotForcedCloseLatchValue),
                                                                  (vccPort,vccNotForcedCloseLatchValue),

                                                                  (statPort,None),
                                                                  (stat,None),
                                                                  (statInterlockHigh,None),
                                                                  (statInterlockHighLatchStatus,None)


                                                                  ],                                                     1,compare)

                                                print("AAA 2")
                                                #can always close
                                                vccClose_w.press()

                                                print("AAA 3")

                                                self.checkChange([(vcc, 0),
                                                                  (vccPort, 0),
                                                                  ], 1,checkBlinks=False)

                                                print("AAA 4")

                                                # Check if can open
                                                if vccAllowedOpenLatchValue and vccNotForcedCloseLatchValue:

                                                    vccOpen_w.press()
                                                    self.checkChange([(vcc,1),
                                                                  (vccPort,1),
                                                                      ], 1,checkBlinks=False)

                                                else:
                                                    vccOpen_w.press()
                                                    self.checkChange([(vcc,0),
                                                                  (vccPort,0),
                                                                      ], 1,checkBlinks=False)

                                                print("AAA 5")
                                                #input()


                                                #self.writeChannels(compare)
                                                self.setDefault(gateway=False,check=False)
                                                self.sleep(.5)
                                                print("AAA 6")


                                                press = []
                                                change1 = []
                                                change2 = []


                                               # input()
                                                print("AAA 7")
                                                if not bool(vccAllowedOpenLatchValue):

                                                    change1.append((vccAllowedOpenLatchStatus, 2))
                                                    change1.append((vccAllowedOpenLatchNeedsReset, 1))

                                                    press.append(vccAllowedOpenLatchReset_w)

                                                    change2.append((vccAllowedOpenLatch, 1))
                                                    change2.append((vccAllowedOpenLatchStatus, 0))
                                                    change2.append((vccAllowedOpenLatchNeedsReset, 0))


                                                if not bool(vccNotForcedCloseLatchValue):
                                                    change1.append((vccNotForcedCloseLatchStatus, 2))
                                                    change1.append((vccNotForcedCloseLatchNeedsReset, 1))

                                                    press.append(vccNotForcedCloseLatchReset_w)

                                                    change2.append((vccNotForcedCloseLatch, 1))
                                                    change2.append((vccNotForcedCloseLatchStatus, 0))
                                                    change2.append((vccNotForcedCloseLatchNeedsReset, 0))


                                                if not bool(turboPumpPermitPortValue):

                                                    change1.append((turboPumpPermitLatchStatus, 2))
                                                    change1.append((turboPumpPermitLatchNeedsReset, 1))

                                                    press.append(turboPumpPermitReset_w)

                                                    change2.append((turboPumpPermitPort, 1))
                                                    change2.append((turboPumpPermit, 1))
                                                    change2.append((turboPumpPermitLatchStatus, 0))
                                                    change2.append((turboPumpPermitLatchNeedsReset, 0))





                                                self.checkChange(change1, 1)

                                                self.pressChannels(press)


                                                self.checkChange(change2, 1)


                                                self.sleep(0.1)

                                                #can open
                                                vccOpen_w.press()
                                                self.checkChange([(vcc, 1),
                                                                  (vccPort, 1),
                                                                  ], 1,checkBlinks=False)
                                                self.sleep(0.5)





                self.step("TestCVTurboPermitAuto permit logic correct.")
                return True

            except ValueError as e:
                self.step("CvTurboPump permit logic failed! Failed at %s. Error: %s "%(self.step_m,str(e)))
                return False


class TestHvTurboPermitAuto(Test):
    def __init__(self,tester,id):
        Test.__init__(self,tester,id)
        self.name = "TestHvTurboPermitAuto"
        self.desc = "Test TestHvTurboPermitAuto permit logic"

    def test(self):
            self.step(self.desc)

            turboPressureUnder10Port = self.tester.testBox.plc.IA0
            turboPressureUnder10 = self.tester.plutoGateway.HVTurboUnder10
            turboPumpOffPort = self.tester.testBox.plc.IA6

            turboPumpOff = self.tester.plutoGateway.HVTurboPumpOFF

            turboPumpPermitPort = self.tester.testBox.plc.Q5
            turboPumpPermit = self.tester.plutoGateway.VhxPumpPerm
            turboPumpPermitLatchStatus = self.tester.plutoGateway.VhxPumpPermLatchStatus
            turboPumpPermitLatchNeedsReset = self.tester.plutoGateway.VhxPumpPermLatchNeedsReset
            turboPumpPermitReset_w = self.tester.plutoGateway.VhxPumpPermReset_w

            mksPort = self.tester.testBox.plc.I34
            mks = self.tester.plutoGateway.MKS925


            vccAllowedOpenLatch = self.tester.plutoGateway.MainVhxVccAllowedOpenLatch
            vccAllowedOpenLatchStatus = self.tester.plutoGateway.MainVhxVccAllowedOpenLatchStatus
            vccAllowedOpenLatchNeedsReset = self.tester.plutoGateway.MainVhxVccAllowedOpenLatchNeedsReset
            vccAllowedOpenLatchReset_w = self.tester.plutoGateway.MainVhxVccAllowedOpenLatchReset_w

            vccNotForcedCloseLatch = self.tester.plutoGateway.MainVhxVccNotForcedCloseLatch
            vccNotForcedCloseLatchStatus = self.tester.plutoGateway.MainVhxVccNotForcedCloseLatchStatus
            vccNotForcedCloseLatchNeedsReset = self.tester.plutoGateway.MainVhxVccNotForcedCloseLatchNeedsReset
            vccNotForcedCloseLatchReset_w = self.tester.plutoGateway.MainVhxVccNotForcedCloseReset_w

            statPort = self.tester.testBox.plc.Q1
            stat = self.tester.plutoGateway.HVStat
            statInterlockHigh = self.tester.plutoGateway.HVInterlockHigh
            statInterlockHighLatchStatus = self.tester.plutoGateway.HVInterlockHighLatchStatus

            vccPort = self.tester.testBox.plc.Q3
            vcc = self.tester.plutoGateway.MainVhxVcc
            vccOpen_w = self.tester.plutoGateway.OpenMainVhxVcc_w
            vccClose_w = self.tester.plutoGateway.CloseMainVhxVcc_w

            CV01Port = self.tester.testBox.plc.I37
            CV01 = self.tester.plutoGateway.HV01



            turboPressureUnder10PortValues = [0,1]
            turboPumpOffPortValues = [0,1]
            mksPortValues = [0,1]

            CV01PortValues = [0,1]


            self.setDefault()
            vccOpen_w.press()


            self.sleep(1)

            n = 0

            try:
                for turboPressureUnder10PortValue in turboPressureUnder10PortValues:
                    for turboPumpOffPortValue in turboPumpOffPortValues:
                                        for mksPortValue in mksPortValues:
                                            for CV01PortValue in CV01PortValues:
                                                n=n+1
                                                print("--------------------------------------------------------------------------")

                                                if n<0:
                                                    continue

                                                # Pump Permit (24V) =  (VCR-UTT-GCC-01 Relay 2 Closed)  AND  ( (Cryostat TurboPumpOff OFF AND Relay Output of MKS925 is Closed) OR Cryostat TurboPumpOff ON)
                                                turboPumpPermitValue = turboPressureUnder10PortValue and ( ( turboPumpOffPortValue==0 and mksPortValue==1) or turboPumpOffPortValue==1)

                                                # Close VCR-UTT-VGC-00 (Set PLC output to 0v)  = Cryostat TurboPumpOff OFF  AND (Relay Output of MKS925 is Open)
                                                if (turboPumpOffPortValue == 0) and (mksPortValue == 0):
                                                    vccNotForcedCloseLatchValue = 0
                                                else:
                                                    vccNotForcedCloseLatchValue = 1


                                                if vccNotForcedCloseLatchValue == 0:
                                                    vccNotForcedCloseLatchStatusValue =1
                                                else:
                                                    vccNotForcedCloseLatchStatusValue = 0
                                                vccNotForcedCloseLatchNeedsResetValue = vccNotForcedCloseLatchStatusValue == 2


                                                turboPumpPermitPortValue = turboPumpPermitValue
                                                turboPumpPermitLatchStatusValue = int(not bool(turboPumpPermitPortValue))
                                                turboPumpPermitLatchNeedsResetValue= turboPumpPermitLatchStatusValue ==2

                                                #VCR-UTT-VGC-00 allowed to open  = Cryostat TurboPumpOff ON OR (Cryostat TurboPumpOff OFF AND (VCR-UTT-GCC-00 Relay 1 AND VCR-UTT-GCC-01 Relay 1))
                                                vccAllowedOpenLatchValue = (turboPumpOffPortValue==1 or (turboPumpOffPortValue==0 and CV01PortValue == 1)) and vccNotForcedCloseLatchValue

                                                if vccAllowedOpenLatchValue ==0:
                                                    vccAllowedOpenLatchStatusValue = 2
                                                    vccAllowedOpenLatchNeedsResetValue = 1
                                                else:
                                                    vccAllowedOpenLatchStatusValue = 0
                                                    vccAllowedOpenLatchNeedsResetValue = 0


                                                ##################

                                                compare = self.readAllChannels()


                                                CV01Port.write(CV01PortValue)
                                                mksPort.write(mksPortValue)

                                                turboPressureUnder10Port.write(turboPressureUnder10PortValue)
                                                turboPumpOffPort.write(turboPumpOffPortValue)

                                                #self.sleep(.6)

                                                self.pressChannels([turboPumpPermitReset_w,vccAllowedOpenLatchReset_w,vccNotForcedCloseLatchReset_w])

                                                #Try to opem
                                                vccOpen_w.press()

                                                print("AAA 1")


                                                self.checkChange([(mksPort, mksPortValue),
                                                                  (mks, mksPortValue),

                                                                  (CV01Port,CV01PortValue),
                                                                  (CV01,CV01PortValue),

                                                                  (turboPressureUnder10Port, turboPressureUnder10PortValue),
                                                                  (turboPressureUnder10,turboPressureUnder10PortValue),

                                                                  (turboPumpOffPort, turboPumpOffPortValue),
                                                                  (turboPumpOff, turboPumpOffPortValue),


                                                                  (turboPumpPermitPort, turboPumpPermitPortValue),
                                                                  (turboPumpPermit, turboPumpPermitValue),
                                                                  (turboPumpPermitLatchStatus, turboPumpPermitLatchStatusValue),
                                                                  (turboPumpPermitLatchNeedsReset,turboPumpPermitLatchNeedsResetValue),

                                                                  (vccAllowedOpenLatch,vccAllowedOpenLatchValue),
                                                                  (vccAllowedOpenLatchStatus,vccAllowedOpenLatchStatusValue),
                                                                  (vccAllowedOpenLatchNeedsReset,vccAllowedOpenLatchNeedsResetValue),

                                                                  (vccNotForcedCloseLatch,vccNotForcedCloseLatchValue),
                                                                  (vccNotForcedCloseLatchStatus,vccNotForcedCloseLatchStatusValue),
                                                                  (vccNotForcedCloseLatchNeedsReset,vccNotForcedCloseLatchNeedsResetValue),

                                                                  (vcc,vccNotForcedCloseLatchValue),
                                                                  (vccPort,vccNotForcedCloseLatchValue),

                                                                  (statPort,None),
                                                                  (stat,None),
                                                                  (statInterlockHigh,None),
                                                                  (statInterlockHighLatchStatus,None)


                                                                  ],                                                     1,compare)

                                                print("AAA 2")
                                                #can always close
                                                vccClose_w.press()

                                                print("AAA 3")

                                                self.checkChange([(vcc, 0),
                                                                  (vccPort, 0),
                                                                  ], 1,checkBlinks=False)

                                                print("AAA 4")

                                                # Check if can open
                                                if vccAllowedOpenLatchValue and vccNotForcedCloseLatchValue:

                                                    vccOpen_w.press()
                                                    self.checkChange([(vcc,1),
                                                                  (vccPort,1),
                                                                      ], 1,checkBlinks=False)

                                                else:
                                                    vccOpen_w.press()
                                                    self.checkChange([(vcc,0),
                                                                  (vccPort,0),
                                                                      ], 1,checkBlinks=False)

                                                print("AAA 5")
                                                #input()


                                                #self.writeChannels(compare)
                                                self.setDefault(gateway=False,check=False)
                                                self.sleep(.5)
                                                print("AAA 6")


                                                press = []
                                                change1 = []
                                                change2 = []


                                               # input()
                                                print("AAA 7")
                                                if not bool(vccAllowedOpenLatchValue):

                                                    change1.append((vccAllowedOpenLatchStatus, 2))
                                                    change1.append((vccAllowedOpenLatchNeedsReset, 1))

                                                    press.append(vccAllowedOpenLatchReset_w)

                                                    change2.append((vccAllowedOpenLatch, 1))
                                                    change2.append((vccAllowedOpenLatchStatus, 0))
                                                    change2.append((vccAllowedOpenLatchNeedsReset, 0))


                                                if not bool(vccNotForcedCloseLatchValue):
                                                    change1.append((vccNotForcedCloseLatchStatus, 2))
                                                    change1.append((vccNotForcedCloseLatchNeedsReset, 1))

                                                    press.append(vccNotForcedCloseLatchReset_w)

                                                    change2.append((vccNotForcedCloseLatch, 1))
                                                    change2.append((vccNotForcedCloseLatchStatus, 0))
                                                    change2.append((vccNotForcedCloseLatchNeedsReset, 0))


                                                if not bool(turboPumpPermitPortValue):

                                                    change1.append((turboPumpPermitLatchStatus, 2))
                                                    change1.append((turboPumpPermitLatchNeedsReset, 1))

                                                    press.append(turboPumpPermitReset_w)

                                                    change2.append((turboPumpPermitPort, 1))
                                                    change2.append((turboPumpPermit, 1))
                                                    change2.append((turboPumpPermitLatchStatus, 0))
                                                    change2.append((turboPumpPermitLatchNeedsReset, 0))





                                                self.checkChange(change1, 1)

                                                self.pressChannels(press)


                                                self.checkChange(change2, 1)


                                                self.sleep(0.1)

                                                #can open
                                                vccOpen_w.press()
                                                self.checkChange([(vcc, 1),
                                                                  (vccPort, 1),
                                                                  ], 1,checkBlinks=False)
                                                self.sleep(0.5)





                self.step("TestHvTurboPermitAuto permit logic correct.")
                return True

            except ValueError as e:
                self.step("TestHvTurboPermitAuto permit logic failed! Failed at %s. Error: %s "%(self.step_m,str(e)))
                return False




