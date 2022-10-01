from calendar import c
import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QWidget, QCheckBox, QApplication, QLabel, QPushButton, QFileDialog, QComboBox,  QTableWidget, QTableWidgetItem, QVBoxLayout
from PyQt5.uic import loadUi
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QLineEdit
import openpyxl
import pandas as pd
from xml.etree.ElementTree import tostring
import xlsxwriter
from solver import buildDp, solve, uniqueGroups, mem, toPrint
from college import *
from display import *
from groups_input import *
from pycode import (
    Monitor,
    Day,
    Task,
    process,
    read_input,
    arabic,
    observer,
    khalafawy,
    road_el_farag,
    professor,
    Adoctor,
    doctor,
    manager,
    monitor0,
    monitors,
    days,
    observser_data_lst,
)

branch_num = -1
option_num = -1

# 1


def get_options(branch_num):
    for i in range(num_of_branches):
        branch.append(Branch(branch_name[i], i, num_of_builds[i]))

    get_and_store_groups()
    print(branch_num)
    DISPLAY(branch_num, num_of_branches)


def get_tables(branch_num, option_num):
    print(option_num)
    options(branch_num, option_num)

    def printCollege(branch: Branch) -> None:
        for hall in branch.hallsInBranch:
            print(f"{hall.name} {hall.volume}")
        print()
        for g in branch.groupsInBranch:
            print(f"{group[g].name} {group[g].volume}")


class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi("screen1.ui", self)

        self.inv = self.findChild(QPushButton, "inv")
        self.exam = self.findChild(QPushButton, "exam")

        self.inv.clicked.connect(self.invScreen)
        self.exam.clicked.connect(self.exScreen)

    def invScreen(self):
        widget.setCurrentWidget(invscreen1)

    def exScreen(self):
        widget.setCurrentWidget(exscreen1)

###############################################################################################################


class invScreen1(QWidget):
    def __init__(self):
        super(invScreen1, self).__init__()
        loadUi("screenInv1.ui", self)
        self.browse = self.findChild(QPushButton, "browse")
        self.generate = self.findChild(QPushButton, "generate")
        self.back = self.findChild(QPushButton, "back")
        self.label = self.findChild(QLabel, "lineEdit")
        self.help = self.findChild(QPushButton, "help")
        self.help.clicked.connect(self.help_func)

        self.browse.clicked.connect(self.browsefiles)
        self.generate.clicked.connect(self.generateTables)
        self.back.clicked.connect(self.goBack)

        self.txt = ""
        self.file_name = ""

    def browsefiles(self):
        fname = QFileDialog.getOpenFileName(
            self, 'Open file', '', 'Excel (*.csv *xls *xlsx )')
        self.lineEdit.setText(fname[0])
        self.txt = fname
        self.file_name = fname[0]

    def help_func(self):
        widget.setCurrentWidget(helpinv)

    def goBack(self):
        widget.setCurrentWidget(mainwindow)

    def generateTables(self):

        if (self.txt != ""):
            read_input(self.file_name)
            ok = process(monitors, days)
            cnt = 1
            if not ok:
                self.label_not_enough = self.findChild(
                    QLabel, "label_not_enough")
                self.label_not_enough.setText("عدد الموظفين غير كافي")

            else:
                for mon in monitors:
                    mon.push_info(observser_data_lst, cnt)
                    # mon.print_info()
                    cnt = cnt + 1
                dataframeout = pd.DataFrame(observser_data_lst)
                dataframeout.to_excel("observer_output.xlsx")
                s2 = invScreen2()
                widget.addWidget(s2)
                widget.setCurrentWidget(s2)


