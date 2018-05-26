from pydm.PyQt.QtCore import *
from pluto_gateway import PlutoGateway
from test_box import TestBox
import time



class Tester(QThread):

    test_line_update = pyqtSignal(int)
    monitor_update = pyqtSignal(str,str,float,str,int,str)

    def __init__(self):
        QThread.__init__(self)

        self.tests = []

        self.current_test = ""
        self.current_test_message = ""
        self.progress_bar = 0
        self.progress_count = ""
        self.result_bar_color = 0
        self.result_bar_message = ""

        self.current_test_obj = None

        self.abortion = False

        self.plutoGateway = None
        self.testBox = None

        self.running_tests = []


        self.plutoGateway = PlutoGateway(self)
        self.testBox = TestBox(self)


        self.always = False




    def run_all(self):
        #self.always = True
        if not self.isRunning():
            self.clean_display()
            self.running_tests = self.tests
            self.start()

    def run_selected(self):
        if not self.isRunning():
            self.clean_display()
            selected_tests = []
            for test in self.tests:
                if test.selected == 2:
                    selected_tests.append(test)
            self.running_tests = selected_tests
            self.start()

    def abort(self):
        self.abortion = True

        if self.current_test_obj is not None:
            self.current_test_obj.abort()

        self.terminate()

        if self.abortion:
            self.progress_bar = 0.0
            self.progress_count = ""
            self.current_test = ""
            self.current_test_message = ""
            self.result_bar_message = "Aborted."
            self.update_menu()

        self.reconnect()

    def clean_display(self):
        for test in self.tests:
            test.result = ""
            test.details = ""
            self.update_test_line(test.id)

    def update_test_line(self,id):
        self.test_line_update.emit(id)

    def update_menu(self):
        self.monitor_update.emit(self.current_test,self.current_test_message,self.progress_bar,self.progress_count,self.result_bar_color,self.result_bar_message)

    def reconnect(self,timeout=15):

        #start = time.time()
        #while time.time() - start < timeout:
        #    try:
        if self.plutoGateway is not None:
            self.plutoGateway.close()


        self.plutoGateway = None

        self.plutoGateway = PlutoGateway(self)
          #  except:
          #      pass

        start = time.time()
        while time.time() - start < timeout:
            try:
                if self.testBox is not None:
                    self.testBox.close()

                self.testBox = None
                self.testBox = TestBox(self)
                break
            except:
                self.sleep(1)

    def run(self):

        while 1:
            self.reconnect()

            self.n_tests = len(self.running_tests)

            self.progress_bar = 0
            self.progress_count = "0 / " + str(self.n_tests)
            self.current_test = ""
            self.current_test_message = ""
            self.result_bar_message = "Running..."
            self.update_menu()

            self.abortion = False

            results = []

            for n, test in enumerate(self.running_tests):



               # self.reconnect()

                self.current_test_obj = test

                test.run()
                self.progress_bar = (n + 1) / float(self.n_tests)
                self.progress_count = str(n + 1) + " / " + str(self.n_tests)

                self.update_menu()

                if test.result == "OK":
                    results.append(True)
                else:
                    results.append(False)

                self.sleep(0.2)

            self.current_test = ""
            self.current_test_message = ""
            if all(results):
                self.result_bar_message = "Finished."
            else:
                self.result_bar_message = "Failed."
            self.update_menu()

            #if not self.always:
            #break
            self.clean_display()

    def log(self,log):
        self.current_test_obj.log(log)


class Test:
    def __init__(self,tester,id):

        self.tester=tester
        self.running = 0 # 0,1,2
        self.abortion = False

        self.name = ""
        self.desc = ""
        self.selected=0
        self.result=""
        self.details=""
        self.step_m = ""

        self.id = id

    def update(self):
        self.tester.current_test = str(self.id+1) + "- " + self.name
        self.tester.current_test_message = self.details
        self.tester.update_menu()
        self.tester.update_test_line(self.id)



    def run(self):
        self.abortion = False
        self.running = 1
        try:
            result = self.test()
        except Exception as e:
            result = 2
            self.details = str(e)
            print (e)

        if result == False:
            self.result = "FAILED"
        elif result == True:
            self.result = "OK"
        elif result == 2:
            self.result = "error"
        self.running = 0

        self.update()

    def abort(self):
        self.abortion = True
        self.running = 0
        self.result = "Aborted"
        self.step_m = "Aborted"
        self.update()

    def test(self):
        raise ValueError("test() not implemented.")


    def sleep(self,s):
        count = 0
        while count < s:
            time.sleep(1/100.0)
            count +=1/100.0
            if self.abortion:
                break

    def log(self,log):
        self.details = log
        self.update()
        print(log)

    def step(self,step):
        self.step_m = step
        self.update()
        print("-----> "+str(step))

    def set_run_button(self,button):
        self.run_button = button
        self.run_button.clicked.connect(self.button_run)

    def button_run(self):
        if not self.tester.isRunning():
            self.tester.running_tests = [self]
            self.tester.start()

    def readChannels(self, chs):
  #      self.log("Reading channels")
        results = []
        digitalBlink = []

        for ch in chs:
            if ch.type == "DigitalBlink":
                digitalBlink.append(ch)
            else:
                results.append((ch, ch.read()))

