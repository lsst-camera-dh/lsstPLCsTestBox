from os import path
from pydm import Display
from pydm.PyQt.QtCore import *
from pydm.PyQt.QtGui import *
import tester
import vac_tests2 as vac_tests
from mapping_parser import import_mappings
import logging

class VaccumTests(Display):
    def __init__(self, parent=None, args=None, macros=None):
        super(VaccumTests, self).__init__(parent=parent, macros=macros)

        #logging.basicConfig(filename=path.join(path.dirname(path.realpath(__file__)), "logs",'vaccumTests.log'), level=logging.DEBUG)
        logging.basicConfig(filename='C:\\Users\\joaoprod\\Documents\\GitHub\\lsstPLCsTestBox\\logs\\vaccumTests2.log',
                            level=logging.DEBUG)
        logging.debug('This message should go to the log file')
        logging.info('So should this')
        logging.warning('And this, too')
        print(path.join(path.dirname(path.realpath(__file__)), "logs",'vaccumTests.log'))

        plutoGateway_mapping_path = path.join(path.dirname(path.realpath(__file__)), "mapping", "vac_modbus_mapping.csv")
        testbox_mapping_path = path.join(path.dirname(path.realpath(__file__)), "mapping", "PLC_Certification_Chassis.xlsx")

        testbox , plutoGateway = import_mappings(plutoGateway_mapping_path,testbox_mapping_path,'Vaccum cables')

        self.vac_tester = tester.Tester(testbox , plutoGateway)


        self.vac_tester.tests.append(vac_tests.TestPlutoGatewayConfig(self.vac_tester, -1))
        self.vac_tester.tests.append(vac_tests.TestPlutoPLCsPresent(self.vac_tester, -1))

        self.vac_tester.tests.append(vac_tests.TestChannelsBootDefault(self.vac_tester, -1))

        self.vac_tester.tests.append(vac_tests.TestPlutoWriteReadback(self.vac_tester, -1))

        #self.vac_tester.tests.append(vac_tests.TestAnalogScaling(self.vac_tester, -1))

        #self.vac_tester.tests.append(vac_tests.TestHvCvDifferences(self.vac_tester, -1))

        self.vac_tester.tests.append(vac_tests.TestCvValves(self.vac_tester, -1))
        self.vac_tester.tests.append(vac_tests.TestValveMonitors(self.vac_tester, -1))

        self.vac_tester.tests.append(vac_tests.TestHvStat(self.vac_tester, -1))
        #self.vac_tester.tests.append(vac_tests.TestHvTurboOnOfflogic(self.vac_tester, -1))
        self.vac_tester.tests.append(vac_tests.TestHvTurboPermitBlock(self.vac_tester, -1))
        self.vac_tester.tests.append(vac_tests.TestHvTurboPermitAuto(self.vac_tester, -1))

        self.vac_tester.tests.append(vac_tests.TestCvStat(self.vac_tester, -1))
        #self.vac_tester.tests.append(vac_tests.TestCvTurboOnOfflogic(self.vac_tester, -1))
        self.vac_tester.tests.append(vac_tests.TestCvTurboPermitBlock(self.vac_tester, -1))
        self.vac_tester.tests.append(vac_tests.TestCvTurboPermitAuto(self.vac_tester, -1))


        for i, test in enumerate( self.vac_tester.tests):
            test.id=i



        self.table = self.ui.tableWidget

        headers= ["Test","Description","","Step","Details"]

        self.table.setRowCount(len(self.vac_tester.tests))
        self.table.setColumnCount(len(headers))

        self.table.setHorizontalHeaderLabels(headers)
        self.table.setVerticalHeaderLabels([str(e)  for e in list(range(1,len(self.vac_tester.tests)+1))])

        for i, test in enumerate(self.vac_tester.tests):
            self.update_table_line(i)
        self.table.setCurrentCell(0, 0 ,QItemSelectionModel.Rows)

        self.table.itemChanged.connect(self.item_changed)

        self.table.setColumnWidth(0, 160)
        self.table.setColumnWidth(1, 300)
        self.table.setColumnWidth(2, 50)
        self.table.setColumnWidth(3, 250)

        self.vac_tester.test_line_update.connect(self.update_table_line)
        self.vac_tester.monitor_update.connect(self.update_monitor_menu)

        self.ui.runAllButton.clicked.connect(self.vac_tester.run_all)
        self.ui.abortButton.clicked.connect(self.vac_tester.abort)


    def item_changed(self,item):
        id = self.table.row(item)
        self.vac_tester.tests[id].selected = item.checkState()


    def update_table_line(self,i):


        test = self.vac_tester.tests[i]

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