# 3
class invScreen2(QWidget):
    def __init__(self):
        super(invScreen2, self).__init__()
        loadUi("screenInv2.ui", self)
        self.combox = self.findChild(QComboBox, "comboBox1")

        self.list = ["...اختار"]
        for mon in monitors:
            self.list.append(mon.user_name)

        self.combox.addItems(self.list)

        self.select = self.findChild(QPushButton, "select")
        self.select.clicked.connect(self.valueOfCombo)

        self.label_name = self.findChild(QLabel, "label_4")
        self.label_dep = self.findChild(QLabel, "label_6")

        self.table_widget = self.findChild(QTableWidget, "tableWidget")

        self.lineEdit = self.findChild(QLineEdit, "lineEdit")
        #self.search_value = self.lineEdit.text()
        self.searchButton = self.findChild(QPushButton, "searchButton")
        self.searchButton.clicked.connect(self.search_fun)

    def search_fun(self):

        if self.lineEdit.text() in self.list:

            self.index = self.list.index(self.lineEdit.text())-1
            self.load_data_search()

        else:
            self.lineEdit.setText("غير موجود")

        # clear combo
        self.combox.setCurrentIndex(0)

    def browsefiles(self):
        QFileDialog.getOpenFileName(
            self, 'Open file', '', 'Excel (*.csv *xls *xlsx )')

    def valueOfCombo(self):
        # clear table rows
        for i in range(self.table_widget.rowCount()):
            self.table_widget.removeRow(self.table_widget.rowCount()-1)
        # clear labels
        self.label_name.setText("")
        self.label_dep.setText("")
        # clear search input
        self.lineEdit.setText("")
        # print(self.combox.currentIndex())
        if (self.combox.currentIndex()):

            self.load_data()   # add combobox value

    def load_data(self):
        mon = monitors[self.combox.currentIndex()-1]
        self.label_name.setText(mon.user_name)
        self.label_dep.setText(mon.title)
        for ts in mon.task:

            row = self.table_widget.rowCount()
            self.table_widget.setRowCount(row+1)

            self.table_widget.setItem(row, 0, QTableWidgetItem(str(ts.day)))
            self.table_widget.setItem(row, 1, QTableWidgetItem(str(ts.type)))
            self.table_widget.setItem(
                row, 2, QTableWidgetItem(str(ts.building)))

    def load_data_search(self):
        # clear table rows
        for i in range(self.table_widget.rowCount()):
            self.table_widget.removeRow(self.table_widget.rowCount() - 1)
        # clear labels
        self.label_name.setText("")
        self.label_dep.setText("")
        mon = monitors[self.index]
        self.label_name.setText(mon.user_name)
        self.label_dep.setText(mon.title)
        for ts in mon.task:

            row = self.table_widget.rowCount()
            self.table_widget.setRowCount(row+1)

            self.table_widget.setItem(row, 0, QTableWidgetItem(str(ts.day)))
            self.table_widget.setItem(row, 1, QTableWidgetItem(str(ts.type)))
            self.table_widget.setItem(
                row, 2, QTableWidgetItem(str(ts.building)))


###############################################################################################################

class exScreen1(QWidget):
    def __init__(self):
        super(exScreen1, self).__init__()
        loadUi("screenEx1.ui", self)
        self.browse = self.findChild(QPushButton, "browse")
        self.generate = self.findChild(QPushButton, "generate")
        self.back = self.findChild(QPushButton, "back")
        self.label = self.findChild(QLabel, "lineEdit")
        self.help = self.findChild(QPushButton, "help")
        self.help.clicked.connect(self.help_func)

        self.khalafawy = self.findChild(QCheckBox, "checkBox")
        self.rod = self.findChild(QCheckBox, "checkBox_2")

        self.browse.clicked.connect(self.browsefiles)
        self.generate.clicked.connect(self.generateTables)
        self.back.clicked.connect(self.goBack)

        self.txt = ""

    def help_func(self):
        widget.setCurrentWidget(helpexam)

    def browsefiles(self):
        fname = QFileDialog.getOpenFileName(
            self, 'Open file', '', 'Excel (*.csv *xlsx)')
        self.lineEdit.setText(fname[0])
        self.txt = fname[0]
        global num_of_branches
        excelSheet, num_of_branches, allBranches = read_inputt(self.txt)
        read_sheet(excelSheet, num_of_branches)

    def goBack(self):
        widget.setCurrentWidget(mainwindow)

    def generateTables(self):

        if (self.txt != ""):
            if (self.khalafawy.isChecked() == True and self.rod.isChecked() == False):
                global branch_num
                branch_num = 1
                get_options(branch_num)
                global s1
                s1 = exScreen2()
                widget.addWidget(s1)
                widget.setCurrentWidget(s1)
            elif (self.rod.isChecked() == True and self.khalafawy.isChecked() == False):
                branch_num = 2
                get_options(branch_num)
                s1 = exScreen2()
                widget.addWidget(s1)
                widget.setCurrentWidget(s1)

# 5


