import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QPushButton, QFileDialog, QComboBox,  QTableWidget, QTableWidgetItem, QVBoxLayout
from PyQt5.uic import loadUi
import openpyxl

# 1
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


# 2
class invScreen1(QWidget):
    def __init__(self):
        super(invScreen1, self).__init__()
        loadUi("screenInv1.ui", self)
        self.browse = self.findChild(QPushButton, "browse")
        self.generate = self.findChild(QPushButton, "generate")
        self.back = self.findChild(QPushButton, "back")
        self.label = self.findChild(QLabel, "lineEdit")

        self.browse.clicked.connect(self.browsefiles)
        self.generate.clicked.connect(self.generateTables)
        self.back.clicked.connect(self.goBack)

        self.txt = ""

    def browsefiles(self):
        fname = QFileDialog.getOpenFileName(
            self, 'Open file', '', 'Excel (*.csv *xls)')
        self.lineEdit.setText(fname[0])
        self.txt = fname

    def goBack(self):
        widget.setCurrentWidget(mainwindow)

    def generateTables(self):
        if (self.txt != ""):
            s2 = invScreen2()
            widget.addWidget(s2)
            widget.setCurrentWidget(s2)


# 3
class invScreen2(QWidget):
    def __init__(self):
        super(invScreen2, self).__init__()
        loadUi("screenInv2.ui", self)
        self.back = self.findChild(QPushButton, "back")
        self.back.clicked.connect(self.backfrominv_fun)

        self.browse = self.findChild(QPushButton, "browse")
        self.browse.clicked.connect(self.browsefiles)

        self.combox = self.findChild(QComboBox, "comboBox1")
        self.list = ["اختار...", "اسراء", "نورهان", "ياسمين"]
        self.combox.addItems(self.list)
        self.select = self.findChild(QPushButton, "select")
        self.select.clicked.connect(self.valueOfCombo)

        self.label_name = self.findChild(QLabel, "label_4")
        self.label_dep = self.findChild(QLabel, "label_6")

        self.table_widget = self.findChild(QTableWidget, "tableWidget")
        # self.load_data(self.combox.currentText())

        # table size
    def browsefiles(self):
        QFileDialog.getOpenFileName(
            self, 'Open file', '', 'Excel (*.csv *xls)')

    def valueOfCombo(self):
        # print(self.combox.currentIndex())
        if (self.combox.currentIndex()):
            self.load_data()   # add combobox value

    def load_data(self):
        # test
        self.label_name.setText("اسراء سعيد")
        self.label_dep.setText("ارشيف")

    def backfrominv_fun(self):
        widget.setCurrentWidget(invscreen1)


# 4
class exScreen1(QWidget):
    def __init__(self):
        super(exScreen1, self).__init__()
        loadUi("screenEx1.ui", self)
        self.browse = self.findChild(QPushButton, "browse")
        self.generate = self.findChild(QPushButton, "generate")
        self.back = self.findChild(QPushButton, "back")
        self.label = self.findChild(QLabel, "lineEdit")

        self.browse.clicked.connect(self.browsefiles)
        self.generate.clicked.connect(self.generateTables)
        self.back.clicked.connect(self.goBack)

        self.txt = ""

    def browsefiles(self):
        fname = QFileDialog.getOpenFileName(
            self, 'Open file', '', 'Excel (*.csv *xls)')
        self.lineEdit.setText(fname[0])
        self.txt = fname

    def goBack(self):
        widget.setCurrentWidget(mainwindow)

    def generateTables(self):
        if (self.txt != ""):
            s1 = exScreen2()
            widget.addWidget(s1)
            widget.setCurrentWidget(s1)


# 5
class exScreen2(QWidget):

    def __init__(self):
        super(exScreen2, self).__init__()
        loadUi("screenEx2.ui", self)

        self.back = self.findChild(QPushButton, "back")
        self.back.clicked.connect(self.backfromex_fun)

        self.browse = self.findChild(QPushButton, "browse")
        self.browse.clicked.connect(self.browsefiles)
        #self.comboxlo = self.findChild(QComboBox, "comboBoxx1")
        #self.list1 = ["Rod Al-farag", "Khalfawy"]
        # self.comboxlo.addItems(self.list1)

        #self.comboxbu = self.findChild(QComboBox, "comboBoxx2")
        #self.list2 = ["Main builing", "Sub builing", ]
        # self.comboxbu.addItems(self.list2)

        self.comboxfl = self.findChild(QComboBox, "comboBoxx1_2")
        self.list3 = ["First floor", "Second floor", "third floor"]
        self.comboxfl.addItems(self.list3)

        # self.select1 = self.findChild(QPushButton, "select11")
        # self.select1.clicked.connect(self.valueOfCombo)

        # self.select2 = self.findChild(QPushButton, "select22")
        # self.select2.clicked.connect(self.valueOfCombo)

        # self.select3 = self.findChild(QPushButton, "select11_2")
        # self.select3.clicked.connect(self.valueOfCombo)

        self.table_widget = self.findChild(QTableWidget, "tableWidgetexam")

        self.label = self.findChild(QLabel, "label1")

    def browsefiles(self):
        QFileDialog.getOpenFileName(
            self, 'Open file', '', 'Excel (*.csv *xls)')

    def backfromex_fun(self):
        widget.setCurrentWidget(exscreen1)


app = QApplication(sys.argv)
widget = QtWidgets.QStackedWidget()
mainwindow = MainWindow()
exscreen1 = exScreen1()
invscreen1 = invScreen1()
widget.addWidget(mainwindow)
widget.addWidget(exscreen1)
widget.addWidget(invscreen1)
widget.setFixedWidth(780)
widget.setFixedHeight(690)
widget.show()
sys.exit(app.exec_())
