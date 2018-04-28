from pydm.PyQt.QtCore import *
import time

class Tester(QThread):

    test_line_update = pyqtSignal(int)
    monitor_update = pyqtSignal(str,str,float,str,int,str)

    def __init__(self):
        QObject.__init__(self)
        QThread.__init__(self)

        self.tests = []

        self.current_test = ""
        self.current_test_message = ""
        self.progress_bar = 0
        self.progress_count = ""
        self.result_bar_color = 0
        self.result_bar_message = ""

        self.abortion = False

        self.plutoGateway = None
        self.testBox = None

        self.running_tests = []

        # real init


      #  for a in range(300):
      #      self.tests.append(Test(name="a "+str(a),id = a,tester = self))

        import vac_tests
        import inspect

        clsmembers = inspect.getmembers(vac_tests, inspect.isclass)

        i=0
        for  c in (clsmembers):
            if c[0].find("test")==0:
                print (c)
                test = c[1](self,i)
                self.tests.append(test)
                i+=1

        self.tests[1].button_run()
        while self.isRunning():
            time.sleep(1)
        self.tests[2].button_run()


    def run_all(self):
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
        for test in self.tests:
            test.abort()

    def clean_display(self):
        for test in self.tests:
            test.result = ""
            test.details = ""
            self.update_test_line(test.id)

    def update_test_line(self,id):
        self.test_line_update.emit(id)

    def update_menu(self):
        self.monitor_update.emit(self.current_test,self.current_test_message,self.progress_bar,self.progress_count,self.result_bar_color,self.result_bar_message)


    def run(self):
        self.n_tests = len(self.running_tests)

        self.progress_bar = 0
        self.progress_count = "0 / " + str(self.n_tests)
        self.current_test = ""
        self.current_test_message = ""
        self.result_bar_message = "Running..."
        self.update_menu()

        self.abortion = False

        for n, test in enumerate(self.running_tests):
            test.run()
            self.progress_bar = (n + 1) / float(self.n_tests)
            self.progress_count = str(n + 1) + " / " + str(self.n_tests)

            self.update_menu()

            if self.abortion:
                self.progress_bar = 0.0
                self.progress_count = ""
                self.current_test = ""
                self.current_test_message = ""
                self.result_bar_message = "Aborted."
                self.update_menu()

                return

        self.current_test = ""
        self.current_test_message = ""
        self.result_bar_message = "Finished."
        self.update_menu()


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

    def test(self):
        raise ValueError("test() not implemented.")

    def abort(self):
        self.abortion = True

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

    def set_run_button(self,button):
        self.run_button = button
        self.run_button.clicked.connect(self.button_run)

    def button_run(self):
        if not self.tester.isRunning():
            self.tester.running_tests = [self]
            self.tester.start()




