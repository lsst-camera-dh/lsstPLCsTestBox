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
        self.expected_config = [0, 3, 1000, 0, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 0,
                                    0, 0, 0, 0,
                                    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
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

        self.step("Checking boot default values.")
        chs = []
        for ch in self.tester.testBox.plc.channels:
            if ch.boot_value != "":
                chs.append((ch, ch.boot_value))
        for ch in self.tester.plutoGateway.channels:
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


class TestAnalogScaling(Test):
    def __init__(self,tester,id):
        Test.__init__(self,tester,id)
        self.name = "TestAnalogScaling"
        self.desc = "Check the analog input wiring, linearity and scaling factors and offsets"

        #[IA0,IA1,IA2,IA3,IA4,IA6,IA7]
        self.expected_factors=[2,2,2,2,2,1000,1000]
        self.expected_offsets=[0,0,0,0,0,0,0]

        self.n_points = 10

    def test(self):
        self.step(self.desc)
        self.step("Scaning...")

        test = dict()

        for n, port in enumerate(["IA0","IA1","IA2","IA3","IA4","IA6","IA7"]):

            test[port] = dict()
            test[port]["step"] = random.uniform(0.6, 1.6)
            test[port]["value"] = 0.05
            test[port]["value_array"] = []
            test[port]["finished"] = False

            for md in self.tester.testBox.dict[port]["modbus"]:
                if md.find("Voltage")>0:
                    test[port]["channel_voltage"] = md
                    test[port]["channel_voltage_array"] = []
                elif md.find("Valid")>0:
                    test[port]["channel_valid"] = md
                    test[port]["channel_valid_array"] = []
                else:
                    test[port]["channel_scaled"] = md
                    test[port]["channel_scaled_array"] = []

        cont = True
        while cont:
            cont = False
            for port in test.keys():
                if test[port]["value"]<10:

                    voltage = test[port]["value"] + test[port]["step"]
                    if voltage>10.1:
                        voltage =10.1
                    self.tester.testBox.write_port("plc", port, voltage)
                    test[port]["value"] = voltage
                    test[port]["value_array"].append(voltage)
                else:
                    test[port]["finished"] = True


            self.sleep(.7)

            for port in test.keys():
                if test[port]["finished"] is not True:
                    test[port]["channel_voltage_array"].append(self.tester.plutoGateway.read_ch( test[port]["channel_voltage"]))
                    test[port]["channel_scaled_array"].append(self.tester.plutoGateway.read_ch(test[port]["channel_scaled"]))
                    test[port]["channel_valid_array"].append(self.tester.plutoGateway.read_ch(test[port]["channel_valid"]))




                cont = cont | (test[port]["value"]<10.0)

        from scipy import stats

        self.step("Evaluating Valid")
        for port in test.keys():
            if sum(test[port]["channel_valid_array"]) != len(test[port]["channel_valid_array"]):
                self.step("Channel %s read not valid"%port)
                return False

        self.step("Evaluating Correct wiring")
        for port in test.keys():
            y = test[port]["value_array"]
            x = range(len(test[port]["channel_voltage_array"]))
            values=stats.linregress(x,y)

            y = test[port]["channel_voltage_array"]
            x = range(len(test[port]["channel_voltage_array"]))
            voltage=stats.linregress(x,y)



            if values.rvalue < 0.99 or voltage.rvalue<0.99:
                self.step("R-square too high on %s" % port)
                return False

            if abs(values.slope*1000-voltage.slope)>(values.slope*1000+voltage.slope)/2*0.005:
                self.step("Slope (over time) discrepancy between input and read value on %s. Probably wrong wiring." % port)
                return False

            if abs(values.intercept*1000 -voltage.intercept )>10000*0.002:
                self.step("Intercept  (over time) discrepancy between input and read value on %s. Probably wrong wiring." % port)
                return False


        self.step("Evaluating voltage linearity")
        for port in test.keys():
            y = test[port]["channel_voltage_array"]
            x = test[port]["value_array"]
            values=stats.linregress(x,y)

            if values.rvalue < 0.99:
                self.step("R-square too high on %s" % port)
                return False

            if abs(values.slope-1000)>1000*0.005:
                self.step("Transfer function Slope not 10 000 +- 0.5%% on %s." % port)
                return False

            if abs(values.intercept)>10000*0.005:
                self.step("Transfer function Intercept not 0 +- 0.5%% on %s." % port)
                return False


        self.step("Evaluating scaling coeficients")
        for port in test.keys():
            y = test[port]["channel_scaled_array"]
            x = test[port]["channel_voltage_array"]
            values = stats.linregress(x, y)

            if values.rvalue < 0.99:
                self.step("R-square too high on %s" % port)
                return False

            if abs(values.slope-1)>1*0.005:
                self.step("Scaling function Slope not 1 +- 0.5%% on %s." % port)
                return False

            if abs(values.intercept)>10000*0.005:
                self.step("Scaling function Intercept not 0 +- 0.5%% on %s." % port)
                return False

        self.step("Analog input wiring, linearity and scaling factors and offsets OK")
        return True


class TestHvCvDifferences(Test):
    def __init__(self,tester,id):
        Test.__init__(self,tester,id)
        self.name = "TestHVDifferences"
        self.desc = "Test HV Pressure absolute difference calculation in the PLC"

    def test(self):
        self.step("Initial message.")

        for n in range(10):
            self.step("Testing HV and CV Pressure Diffs %d/10."%n)
            a = random.uniform(1,9)
            b = random.uniform(1,9)
            self.tester.testBox.plc.IA1.write(a)
            self.tester.testBox.plc.IA0.write(b)

            c = random.uniform(1,9)
            d = random.uniform(1,9)
            self.tester.testBox.plc.IA4.write(c)
            self.tester.testBox.plc.IA3.write(d)

            self.sleep(0.5)

            read = self.tester.plutoGateway.HVPressureDiff.read()

            if abs(read - abs(a-b)*1000) > 10000*0.005:
                self.step("HV Differences do not match analog differences! |%f - %f !|*1000 != %d (=%d) diff = %d" %(a,b,read,abs(a-b)*1000,abs(read-abs(a-b)*1000)))
                return False

            read = self.tester.plutoGateway.CVPressureDiff.read()

            if abs(read - abs(c-d)*1000) > 10000*0.005:
                self.step("CV Differences do not match analog differences! |%f - %f !|*1000 != %d (=%d) diff = %d" %(c,b,read,abs(c-d)*1000,abs(read-abs(c-d)*1000)))
                return False

        self.step("HV and CV Differences correctly calculated")
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
                self.checkChange([(self.tester.plutoGateway.HV001,1),(self.tester.plutoGateway.HVInterlockHigh,0),(self.tester.testBox.plc.I40,1),(self.tester.plutoGateway.HVInterlockHighLatchStatus, 2)], 1,compare)

                self.sleep(1)

                self.step("Try to reset the permit latch.")
                compare = self.readAllChannels()
                self.tester.plutoGateway.press_ch("HVStatLatchReset_w")
                self.checkChange([(self.tester.testBox.plc.Q1,1),(self.tester.plutoGateway.HVStat,1),(self.tester.plutoGateway.HVInterlockHighLatchStatus,0)], 2,compare)
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
                self.checkChange([ (self.tester.plutoGateway.HVStatBlock,0),(self.tester.testBox.plc.Q1,0),(self.tester.plutoGateway.HVStat,0),(self.tester.plutoGateway.HVStatBlock_w,0),(self.tester.plutoGateway.HVInterlockHighLatchStatus, 2)], 1,compare)

                self.sleep(1)

                self.step("Reset the permit latch.")
                compare = self.readAllChannels()
                self.tester.plutoGateway.press_ch("HVStatLatchReset_w")
                self.checkChange([(self.tester.testBox.plc.Q1,1),(self.tester.plutoGateway.HVStat,1),(self.tester.plutoGateway.HVInterlockHighLatchStatus,0)], 2,compare)

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
                self.checkChange([(self.tester.plutoGateway.CV001,1),(self.tester.plutoGateway.CVInterlockHigh,0),(self.tester.testBox.plc.I36,1),(self.tester.plutoGateway.CVInterlockHighLatchStatus, 2)], 1,compare)

                self.sleep(1)

                self.step("Try to reset the permit latch.")
                compare = self.readAllChannels()
                self.tester.plutoGateway.press_ch("CVStatLatchReset_w")
                self.checkChange([(self.tester.testBox.plc.Q0,1),(self.tester.plutoGateway.CVStat,1),(self.tester.plutoGateway.CVInterlockHighLatchStatus,0)], 2,compare)
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
                self.checkChange([ (self.tester.plutoGateway.CVStatBlock,0),(self.tester.testBox.plc.Q0,0),(self.tester.plutoGateway.CVStat,0),(self.tester.plutoGateway.CVStatBlock_w,0),(self.tester.plutoGateway.CVInterlockHighLatchStatus, 2)], 1,compare)

                self.sleep(1)

                self.step("Reset the permit latch.")
                compare = self.readAllChannels()
                self.tester.plutoGateway.press_ch("CVStatLatchReset_w")
                self.checkChange([(self.tester.testBox.plc.Q0,1),(self.tester.plutoGateway.CVStat,1),(self.tester.plutoGateway.CVInterlockHighLatchStatus,0)], 2,compare)

                self.checkDefault()

                self.step("CvStat permit logic correct.")
                return True

            except Exception as e:
                self.step("CvStat permit logic failed!"+str(e))
                return False


class TestCvTurboOnOfflogic(Test):
    def __init__(self,tester,id):
        Test.__init__(self,tester,id)
        self.name = "TestCvTurboOnOfflogic"
        self.desc = "Test TestCvTurboOnOfflogic permit logic"

    def test(self):
            self.step(self.desc)


            turboPumpPort = self.tester.testBox.plc.IA7
            turboPumpVoltage = self.tester.plutoGateway.CVTurboPumpVoltage
            turboPumpSpeed = self.tester.plutoGateway.CVTurboPumpSpeed
            turboPumpOn = self.tester.plutoGateway.CVTurboPumpON
            turboPumpOff = self.tester.plutoGateway.CVTurboPumpOFF
            turboPumpNotValidPort = self.tester.testBox.plc.IA7v
            turboPumpValid = self.tester.plutoGateway.CVTurboSpeedValid

            try:

                self.setDefault()
                self.checkDefault()

                for val in [0.1, 0.9]:
                    self.step(str(val))
                    turboPumpPort.write(val)
                    self.checkChange([
                        (turboPumpPort, val),
                        (turboPumpVoltage, val * 1000),
                        (turboPumpSpeed, val * 1000),
                        (turboPumpOn, int(val > 5)),
                        (turboPumpOff, int(val < 1))
                    ],
                        1)

                for val in [1.2, 4.8]:
                    self.step(str(val))
                    turboPumpPort.write(val)
                    self.checkChange([
                        (turboPumpPort, val),
                        (turboPumpVoltage, val * 1000),
                        (turboPumpSpeed, val * 1000),
                        (turboPumpOn, int(val > 5)),
                        (turboPumpOff, int(val < 1))
                    ],
                        1)

                for val in [5.1, 8, 9]:
                    self.step(str(val))

                    turboPumpPort.write(val)
                    self.checkChange([
                        (turboPumpPort, val),
                        (turboPumpVoltage, val * 1000),
                        (turboPumpSpeed, val * 1000),
                        (turboPumpOn, int(val > 5)),
                        (turboPumpOff, int(val < 1))
                    ],
                        1)

                for val in [4]:
                    self.step(str(val))
                    turboPumpPort.write(val)
                    self.checkChange([
                        (turboPumpPort, val),
                        (turboPumpVoltage, val * 1000),
                        (turboPumpSpeed, val * 1000),
                        (turboPumpOn, int(val > 5)),
                        (turboPumpOff, int(val < 1))
                    ],
                        1)

                for val in [0]:
                    self.step(str(val))
                    turboPumpPort.write(val)
                    self.checkChange([
                        (turboPumpPort, val),
                        (turboPumpVoltage, val * 1000),
                        (turboPumpSpeed, val * 1000),
                        (turboPumpOn, int(val > 5)),
                        (turboPumpOff, int(val < 1)),
                    ],
                        1)

                val = 0.5
                turboPumpPort.write(val)
                turboPumpNotValidPort.write(1)
                self.checkChange([
                    (turboPumpPort, val),
                    (turboPumpVoltage, 0),
                    (turboPumpSpeed, 0),
                    (turboPumpOn, 0),
                    (turboPumpOff, 0),
                    (turboPumpNotValidPort, 1),
                    (turboPumpValid, 0)
                ],
                    1)

                val = 8
                turboPumpPort.write(val)
                turboPumpNotValidPort.write(1)
                self.checkChange([
                    (turboPumpPort, val),
                    (turboPumpVoltage, 0),
                    (turboPumpSpeed, 0),
                    (turboPumpOn, 0),
                    (turboPumpOff, 0),
                    (turboPumpNotValidPort, 1),
                    (turboPumpValid, 0)
                ],
                    1)

                turboPumpPort.write(val)
                turboPumpNotValidPort.write(0)
                self.checkChange([
                    (turboPumpPort, val),
                    (turboPumpVoltage, val * 1000),
                    (turboPumpSpeed, val * 1000),
                    (turboPumpOn, 1),
                    (turboPumpOff, 0),
                    (turboPumpNotValidPort, 0),
                    (turboPumpValid, 1)
                ],
                    1)




                self.step("TestCvTurboOnOfflogic logic correct.")
                return True

            except Exception as e:
                self.step("TestCvTurboOnOfflogic logic failed! Failed at %s. Error: %s "%(self.step_m,str(e)))
                return False


class TestHvTurboOnOfflogic(Test):
    def __init__(self,tester,id):
        Test.__init__(self,tester,id)
        self.name = "TestHvTurboOnOfflogic"
        self.desc = "Test TestHvTurboOnOfflogic permit logic"

    def test(self):
            self.step(self.desc)


            turboPumpPort = self.tester.testBox.plc.IA6
            turboPumpVoltage = self.tester.plutoGateway.HVTurboPumpVoltage
            turboPumpSpeed = self.tester.plutoGateway.HVTurboPumpSpeed
            turboPumpOn = self.tester.plutoGateway.HVTurboPumpON
            turboPumpOff = self.tester.plutoGateway.HVTurboPumpOFF
            turboPumpNotValidPort = self.tester.testBox.plc.IA6v
            turboPumpValid = self.tester.plutoGateway.HVTurboSpeedValid



            try:

                self.setDefault()
                self.checkDefault()

                for val in [0.1,0.9]:
                    self.step(str(val))
                    turboPumpPort.write(val)
                    self.checkChange([
                                      (turboPumpPort, val),
                                      (turboPumpVoltage, val * 1000),
                                      (turboPumpSpeed, val * 1000),
                                      (turboPumpOn, int(val>5)),
                                      (turboPumpOff, int(val<1))
                                      ],
                                     1)

                for val in [1.2,4.8]:
                    self.step(str(val))
                    turboPumpPort.write(val)
                    self.checkChange([
                                      (turboPumpPort, val),
                                      (turboPumpVoltage, val * 1000),
                                      (turboPumpSpeed, val * 1000),
                                      (turboPumpOn, int(val>5)),
                                      (turboPumpOff, int(val<1))
                                      ],
                                     1)


                for val in [5.1,8,9]:
                    self.step(str(val))

                    turboPumpPort.write(val)
                    self.checkChange([
                                      (turboPumpPort, val),
                                      (turboPumpVoltage, val * 1000),
                                      (turboPumpSpeed, val * 1000),
                                      (turboPumpOn, int(val>5)),
                                      (turboPumpOff, int(val<1))
                                      ],
                                     1)

                for val in [4]:
                    self.step(str(val))
                    turboPumpPort.write(val)
                    self.checkChange([
                                      (turboPumpPort, val),
                                      (turboPumpVoltage, val * 1000),
                                      (turboPumpSpeed, val * 1000),
                                      (turboPumpOn, int(val>5)),
                                      (turboPumpOff, int(val<1))
                                      ],
                                     1)

                for val in [0]:
                    self.step(str(val))
                    turboPumpPort.write(val)
                    self.checkChange([
                                      (turboPumpPort, val),
                                      (turboPumpVoltage, val * 1000),
                                      (turboPumpSpeed, val * 1000),
                                      (turboPumpOn, int(val>5)),
                                      (turboPumpOff, int(val<1)),
                                      ],
                                     1)


                val = 0.5
                turboPumpPort.write(val)
                turboPumpNotValidPort.write(1)
                self.checkChange([
                    (turboPumpPort, val),
                    (turboPumpVoltage, 0),
                    (turboPumpSpeed,0),
                    (turboPumpOn, 0),
                    (turboPumpOff, 0),
                    (turboPumpNotValidPort,1),
                    (turboPumpValid,0)
                ],
                    1)

                val = 8
                turboPumpPort.write(val)
                turboPumpNotValidPort.write(1)
                self.checkChange([
                    (turboPumpPort, val),
                    (turboPumpVoltage, 0),
                    (turboPumpSpeed, 0),
                    (turboPumpOn, 0),
                    (turboPumpOff, 0),
                    (turboPumpNotValidPort,1),
                    (turboPumpValid,0)
                ],
                    1)

                turboPumpPort.write(val)
                turboPumpNotValidPort.write(0)
                self.checkChange([
                    (turboPumpPort, val),
                    (turboPumpVoltage, val * 1000),
                    (turboPumpSpeed, val * 1000),
                    (turboPumpOn, 1),
                    (turboPumpOff, 0),
                    (turboPumpNotValidPort,0),
                    (turboPumpValid,1)
                ],
                    1)




                self.step("TestHvTurboOnOfflogic logic correct.")
                return True

            except Exception as e:
                self.step("TestHvTurboOnOfflogic logic failed! Failed at %s. Error: %s "%(self.step_m,str(e)))
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
                self.checkChange([(turboPumpPermitPort, 0),(turboPumpPermit, 0),(turboPumpPermitLatchStatus, 2),(permitBlock,0),(permitBlock_w,0)], 1, compare)

                compare = self.readAllChannels()
                turboPumpPermitReset.press()
                self.checkChange([(turboPumpPermitPort, 1), (turboPumpPermit, 1), (turboPumpPermitLatchStatus, 0)], 1,compare)



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
                self.checkChange([(turboPumpPermitPort, 0),(turboPumpPermit, 0),(turboPumpPermitLatchStatus, 2),(permitBlock,0),(permitBlock_w,0)], 1, compare)

                compare = self.readAllChannels()
                turboPumpPermitReset.press()
                self.checkChange([(turboPumpPermitPort, 1), (turboPumpPermit, 1), (turboPumpPermitLatchStatus, 0)], 1,compare)



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

            interlockPressurePort = self.tester.testBox.plc.IA4
            interlockPressureVoltage = self.tester.plutoGateway.CVInterlockVoltage
            interlockPressurePressure = self.tester.plutoGateway.CVInterlockPressure
            interlockPressureNotValidPort = self.tester.testBox.plc.IA4v
            interlockPressureValid = self.tester.plutoGateway.CVInterlockValid

            turboPressurePort = self.tester.testBox.plc.IA3
            turboPressureVoltage = self.tester.plutoGateway.CVTurboVoltage
            turboPressurePressure = self.tester.plutoGateway.CVTurboPressure
            turboPressureNotValidPort = self.tester.testBox.plc.IA3v
            turboPressureValid = self.tester.plutoGateway.CVTurboValid

            turboPressureDiff = self.tester.plutoGateway.CVPressureDiff

            turboPumpPort = self.tester.testBox.plc.IA7
            turboPumpVoltage = self.tester.plutoGateway.CVTurboPumpVoltage
            turboPumpSpeed = self.tester.plutoGateway.CVTurboPumpSpeed
            turboPumpValid = self.tester.plutoGateway.CVTurboSpeedValid
            turboPumpNotValidPort = self.tester.testBox.plc.IA7v
            turboPumpOn = self.tester.plutoGateway.CVTurboPumpON
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



            interlockPressurePortValues = [0.18+.22]
            interlockPressureNotValidPortValues = [0,1]

            turboPressurePortValues = [0.18,.22]
            turboPressureNotValidPortValues = [0,1]

            turboPumpPortValues = [0.9,4,8]
            turboPumpNotValidPortValues = [1]

            mksPortValues = [0,1]

            CV01PortValues = [0,1]

            size = 1*2*2*2*3*1*2*2

            self.setDefault()
            vccOpen_w.press()

            self.sleep(1)

            n = 0

            try:
                for turboPressurePortValue in turboPressurePortValues:
                    for turboPressureNotValidPortValue in turboPressureNotValidPortValues:
                        for interlockPressurePortValue in interlockPressurePortValues:
                            for interlockPressureNotValidPortValue in interlockPressureNotValidPortValues:
                                for turboPumpPortValue in turboPumpPortValues:
                                    for turboPumpNotValidPortValue in turboPumpNotValidPortValues:
                                        for mksPortValue in mksPortValues:
                                            for CV01PortValue in CV01PortValues:
                                                n=n+1
                                                print("--------------------------------------------------------------------------")
                                                print(n,size)

                                                if n<0:
                                                    continue

                                                turboPumpPermitValue = turboPressurePortValue<0.22 and not turboPressureNotValidPortValue and mksPortValue == 1

                                                if (turboPumpPortValue > 5 or turboPumpNotValidPortValue) and (mksPortValue == 0):
                                                    vccNotForcedCloseLatchValue = 0
                                                else:
                                                    vccNotForcedCloseLatchValue = 1

                                                vccNotForcedCloseLatchStatusValue = int(not bool(vccNotForcedCloseLatchValue))


                                                turboPumpPermitPortValue = turboPumpPermitValue
                                                turboPumpPermitLatchStatusValue = int(not bool(turboPumpPermitPortValue))


                                                vccAllowedOpenLatchValue = (turboPumpPortValue > 5 and not turboPumpNotValidPortValue and CV01PortValue) or (turboPumpPortValue <1 and not turboPumpNotValidPortValue and not turboPressureNotValidPortValue and not interlockPressureNotValidPortValue and abs(turboPressurePortValue-interlockPressurePortValue)<0.22)
                                                vccAllowedOpenLatchStatusValue = int(not bool(vccAllowedOpenLatchValue))


                                                ##################

                                                compare = self.readAllChannels()


                                                CV01Port.write(CV01PortValue)
                                                mksPort.write(mksPortValue)

                                                turboPumpPort.write(turboPumpPortValue)
                                                turboPumpNotValidPort.write(turboPumpNotValidPortValue)

                                                turboPressurePort.write(turboPressurePortValue)
                                                turboPressureNotValidPort.write(turboPressureNotValidPortValue)

                                                interlockPressurePort.write(interlockPressurePortValue)
                                                interlockPressureNotValidPort.write(interlockPressureNotValidPortValue)


                                                self.sleep(.6)


                                                self.pressChannels([turboPumpPermitReset_w,vccAllowedOpenLatchReset_w,vccNotForcedCloseLatchReset_w])



                                                self.checkChange([(mksPort, mksPortValue),
                                                                  (mks, mksPortValue),

                                                                  (CV01Port,CV01PortValue),
                                                                  (CV01,CV01PortValue),



                                                                  (turboPressurePort, turboPressurePortValue),
                                                                  (turboPressureVoltage, turboPressurePortValue * 1000 * int(not bool(turboPressureNotValidPortValue))),
                                                                  (turboPressurePressure, turboPressurePortValue * 1000 * int(not bool(turboPressureNotValidPortValue))),
                                                                  (turboPressureNotValidPort,turboPressureNotValidPortValue),
                                                                  (turboPressureValid,not turboPressureNotValidPortValue),

                                                                  (interlockPressurePort, interlockPressurePortValue),
                                                                  (interlockPressureVoltage, interlockPressurePortValue * 1000 * int(not bool(interlockPressureNotValidPortValue))),
                                                                  (interlockPressurePressure, interlockPressurePortValue * 1000 * int(not bool(interlockPressureNotValidPortValue))),
                                                                  (interlockPressureNotValidPort, interlockPressureNotValidPortValue),
                                                                  (interlockPressureValid, not interlockPressureNotValidPortValue),

                                                                  (turboPressureDiff,abs(interlockPressurePortValue * 1000 * int(not bool(interlockPressureNotValidPortValue)) - turboPressurePortValue * 1000 * int(not bool(turboPressureNotValidPortValue)))),


                                                                  (turboPumpPort, turboPumpPortValue),
                                                                  (turboPumpVoltage, turboPumpPortValue * 1000 * int(not bool(turboPumpNotValidPortValue))),
                                                                  (turboPumpSpeed, turboPumpPortValue * 1000 * int(not bool(turboPumpNotValidPortValue))),
                                                                  (turboPumpOn, int(turboPumpPortValue > 5) and not bool(turboPumpNotValidPortValue) ),
                                                                  (turboPumpOff, int(turboPumpPortValue < 1)  and not bool(turboPumpNotValidPortValue) ),
                                                                  (turboPumpNotValidPort,turboPumpNotValidPortValue),
                                                                  (turboPumpValid, not turboPumpNotValidPortValue),

                                                                  (turboPumpPermitPort, turboPumpPermitPortValue),
                                                                  (turboPumpPermit, turboPumpPermitValue),
                                                                  (turboPumpPermitLatchStatus, turboPumpPermitLatchStatusValue),

                                                                  (vccAllowedOpenLatch,vccAllowedOpenLatchValue),
                                                                  (vccAllowedOpenLatchStatus,vccAllowedOpenLatchStatusValue),

                                                                  (vccNotForcedCloseLatch,vccNotForcedCloseLatchValue),
                                                                  (vccNotForcedCloseLatchStatus,vccNotForcedCloseLatchStatusValue),

                                                                  (vcc,vccNotForcedCloseLatchValue),
                                                                  (vccPort,vccNotForcedCloseLatchValue),

                                                                  (statPort,None),
                                                                  (stat,None),
                                                                  (statInterlockHigh,None),
                                                                  (statInterlockHighLatchStatus,None)


                                                                  ],                                                     1,compare)


                                                #can always close
                                                vccClose_w.press()
                                                self.checkChange([(vcc, 0),
                                                                  (vccPort, 0),
                                                                  ], 1,checkBlinks=False)



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




                                                #input()

                                                vccAllowedOpenLatchValueOld = vccAllowedOpenLatch.read()
                                                vccNotForcedCloseLatchValueOld = vccNotForcedCloseLatch.read()
                                                turboPumpPermitPortValueOld = turboPumpPermitPort.read()

                                                self.writeChannels(compare)
                                                self.sleep(.5)

                                                if vccAllowedOpenLatchValueOld and not vccAllowedOpenLatch.read():
                                                    vccAllowedOpenLatchReset_w.press()

                                                if vccNotForcedCloseLatchValueOld and not vccNotForcedCloseLatch.read():
                                                    vccNotForcedCloseLatchReset_w.press()

                                                if turboPumpPermitPortValueOld and not turboPumpPermitPort.read():
                                                    turboPumpPermitReset_w.press()


                                                press = []
                                                change1 = []
                                                change2 = []


                                               # input()

                                                if not bool(vccAllowedOpenLatchValue):

                                                    change1.append((vccAllowedOpenLatchStatus, 2))


                                                    press.append(vccAllowedOpenLatchReset_w)

                                                    change2.append((vccAllowedOpenLatch, 1))
                                                    change2.append((vccAllowedOpenLatchStatus, 0))


                                                if not bool(vccNotForcedCloseLatchValue):
                                                    change1.append((vccNotForcedCloseLatchStatus, 2))

                                                    press.append(vccNotForcedCloseLatchReset_w)

                                                    change2.append((vccNotForcedCloseLatch, 1))
                                                    change2.append((vccNotForcedCloseLatchStatus, 0))


                                                if not bool(turboPumpPermitPortValue):

                                                    change1.append((turboPumpPermitLatchStatus, 2))
                                                    press.append(turboPumpPermitReset_w)

                                                    change2.append((turboPumpPermitPort, 1))
                                                    change2.append((turboPumpPermit, 1))
                                                    change2.append((turboPumpPermitLatchStatus, 0))





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





                self.step("HvTurboPump permit logic correct.")
                return True

            except ValueError as e:
                self.step("HvTurboPump permit logic failed! Failed at %s. Error: %s "%(self.step_m,str(e)))
                return False


class TestHvTurboPermitAuto(Test):
    def __init__(self,tester,id):
        Test.__init__(self,tester,id)
        self.name = "TestHvTurboPermitAuto"
        self.desc = "Test TestHvTurboPermitAuto permit logic"

    def test(self):
            self.step(self.desc)

            interlockPressurePort = self.tester.testBox.plc.IA1
            interlockPressureVoltage = self.tester.plutoGateway.HVInterlockVoltage
            interlockPressurePressure = self.tester.plutoGateway.HVInterlockPressure
            interlockPressureNotValidPort = self.tester.testBox.plc.IA1v
            interlockPressureValid = self.tester.plutoGateway.HVInterlockValid

            turboPressurePort = self.tester.testBox.plc.IA0
            turboPressureVoltage = self.tester.plutoGateway.HVTurboVoltage
            turboPressurePressure = self.tester.plutoGateway.HVTurboPressure
            turboPressureNotValidPort = self.tester.testBox.plc.IA0v
            turboPressureValid = self.tester.plutoGateway.HVTurboValid

            turboPressureDiff = self.tester.plutoGateway.HVPressureDiff

            turboPumpPort = self.tester.testBox.plc.IA6
            turboPumpVoltage = self.tester.plutoGateway.HVTurboPumpVoltage
            turboPumpSpeed = self.tester.plutoGateway.HVTurboPumpSpeed
            turboPumpValid = self.tester.plutoGateway.HVTurboSpeedValid
            turboPumpNotValidPort = self.tester.testBox.plc.IA6v
            turboPumpOn = self.tester.plutoGateway.HVTurboPumpON
            turboPumpOff = self.tester.plutoGateway.HVTurboPumpOFF



            turboPumpPermitPort = self.tester.testBox.plc.Q5
            turboPumpPermit = self.tester.plutoGateway.VhxPumpPerm
            turboPumpPermitLatchStatus = self.tester.plutoGateway.VhxPumpPermLatchStatus
            turboPumpPermitReset_w = self.tester.plutoGateway.VhxPumpPermReset_w

            mksPort = self.tester.testBox.plc.I34
            mks = self.tester.plutoGateway.MKS925


            vccAllowedOpenLatch = self.tester.plutoGateway.MainVhxVccAllowedOpenLatch
            vccAllowedOpenLatchStatus = self.tester.plutoGateway.MainVhxVccAllowedOpenLatchStatus
            vccAllowedOpenLatchReset_w = self.tester.plutoGateway.MainVhxVccAllowedOpenLatchReset_w

            vccNotForcedCloseLatch = self.tester.plutoGateway.MainVhxVccNotForcedCloseLatch
            vccNotForcedCloseLatchStatus = self.tester.plutoGateway.MainVhxVccNotForcedCloseLatchStatus
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



            interlockPressurePortValues = [0.18+.22]
            interlockPressureNotValidPortValues = [0,1]

            turboPressurePortValues = [0.18,.22]
            turboPressureNotValidPortValues = [0,1]

            turboPumpPortValues = [0.9,4,8]
            turboPumpNotValidPortValues = [1]

            mksPortValues = [0,1]

            CV01PortValues = [0,1]

            size = 1*2*2*2*3*1*2*2

            self.setDefault()
            vccOpen_w.press()

            self.sleep(1)

            n = 0

            try:
                for turboPressurePortValue in turboPressurePortValues:
                    for turboPressureNotValidPortValue in turboPressureNotValidPortValues:
                        for interlockPressurePortValue in interlockPressurePortValues:
                            for interlockPressureNotValidPortValue in interlockPressureNotValidPortValues:
                                for turboPumpPortValue in turboPumpPortValues:
                                    for turboPumpNotValidPortValue in turboPumpNotValidPortValues:
                                        for mksPortValue in mksPortValues:
                                            for CV01PortValue in CV01PortValues:
                                                n=n+1
                                                print("--------------------------------------------------------------------------")
                                                print(n,size)

                                                if n<0:
                                                    continue

                                                turboPumpPermitValue = turboPressurePortValue<0.22 and not turboPressureNotValidPortValue

                                                if (turboPumpPortValue > 5 or turboPumpNotValidPortValue) and (mksPortValue == 0):
                                                    turboPumpPermitValue = 0
                                                    vccNotForcedCloseLatchValue = 0

                                                else:
                                                    vccNotForcedCloseLatchValue = 1

                                                vccNotForcedCloseLatchStatusValue = int(not bool(vccNotForcedCloseLatchValue))




                                                turboPumpPermitPortValue = turboPumpPermitValue
                                                turboPumpPermitLatchStatusValue = int(not bool(turboPumpPermitPortValue))


                                                vccAllowedOpenLatchValue = (turboPumpPortValue > 5 and not turboPumpNotValidPortValue and CV01PortValue) or (turboPumpPortValue <1 and not turboPumpNotValidPortValue and not turboPressureNotValidPortValue and not interlockPressureNotValidPortValue and abs(turboPressurePortValue-interlockPressurePortValue)<0.22)
                                                vccAllowedOpenLatchStatusValue = int(not bool(vccAllowedOpenLatchValue))





                                                ##################

                                                compare = self.readAllChannels()


                                                CV01Port.write(CV01PortValue)
                                                mksPort.write(mksPortValue)

                                                turboPumpPort.write(turboPumpPortValue)
                                                turboPumpNotValidPort.write(turboPumpNotValidPortValue)

                                                turboPressurePort.write(turboPressurePortValue)
                                                turboPressureNotValidPort.write(turboPressureNotValidPortValue)

                                                interlockPressurePort.write(interlockPressurePortValue)
                                                interlockPressureNotValidPort.write(interlockPressureNotValidPortValue)


                                                self.sleep(.6)


                                                self.pressChannels([turboPumpPermitReset_w,vccAllowedOpenLatchReset_w,vccNotForcedCloseLatchReset_w])



                                                self.checkChange([(mksPort, mksPortValue),
                                                                  (mks, mksPortValue),

                                                                  (CV01Port,CV01PortValue),
                                                                  (CV01,CV01PortValue),



                                                                  (turboPressurePort, turboPressurePortValue),
                                                                  (turboPressureVoltage, turboPressurePortValue * 1000 * int(not bool(turboPressureNotValidPortValue))),
                                                                  (turboPressurePressure, turboPressurePortValue * 1000 * int(not bool(turboPressureNotValidPortValue))),
                                                                  (turboPressureNotValidPort,turboPressureNotValidPortValue),
                                                                  (turboPressureValid,not turboPressureNotValidPortValue),

                                                                  (interlockPressurePort, interlockPressurePortValue),
                                                                  (interlockPressureVoltage, interlockPressurePortValue * 1000 * int(not bool(interlockPressureNotValidPortValue))),
                                                                  (interlockPressurePressure, interlockPressurePortValue * 1000 * int(not bool(interlockPressureNotValidPortValue))),
                                                                  (interlockPressureNotValidPort, interlockPressureNotValidPortValue),
                                                                  (interlockPressureValid, not interlockPressureNotValidPortValue),

                                                                  (turboPressureDiff,abs(interlockPressurePortValue * 1000 * int(not bool(interlockPressureNotValidPortValue)) - turboPressurePortValue * 1000 * int(not bool(turboPressureNotValidPortValue)))),


                                                                  (turboPumpPort, turboPumpPortValue),
                                                                  (turboPumpVoltage, turboPumpPortValue * 1000 * int(not bool(turboPumpNotValidPortValue))),
                                                                  (turboPumpSpeed, turboPumpPortValue * 1000 * int(not bool(turboPumpNotValidPortValue))),
                                                                  (turboPumpOn, int(turboPumpPortValue > 5) and not bool(turboPumpNotValidPortValue) ),
                                                                  (turboPumpOff, int(turboPumpPortValue < 1)  and not bool(turboPumpNotValidPortValue) ),
                                                                  (turboPumpNotValidPort,turboPumpNotValidPortValue),
                                                                  (turboPumpValid, not turboPumpNotValidPortValue),

                                                                  (turboPumpPermitPort, turboPumpPermitPortValue),
                                                                  (turboPumpPermit, turboPumpPermitValue),
                                                                  (turboPumpPermitLatchStatus, turboPumpPermitLatchStatusValue),

                                                                  (vccAllowedOpenLatch,vccAllowedOpenLatchValue),
                                                                  (vccAllowedOpenLatchStatus,vccAllowedOpenLatchStatusValue),

                                                                  (vccNotForcedCloseLatch,vccNotForcedCloseLatchValue),
                                                                  (vccNotForcedCloseLatchStatus,vccNotForcedCloseLatchStatusValue),

                                                                  (vcc,vccNotForcedCloseLatchValue),
                                                                  (vccPort,vccNotForcedCloseLatchValue),

                                                                  (statPort,None),
                                                                  (stat,None),
                                                                  (statInterlockHigh,None),
                                                                  (statInterlockHighLatchStatus,None)


                                                                  ],                                                     1,compare)


                                                #can always close
                                                vccClose_w.press()
                                                self.checkChange([(vcc, 0),
                                                                  (vccPort, 0),
                                                                  ], 1,checkBlinks=False)



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




                                                #input()

                                                vccAllowedOpenLatchValueOld = vccAllowedOpenLatch.read()
                                                vccNotForcedCloseLatchValueOld = vccNotForcedCloseLatch.read()
                                                turboPumpPermitPortValueOld = turboPumpPermitPort.read()

                                                self.writeChannels(compare)
                                                self.sleep(.5)

                                                if vccAllowedOpenLatchValueOld and not vccAllowedOpenLatch.read():
                                                    vccAllowedOpenLatchReset_w.press()

                                                if vccNotForcedCloseLatchValueOld and not vccNotForcedCloseLatch.read():
                                                    vccNotForcedCloseLatchReset_w.press()

                                                if turboPumpPermitPortValueOld and not turboPumpPermitPort.read():
                                                    turboPumpPermitReset_w.press()


                                                press = []
                                                change1 = []
                                                change2 = []


                                               # input()

                                                if not bool(vccAllowedOpenLatchValue):

                                                    change1.append((vccAllowedOpenLatchStatus, 2))


                                                    press.append(vccAllowedOpenLatchReset_w)

                                                    change2.append((vccAllowedOpenLatch, 1))
                                                    change2.append((vccAllowedOpenLatchStatus, 0))


                                                if not bool(vccNotForcedCloseLatchValue):
                                                    change1.append((vccNotForcedCloseLatchStatus, 2))

                                                    press.append(vccNotForcedCloseLatchReset_w)

                                                    change2.append((vccNotForcedCloseLatch, 1))
                                                    change2.append((vccNotForcedCloseLatchStatus, 0))


                                                if not bool(turboPumpPermitPortValue):

                                                    change1.append((turboPumpPermitLatchStatus, 2))
                                                    press.append(turboPumpPermitReset_w)

                                                    change2.append((turboPumpPermitPort, 1))
                                                    change2.append((turboPumpPermit, 1))
                                                    change2.append((turboPumpPermitLatchStatus, 0))





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




