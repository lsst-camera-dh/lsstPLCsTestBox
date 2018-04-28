from os import path
from pydm import Display
from pydm.PyQt.QtCore import *
from pydm.PyQt.QtGui import *

from tester import Tester


maq20_ip = "192.168.1.101"
maq20_port = 502

class VaccumTests(Display):
    def __init__(self, parent=None, args=None, macros=None):
        super(VaccumTests, self).__init__(parent=parent, macros=macros)

        self.vac_tester = Tester()

   #    print(dir(self.vac_tester))




        self.table = self.ui.tableWidget

        headers= ["Test","Description","Run","Result","Details"]

        self.table.setRowCount(len(self.vac_tester.tests))
        self.table.setColumnCount(len(headers))

        self.table.setHorizontalHeaderLabels(headers)
        self.table.setVerticalHeaderLabels([str(e)  for e in list(range(1,len(self.vac_tester.tests)+1))])

        for i, test in enumerate(self.vac_tester.tests):
            self.update_table_line(i)
        self.table.setCurrentCell(0, 0 ,QItemSelectionModel.Rows)

        self.table.itemChanged.connect(self.item_changed)

        self.vac_tester.test_line_update.connect(self.update_table_line)
        self.vac_tester.monitor_update.connect(self.update_monitor_menu)

        self.ui.runAllButton.clicked.connect(self.vac_tester.run_all)
        self.ui.runSelectedButton.clicked.connect(self.vac_tester.run_selected)
        self.ui.abortButton.clicked.connect(self.vac_tester.abort)



   # def resizeEvent(self, event):
   #     print("resize")

    #    original =  self.ui.tableWidget.width()
    #    self.ui.tableWidget.setColumnWidth(0,original/5)

        #self.QMainWindow.resizeEvent(self, event)




    def item_changed(self,item):
        id = self.table.row(item)
        self.vac_tester.tests[id].selected = item.checkState()


    def update_table_line(self,i):

        test = self.vac_tester.tests[i]

        name = QTableWidgetItem(test.name)

    #    print(test.selected)

        if test.selected:
            name.setCheckState(Qt.Checked)
        else:
            name.setCheckState(Qt.Unchecked)

        self.table.setItem(i, 0, name)

        self.table.setItem(i, 1, QTableWidgetItem(test.desc))

        run = QPushButton("RUN")
        test.set_run_button(run)

        self.table.setCellWidget(i, 2, run)
        self.table.setItem(i, 3, QTableWidgetItem(test.result))
        self.table.setItem(i, 4, QTableWidgetItem(test.details))

        self.table.setCurrentCell(i,0,QItemSelectionModel.Rows)

    def update_monitor_menu(self,current_test,current_test_message,progress_bar,progress_count,result_bar_color,result_bar_message):

        self.ui.progressBar.setValue(progress_bar*100)
        self.ui.progressCount.setText(progress_count)
        self.ui.currentTest.setText(current_test)
        self.ui.currentTestMessage.setText(current_test_message)
        self.ui.resultMessage.setText(result_bar_message)







    def ui_filename(self):
        return 'vaccumTestMenu.ui'

    def ui_filepath(self):
        return path.join(path.dirname(path.realpath(__file__)),"ui", self.ui_filename())


class Mymodel (QAbstractTableModel):

    def rowCount(self):
        return 10

    def columnCount(self):
        return 10



'''

        tableView = self.ui.columnView

        list2 = tableView

        model = QStandardItemModel(list)

        item = QStandardItem()

        foods = [
            'Cookie dough',  # Must be store-bought
            'Hummus',  # Must be homemade
            'Spaghetti',  # Must be saucy
            'Dal makhani',  # Must be spicy
            'Chocolate whipped cream'  # Must be plentiful
        ]

        for food in foods:
            # Create an item with a caption
            item = QStandardItem(food)

            # Add a checkbox to it
            item.setCheckable(True)

            # Add the item to the model
            model.appendRow(item)

        list.setModel(model)



        def on_item_changed(item):

            print("CANGEH")

            # If the changed item is not checked, don't bother checking others
            if not item.checkState():
                return

            # Loop through the items until you get None, which
            # means you've passed the end of the list
            i = 0
            while model.item(i):
                if not model.item(i).checkState():
                    return
                i += 1

        model.itemChanged.connect(on_item_changed)
'''