#        self.log("Reading DigitalBlink channels")
        blinks = self.readDigitalBlinks(digitalBlink)
        for i, ch in enumerate(digitalBlink):
            results.append((ch, blinks[i]))

        return results

    def readDigitalBlinks(self,chs,timeout=1):
            zero = [0] * len(chs)
            one = [0] * len(chs)
            results= [None] * len(chs)

            start = time.time()
            while time.time() - start < timeout and len(chs)>0:
                time.sleep(0.03)
                for i,ch in enumerate(chs):
                  read = ch.read()
                  if read:
                        one[i] += 1
                  else:
                        zero[i] += 1
                #if sum(zero)+sum(one) > len(chs)*2*2:
                #    break

            for i,v in enumerate(zero):
                if zero[i] > 2 and one[i] > 2:
                    results[i]=(2)
                elif zero[i] > 2 and one[i] == 0 :
                    results[i]=(0)
                elif zero[i] == 0 and one[i] > 2 :
                    results[i]=(1)
            return results

    def readAllChannels(self):
        chs = self.tester.testBox.plc.channels + self.tester.plutoGateway.channels
        return self.readChannels(chs)

    def readPermitChannels(self):
        chs = self.tester.testBox.plc.channels + self.tester.plutoGateway.channels
        return self.readChannels(chs)



    def checkChannels(self,channelsValues,checkBlinks = True):
        digitalBlink = []
        for chV in channelsValues:
            if chV[1] is not  None:
                if chV[0].type == "DigitalBlink":
                    digitalBlink.append(chV)
                else:
                    if not chV[0].checkValue(chV[1]):
                        raise ValueError("Do not match. %s should be %s. It is %s"%(chV[0].ch,str(chV[1]),str(chV[0].read())))

        if checkBlinks:
            if not self.checkDigitalBlinks(digitalBlink):
                raise ValueError("Blinks do not match ")

        return True

    def checkDigitalBlinks(self,channelsValues,timeout=0.5):
            vals = []
            chs = []
            for chV in channelsValues:
                vals.append(int(chV[1]))
                chs.append(chV[0])
            return vals == self.readDigitalBlinks(chs,timeout)


    def checkDefault(self):
        self.log("Checking normal operation values")
        chs = []
        for ch in self.tester.testBox.plc.channels:
            if ch.default_value != "":
                chs.append((ch, ch.default_value))
        for ch in self.tester.plutoGateway.channels:
            if ch.default_value != "":
                chs.append((ch, ch.default_value))

        try:
            self.checkChange(chs,1)
            self.log("Normal operation values confirmed.")
            return True
        except ValueError as e:
            error = "Normal operation values not found. :: " + str(e)
            self.log(error)
            raise ValueError(error)




    def setDefault(self):
        self.log("Setting normal operation values.")

        for a in range(3):
            press_chs =[]

            for ch in self.tester.testBox.plc.channels:
                if str(ch.default_value) != "":
                    try:
                        ch.write(float(ch.default_value))
                    except ValueError:
                        self.log("Can't write to testBox.plc " + ch.ch)
                        raise ValueError("Can't write to " + ch.ch)

            for ch in self.tester.plutoGateway.channels:
                if str(ch.default_value) != "" and str(ch.default_value) != "P" and ch.ch.find("_w") >= 0:
                    try:
                        ch.write(int(ch.default_value))
                    except ValueError:
                        self.log("Can't write to plutoGateway " + ch.ch)
                        raise ValueError("Can't write to " + ch.ch)
                elif str(ch.default_value) == "P":
                    #ch.press()
                    press_chs.append(ch)

            self.sleep(0.2)

            for ch in press_chs:
                ch.write(1)
            self.sleep(0.3)

            for ch in press_chs:
                ch.write(0)

            if self.checkDefault():
                self.log("Normal operation values set.")
                return True



    def checkDuring(self,channelsValues, timeout):
        self.log("Wait for %d s with no changes.")

        start = time.time()
        while time.time() - start < timeout:
            for ch in (channelsValues):
                read = ch[0].read()
                if read != ch[1]:
                    error = "A channel not suposed to change changed its value. :: %s in %s, not %s."%(ch[0].ch,read, ch[1])
                    self.log(error)
                    raise ValueError(error)

        return True

    def checkChange(self,channelsValues, timeout, compare=None,checkBlinks=True):
        self.log("Wait for a change in the selected channels.")
        for chV in channelsValues:
            self.log(chV[0].ch+"\t"+str(chV[1]))

        change_ok = False
        start = time.time()
        while time.time() - start < timeout:
            try:
                self.checkChannels(channelsValues)
                change_ok=True
                break
            except ValueError as e:
                pass
            self.sleep(0.1)
        if not change_ok:
            try:
                self.checkChannels(channelsValues)
            except ValueError as e:
                error = "A value expected to change did not change. ::" + str(e)
                self.log(error)
                raise ValueError(error)

        else:
            if compare is not None:
                self.log ("Check if any other channel has changed.")
                chs = []
                for chV in compare:
                    scan = True
                    for notScanV in channelsValues:
                        if notScanV[0].ch is chV[0].ch:
                            scan = False
                    if scan:
                        chs.append(chV)
                try:
                    self.checkChannels(chs, checkBlinks=checkBlinks)
                    self.log("No other channel has changed.")
                except ValueError as e:
                    error = "A value not supposed to change changed. :: "+ str(e)
                    self.log(error)
                    raise ValueError(error)

            self.log("Channels changed as expected.")
            return True


    def writeChannels(self, chVs):

        for chV in chVs:
            try:
                chV[0].write(chV[1])
            except:
                pass



    def pressChannels(self, chs):

        for ch in chs:
            ch.write(0)

        self.sleep(0.1)

        for ch in chs:
            ch.write(1)
        self.sleep(0.3)

        for ch in chs:
            ch.write(0)

        self.sleep(0.1)















