from os import path
from pydm import Display
from pydm.PyQt.QtCore import *
from pydm.PyQt.QtGui import *
import tester
import mpm_tests
from mapping_parser import import_mappings
import logging
import time

class MpmTests(Display):
    def __init__(self, parent=None, args=None, macros=None):
        super(MpmTests, self).__init__(parent=parent, macros=macros)

        logging.basicConfig(filename='vacuumTests%s.log', level=logging.DEBUG)

        plutoGateway_mapping_path = path.join(path.dirname(path.realpath(__file__)), "mapping", "mpm_modbus_mapping.csv")
        testbox_mapping_path = path.join(path.dirname(path.realpath(__file__)), "mapping", "PLC_Certification_Chassis.xlsx")

        testBox, plutoGateway = import_mappings(plutoGateway_mapping_path,testbox_mapping_path,'MPM Cables')

        print('ola')



        self.mpm_tester = tester.Tester(testBox , plutoGateway)
        #self.mpm_tester.connectTestBox()
        #self.mpm_tester.connectGateway(timeout=30)


        self.mpm_tester.tests.append(mpm_tests.TestPlutoGatewayConfig(self.mpm_tester, -1))
        self.mpm_tester.tests.append(mpm_tests.TestPlutoPLCsPresent(self.mpm_tester, -1))


        self.mpm_tester.tests.append(mpm_tests.TestChannelsBootDefault(self.mpm_tester, -1))

        self.mpm_tester.tests.append(mpm_tests.TestPlutoWriteReadback(self.mpm_tester, -1))

        self.mpm_tester.tests.append(mpm_tests.TestTemperatureSetpoints(self.mpm_tester, -1))
        self.mpm_tester.tests.append(mpm_tests.TestPermitsBlock(self.mpm_tester, -1))
        self.mpm_tester.tests.append(mpm_tests.TestAcPermitCoolantValve(self.mpm_tester, -1))

        self.mpm_tester.tests.append(mpm_tests.TestVacuumToRefPermits(self.mpm_tester, -1))
        self.mpm_tester.tests.append(mpm_tests.TestColdCryoPermits(self.mpm_tester, -1))

        for i, test in enumerate( self.mpm_tester.tests):
            test.id=i


        self.table = self.ui.tableWidget

        headers= ["Test","Description","","Step","Details"]

        self.table.setRowCount(len(self.mpm_tester.tests))
        self.table.setColumnCount(len(headers))

        self.table.setHorizontalHeaderLabels(headers)
        self.table.setVerticalHeaderLabels([str(e)  for e in list(range(1,len(self.mpm_tester.tests)+1))])

        for i, test in enumerate(self.mpm_tester.tests):
            self.update_table_line(i)
        self.table.setCurrentCell(0, 0 ,QItemSelectionModel.Rows)

        self.table.itemChanged.connect(self.item_changed)

        self.table.setColumnWidth(0, 160)
        self.table.setColumnWidth(1, 300)
        self.table.setColumnWidth(2, 50)
        self.table.setColumnWidth(3, 250)

        self.mpm_tester.test_line_update.connect(self.update_table_line)
        self.mpm_tester.monitor_update.connect(self.update_monitor_menu)

        self.ui.runAllButton.clicked.connect(self.mpm_tester.run_all)
        self.ui.abortButton.clicked.connect(self.mpm_tester.abort)

    def item_changed(self,item):
        id = self.table.row(item)
        self.mpm_tester.tests[id].selected = item.checkState()

    def update_table_line(self,i):

        test = self.mpm_tester.tests[i]
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

