from pydm.PyQt.QtCore import *
from pluto_gateway import PlutoGateway
from test_box import TestBox
import time
import logging

class Tester(QThread):

    test_line_update = pyqtSignal(int)
    monitor_update = pyqtSignal(str,str,float,str,int,str)

    def __init__(self,testBox_chs , plutoGateway_chs):
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

        self.plutoGateway_chs= plutoGateway_chs
        self.testBox_chs = testBox_chs

        self.plutoGateway = None #PlutoGateway(self,self.plutoGateway_chs)
        self.testBox = None #TestBox(self,self.testBox_chs)

        self.logger = logging.getLogger("tester")

    def connectTestBox(self,timeout=15):
        start = time.time()
        while time.time() - start < timeout:
            try:
                if self.testBox is not None:
                    self.testBox.close()
                    self.sleep(1)

                self.testBox = None
                self.testBox = TestBox(self, self.testBox_chs)
                self.logger.warning("Reconnected to Testbox.")
                break
            except:
                self.sleep(1)

    def connectGateway(self,timeout=15):
        start = time.time()
        while time.time() - start < timeout:
            try:
                if self.plutoGateway is not None:
                    self.plutoGateway.close()
                    self.sleep(1)

                self.plutoGateway = None
                self.plutoGateway = PlutoGateway(self,self.plutoGateway_chs)
                self.logger.warning("Reconnected to Pluto Gateway")
                break
            except Exception as e:
                self.sleep(1)
                print(e)


    def run_all(self):
        if not self.isRunning():
            self.clean_display()
            self.running_tests = self.tests
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

            self.logger.warning("aborted by the user")

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

        self.sleep(0.5)

        self.connectGateway()

        self.connectTestBox(timeout)




    def run(self):

        while 1:

            self.n_tests = len(self.running_tests)

            self.progress_bar = 0
            self.progress_count = "0 / " + str(self.n_tests)
            self.current_test = ""
            self.current_test_message = ""
            self.result_bar_message = "Running..."
            self.update_menu()

            self.abortion = False

            results = []

            for test in self.running_tests:
                self.logger.info('>>>>>>>>>>> Will run ' + str(test.name))


            for n, test in enumerate(self.running_tests):

                self.reconnect()

                self.current_test_obj = test

                self.logger.info('>>>>>>> Running '+str(self.current_test_obj.name))
                self.logger.info ('>>>>>>>>>>>>. '+str(self.current_test_obj.desc))

                test.run()
                self.progress_bar = (n + 1) / float(self.n_tests)
                self.progress_count = str(n + 1) + " / " + str(self.n_tests)

                self.update_menu()

                if test.result == "OK":
                    results.append(True)
                    self.logger.info('>>>>>>> ' + str(self.current_test_obj.name)+' passed!')
                else:
                    results.append(False)
                    self.logger.error('>>>>>>> ' + str(self.current_test_obj.name) + ' failed!')

                print(n)

                self.sleep(0.2)

            self.current_test = ""
            self.current_test_message = ""
            if all(results):
                self.result_bar_message = "Finished."
                self.logger.info('>>>>>>> Finished with success!')
            else:
                self.result_bar_message = "Failed."
                self.logger.error('>>>>>>> Tests Failed!')
            self.update_menu()

            break

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

        self.logger = logging.getLogger(self.name)

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

    def log(self,log,error=False):
        self.details = log
        self.update()
        if error:
            self.logger.error(log)
        else:
            self.logger.info(log)

        #print(log)

    def step(self,step,error=False):
        self.step_m = step
        self.update()
        if error:
            self.logger.error("-----> "+str(step))
        else:
            self.logger.info("-----> "+str(step))
        print("-----> "+str(step)) #TODO apagar

    def set_run_button(self,button):
        self.run_button = button
        self.run_button.clicked.connect(self.button_run)

    def button_run(self):
        if not self.tester.isRunning():
            self.tester.running_tests = [self]
            self.tester.start()

    def readChannels(self, chs):
        results = []
        digitalBlink = []

        for ch in chs:
            if ch.type == "DigitalBlink":
                digitalBlink.append(ch)
            else:
                results.append((ch, ch.read()))

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

            for i,v in enumerate(zero):
                if zero[i] > 2 and one[i] > 2:
                    results[i]=(2)
                elif zero[i] > 2 and one[i] == 0 :
                    results[i]=(0)
                elif zero[i] == 0 and one[i] > 2 :
                    results[i]=(1)
            return results

    def readAllChannels(self):
        self.log("Reading all channels")
        #chs = []
        chs = self.tester.testBox.plc.channels + self.tester.plutoGateway.channels
        return self.readChannels(chs)


    def checkChannels(self,channelsValues,checkBlinks = True):

        digitalBlink = []
        for chV in channelsValues:
            if chV[1] is not None:
                if chV[0].type == "DigitalBlink":
                    digitalBlink.append(chV)
                else:
                    self.log("Checking channel %s. Expected %s"%(str(chV[0].ch),str(chV[1])))
                    if not chV[0].checkValue(chV[1]):
                        error = "Do not match. %s should be %s. It is %s"%(chV[0].ch,str(chV[1]),str(chV[0].read()))
                        self.log (error,True)
                        raise ValueError(error)

        if checkBlinks:
            self.checkDigitalBlinks(digitalBlink)

        return True

    def checkDigitalBlinks(self,channelsValues,timeout=0.8):
            vals = []
            chs = []
            for chV in channelsValues:
                vals.append(int(chV[1]))
                chs.append(chV[0])
            results = self.readDigitalBlinks(chs,timeout)
            if vals == results:
                return  True
            else:
                string="Blinks do not match: "
                for n in range(len(vals)):
                    if vals[n] != results[n]:
                        string = string + ("%s is %s (should be %s);  "%(str(chs[n].ch),str(results[n]),str(vals[n])))
                self.log(string,True)
                raise ValueError(string)


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
            self.log(error,True)
            raise ValueError(error)




    def setDefault(self,gateway=True,check=True):
        self.log("Setting normal operation values.")

        for a in range(3):
            press_chs =[]

            for ch in self.tester.testBox.plc.channels:
                if str(ch.default_value) != "":
                    try:
                        ch.write(float(ch.default_value))
                    except ValueError:
                        self.log("Can't write to testBox.plc " + ch.ch,True)
                        raise ValueError("Can't write to " + ch.ch)

            if gateway:
                for ch in self.tester.plutoGateway.channels:
                    if str(ch.default_value) != "" and str(ch.default_value) != "P" and ch.ch.find("_w") >= 0:
                        try:
                            ch.write(int(ch.default_value))
                        except ValueError:
                            self.log("Can't write to plutoGateway " + ch.ch,True)
                            raise ValueError("Can't write to " + ch.ch)
                    elif str(ch.default_value) == "P":
                        press_chs.append(ch)

            self.sleep(0.2)

            for ch in press_chs:
                ch.write(1)
            self.sleep(0.3)

            for ch in press_chs:
                ch.write(0)

            if check:
                if self.checkDefault():
                    self.log("Normal operation values set.")
                    return True
            else:
                self.log("Normal operation values set.")
                return True



    def checkDuring(self,channelsValues, timeout):
        self.log("Wait for %s s with no changes."%str(timeout))

        start = time.time()
        while time.time() - start < timeout:
            for ch in (channelsValues):
                read = ch[0].read()
                if read != ch[1]:
                    error = "A channel not suposed to change changed its value. :: %s in %s, not %s."%(ch[0].ch,read, ch[1])
                    self.log(error,True)
                    raise ValueError(error)
            self.sleep(1)
            print(int(time.time() - start))

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
                self.log(error,True)
                raise ValueError(error)

        else:

            if compare is not None:
                channels = ''
                for chV in compare:
                    channels +="%s,"%chV[0].ch

                self.log ("Check if any other channel has changed.(%s)"%channels)
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
                    self.log(error,True)
                    raise ValueError(error)

            self.log("Channels changed as expected.")
            return True


    def writeChannels(self, chVs):

        for chV in chVs:
            try:
                self.log("Writing %s to %s"%(str(chV[1]),str(chV[0])))
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















