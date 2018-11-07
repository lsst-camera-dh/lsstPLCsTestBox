from os import path
from pydm import Display
from pydm.PyQt.QtCore import *
from pydm.PyQt.QtGui import *
import tester
import cold_tests
from mapping_parser import import_mappings
import logging
import time

class ColdTests(Display):
    def __init__(self, parent=None, args=None, macros=None):
        super(ColdTests, self).__init__(parent=parent, macros=macros)

        logging.basicConfig(filename='vaccumTests%s.log', level=logging.DEBUG)

        plutoGateway_mapping_path = path.join(path.dirname(path.realpath(__file__)), "mapping", "cold_modbus_mapping.csv")
        testbox_mapping_path = path.join(path.dirname(path.realpath(__file__)), "mapping", "PLC_Certification_Chassis.xlsx")

        testBox, plutoGateway = import_mappings(plutoGateway_mapping_path,testbox_mapping_path,'ColdCryo Cables')


        self.cold_tester = tester.Tester(testBox , plutoGateway)
        self.cold_tester.connectTestBox()
        self.cold_tester.connectGateway(timeout=30)



        self.cold_tester.tests.append(cold_tests.TestPlutoGatewayConfig(self.cold_tester, -1))
        self.cold_tester.tests.append(cold_tests.TestPlutoPLCsPresent(self.cold_tester, -1))


        self.cold_tester.tests.append(cold_tests.TestChannelsBootDefault(self.cold_tester, -1))

        self.cold_tester.tests.append(cold_tests.TestPlutoWriteReadback(self.cold_tester, -1))


        self.cold_tester.tests.append(cold_tests.TestDigitalInputs(self.cold_tester, -1))
        self.cold_tester.tests.append(cold_tests.TestSensorsValid(self.cold_tester, -1))
        self.cold_tester.tests.append(cold_tests.TestImmediateTrips(self.cold_tester, -1))
        self.cold_tester.tests.append(cold_tests.TestImmediatePowerTrips(self.cold_tester, -1))

        self.cold_tester.tests.append(cold_tests.TestDelay0(self.cold_tester, -1))
        self.cold_tester.tests.append(cold_tests.TestDelay1(self.cold_tester, -1))
        self.cold_tester.tests.append(cold_tests.TestDelay2(self.cold_tester, -1))
        self.cold_tester.tests.append(cold_tests.TestDelay3(self.cold_tester, -1))

        for i, test in enumerate( self.cold_tester.tests):
            test.id=i


        self.table = self.ui.tableWidget

        headers= ["Test","Description","","Step","Details"]

        self.table.setRowCount(len(self.cold_tester.tests))
        self.table.setColumnCount(len(headers))

        self.table.setHorizontalHeaderLabels(headers)
        self.table.setVerticalHeaderLabels([str(e)  for e in list(range(1,len(self.cold_tester.tests)+1))])

        for i, test in enumerate(self.cold_tester.tests):
            self.update_table_line(i)
        self.table.setCurrentCell(0, 0 ,QItemSelectionModel.Rows)

        self.table.itemChanged.connect(self.item_changed)

        self.table.setColumnWidth(0, 160)
        self.table.setColumnWidth(1, 300)
        self.table.setColumnWidth(2, 50)
        self.table.setColumnWidth(3, 250)

        self.cold_tester.test_line_update.connect(self.update_table_line)
        self.cold_tester.monitor_update.connect(self.update_monitor_menu)

        self.ui.runAllButton.clicked.connect(self.cold_tester.run_all)
        self.ui.abortButton.clicked.connect(self.cold_tester.abort)

    def item_changed(self,item):
        id = self.table.row(item)
        self.cold_tester.tests[id].selected = item.checkState()

    def update_table_line(self,i):

        test = self.cold_tester.tests[i]
        name = QTableWidgetItem(test.name)


        self.table.setItem(i, 0, name)

        self.table.setItem(i, 1, QTableWidgetItem(test.desc))

        run = QPushButton("RUN")
        test.set_run_button(run)


        color = " rgb(230, 230, 230)"

        if test.result == "":
            color = " rgb(230, 230, 230)"
        elif test.result == "OK":
            color = " #06b025"
        elif test.result =="error" or test.result == "Aborted" :
            color = "yellow"
        elif test.result == "FAILED":
            color = " red"

        if test.running == 1:
            color = " blue"

        style='''QPushButton
        {
            background-color:  '''+color+''';    color: black;      border: none;     border-radius: 5px;    text-align: center; margin: 3px;    padding: 80px 6px;}

                QPushButton::hover
        {
            background-color: black;
        color: white;
        }'''

        run.setStyleSheet(style)

        self.table.setCellWidget(i, 2, run)
        self.table.setItem(i, 3, QTableWidgetItem(test.step_m))
        self.table.setItem(i, 4, QTableWidgetItem(test.details))

        self.table.setCurrentCell(i,0,QItemSelectionModel.Rows)

    def update_monitor_menu(self,current_test,current_test_message,progress_bar,progress_count,result_bar_color,result_bar_message):

        self.ui.progressBar.setValue(progress_bar*100)

        bar = self.ui.progressBar
        p = bar.palette()
        p.setColor(QPalette.Highlight, Qt.red);

        self.ui.progressCount.setText(progress_count)
        self.ui.currentTest.setText(current_test)
        self.ui.currentTestMessage.setText(current_test_message)


        self.ui.resultMessage.setText(result_bar_message)
        if result_bar_message == "Finished.":
            self.ui.resultMessage.setStyleSheet("background-color: #06b025;")

        elif result_bar_message == "Aborted.":
            self.ui.resultMessage.setStyleSheet("background-color: yellow;")

        elif result_bar_message == "Running...":
            self.ui.resultMessage.setStyleSheet("background-color: blue;")

        elif result_bar_message == "Failed.":
            self.ui.resultMessage.setStyleSheet("background-color: red;")

        else:
            self.ui.resultMessage.setStyleSheet("background-color:rgb(230, 230, 230);")

    def ui_filename(self):
        return 'testMenu.ui'

    def ui_filepath(self):
        return path.join(path.dirname(path.realpath(__file__)),"ui", self.ui_filename())

