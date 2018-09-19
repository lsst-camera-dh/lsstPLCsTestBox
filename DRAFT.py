self.step(self.desc)

inputs = dict()

# PLC 2 inputs
inputs['p1_tsw0']['port'] = self.tester.testBox.plc.P1.IA0
inputs['p1_tsw1']['port'] = self.tester.testBox.plc.P1.IA1
inputs['p1_tsw2']['port'] = self.tester.testBox.plc.P1.IA2
inputs['p1_tsw3']['port'] = self.tester.testBox.plc.P1.IA3
inputs['p1_noLeak']['port'] = self.tester.testBox.plc.P1.I4
inputs['p1_leak']['port'] = self.tester.testBox.plc.P1.I5
inputs['p1_noSmoke']['port'] = self.tester.testBox.plc.P1.I6
inputs['p1_noLeakFault']['port'] = self.tester.testBox.plc.P1.I7

inputs['p1_tsw0']['values'] = [0, 1]
inputs['p1_tsw1']['values'] = [0, 1]
inputs['p1_tsw2']['values'] = [0, 1]
inputs['p1_tsw3']['values'] = [0, 1]
inputs['p1_noLeak']['values'] = [0, 1]
inputs['p1_leak']['values'] = [0, 1]
inputs['p1_noSmoke']['values'] = [0, 1]
inputs['p1_noLeakFault']['values'] = [0, 1]

# PLC 2 inputs
inputs['p2_temp0']['port'] = self.tester.testBox.plc.P2.IA0
inputs['p2_temp1']['port'] = self.tester.testBox.plc.P2.IA1
inputs['p2_temp2']['port'] = self.tester.testBox.plc.P2.IA2
inputs['p2_temp3']['port'] = self.tester.testBox.plc.P2.IA3
inputs['p2_noSmokeFault']['port'] = self.tester.testBox.plc.P2.I4
inputs['p2_noSmokeWarning']['port'] = self.tester.testBox.plc.P2.I5
inputs['p2_masterReset']['port'] = self.tester.testBox.plc.P2.I7

low = 1
normal = 5
high = 10

inputs['p2_temp0']['values'] = [0, low, normal, high]
inputs['p2_temp1']['values'] = [0, low, normal, high]
inputs['p2_temp2']['values'] = [0, low, normal, high]
inputs['p2_temp3']['values'] = [0, low, normal, high]
inputs['p2_noSmokeFault']['values'] = [0, 1]
inputs['p2_noSmokeWarning']['values'] = [0, 1]
inputs['p2_masterReset']['values'] = [0]

# PLC 3 inputs
inputs['p3_temp0']['port'] = self.tester.testBox.plc.P3.IA0
inputs['p3_temp1']['port'] = self.tester.testBox.plc.P3.IA1
inputs['p3_temp2']['port'] = self.tester.testBox.plc.P3.IA2
inputs['p3_temp3']['port'] = self.tester.testBox.plc.P3.IA3
inputs['p3_hvStat']['port'] = self.tester.testBox.plc.P3.I5
inputs['p3_cvStat']['port'] = self.tester.testBox.plc.P3.I6

low = 1
normal = 5
high = 10

inputs['p3_temp0']['values'] = [0, low, normal, high]
inputs['p3_temp1']['values'] = [0, low, normal, high]
inputs['p3_temp2']['values'] = [0, low, normal, high]
inputs['p3_temp3']['values'] = [0, low, normal, high]
inputs['p3_hvStat']['values'] = [0, 1]
inputs['p3_cvStat']['values'] = [0, 1]