class exScreen2(QWidget):

    def __init__(self):
        super(exScreen2, self).__init__()
        loadUi("screenEx2.ui", self)

        self.save = self.findChild(QPushButton, "save")
        self.save.clicked.connect(self.save_func)

        self.tableWidgetexam = self.findChild(QTableWidget, "tableWidget")
        self.comboxfl = self.findChild(QComboBox, "comboBoxx1_2")
        self.comboxfl.clear()
        self.comboxfl.addItem('choose')
        cnt = 1
        for group in uniqueGroups:
            self.comboxfl.addItem(f"{cnt}")
            # print(f"{cnt}.")
            cnt += 1

        self.comboxfl.currentTextChanged.connect(self.change_table)

        self.label = self.findChild(QLabel, "label1")

    def change_table(self, s):
        global option_num
        if (s != "choose"):
            option_num = int(s)
            row1 = 0
            row2 = 0
            row3 = 0
            row11 = 0
            row22 = 0
            row33 = 0
            print("Text changed:", s)

            get_tables(branch_num, option_num)

            print(len(to_print1))
            self.tableWidgetexam.setRowCount(len(to_print1))
            for res in to_print3:
                self.tableWidgetexam.setItem(
                    row1, 0, QtWidgets.QTableWidgetItem(str(res[3])))
                self.tableWidgetexam.setItem(
                    row1, 1, QtWidgets.QTableWidgetItem(str(res[2])))
                self.tableWidgetexam.setItem(
                    row1, 2, QtWidgets.QTableWidgetItem(str(res[1])))
                row1 += 1

            for res in to_print2:
                self.tableWidgetexam.setItem(
                    row2, 3, QtWidgets.QTableWidgetItem(str(res[3])))
                self.tableWidgetexam.setItem(
                    row2, 4, QtWidgets.QTableWidgetItem(str(res[2])))
                self.tableWidgetexam.setItem(
                    row2, 5, QtWidgets.QTableWidgetItem(str(res[1])))
                row2 += 1

            for res in to_print1:
                self.tableWidgetexam.setItem(
                    row3, 6, QtWidgets.QTableWidgetItem(str(res[3])))
                self.tableWidgetexam.setItem(
                    row3, 7, QtWidgets.QTableWidgetItem(str(res[2])))
                self.tableWidgetexam.setItem(
                    row3, 8, QtWidgets.QTableWidgetItem(str(res[1])))
                row3 += 1

            for res in to_print3:
                self.tableWidgetexam.setItem(
                    row11, 9, QtWidgets.QTableWidgetItem(str(res[0])))
                self.tableWidgetexam.setItem(
                    row11, 9, QtWidgets.QTableWidgetItem(str(res[0])))
                self.tableWidgetexam.setItem(
                    row11, 9, QtWidgets.QTableWidgetItem(str(res[0])))
                row11 += 1

            for res in to_print2:
                self.tableWidgetexam.setItem(
                    row22, 9, QtWidgets.QTableWidgetItem(str(res[0])))
                self.tableWidgetexam.setItem(
                    row22, 9, QtWidgets.QTableWidgetItem(str(res[0])))
                self.tableWidgetexam.setItem(
                    row22, 9, QtWidgets.QTableWidgetItem(str(res[0])))
                row22 += 1

            for res in to_print1:
                self.tableWidgetexam.setItem(
                    row33, 9, QtWidgets.QTableWidgetItem(str(res[0])))
                self.tableWidgetexam.setItem(
                    row33, 9, QtWidgets.QTableWidgetItem(str(res[0])))
                self.tableWidgetexam.setItem(
                    row33, 9, QtWidgets.QTableWidgetItem(str(res[0])))
                row33 += 1
            to_print1.clear()
            to_print2.clear()
            to_print3.clear()

            # for i in range(5):
        #    print(to_print1[i], to_print2[i], to_print3[i])

    def browsefiles(self):
        QFileDialog.getOpenFileName(
            self, 'Open file', '', 'Excel (*.csv *xls)')

    def save_func(self):
        output_the_distribution(branch_num, option_num)

    def backfromex_fun(self):
        widget.removeWidget(s1)
        exscreen1 = exScreen1()
        widget.addWidget(exscreen1)
        widget.setCurrentWidget(exscreen1)


class invHelp(QWidget):
    def __init__(self):
        super(invHelp, self).__init__()
        loadUi("helpInv.ui", self)
        self.save = self.findChild(QPushButton, "back")
        self.save.clicked.connect(self.back_func)

    def back_func(self):
        widget.setCurrentWidget(invscreen1)


class examHelp(QWidget):
    def __init__(self):
        super(examHelp, self).__init__()
        loadUi("helpEx.ui", self)
        self.save = self.findChild(QPushButton, "back")
        self.save.clicked.connect(self.back_func)

    def back_func(self):
        widget.setCurrentWidget(exscreen1)


app = QApplication(sys.argv)
widget = QtWidgets.QStackedWidget()
mainwindow = MainWindow()
exscreen1 = exScreen1()
invscreen1 = invScreen1()
helpinv = invHelp()
helpexam = examHelp()

widget.addWidget(mainwindow)
widget.addWidget(exscreen1)
widget.addWidget(invscreen1)
widget.addWidget(helpinv)
widget.addWidget(helpexam)


widget.show()
sys.exit(app.exec_())
