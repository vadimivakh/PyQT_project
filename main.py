# -*- coding: utf-8 -*-

import datetime
import os
import requests
import sys
from PyQt4 import QtCore  # import graphics module core for project
from PyQt4 import QtGui  # import graphics module ui for project

# This part will recreate window design from window.ui to main_window.py
# Make sure that pyuic4.bat file exist
os.popen(r'C:\Python34\Lib\site-packages\PyQt4\pyuic window.ui>>main_window.py')
from main_window import Ui_MainWindow

_fromUtf8 = QtCore.QString.fromUtf8

class Main(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self, None)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.resize(self.sizeHint())
        self.today = datetime.date.today()

        self.check_net_connection()
        self.time_diff()
        self.total_counting()

        QtCore.QObject.connect(self.ui.date_start, QtCore.SIGNAL(_fromUtf8("dateChanged(QDate)")), self.time_diff)
        QtCore.QObject.connect(self.ui.date_end, QtCore.SIGNAL(_fromUtf8("dateChanged(QDate)")), self.time_diff)
        QtCore.QObject.connect(self.ui.spinBox_prepainment, QtCore.SIGNAL(_fromUtf8("valueChanged(QString)")),
                               self.total_counting)
        QtCore.QObject.connect(self.ui.SpinBox_square, QtCore.SIGNAL(_fromUtf8("valueChanged(QString)")),
                               self.total_counting)
        QtCore.QObject.connect(self.ui.spinBox_price, QtCore.SIGNAL(_fromUtf8("valueChanged(QString)")),
                               self.total_counting)


    def time_diff(self):
        t_start = self.ui.date_start.date()
        t_end = self.ui.date_end.date()
        diff_from_now = self.today - t_start.toPyDate()
        diff_from_end = t_end.toPyDate() - t_start.toPyDate()
        Main.month_total = round(diff_from_end.days / 30.)
        Main.month_from_now = round(diff_from_now.days / 30.)
        print(Main.month_total, Main.month_from_now)
        self.total_counting()

    def total_counting(self):
        square = self.ui.SpinBox_square.value()
        price = self.ui.spinBox_price.value()
        Main.total_price = round(square * price)
        Main.balance_amount = Main.total_price - self.ui.spinBox_prepainment.value()
        Main.mon_payment = Main.balance_amount / (Main.month_total - 1)
        self.ui.spinBox_total.setValue(int(Main.total_price))
        self.ui.spinBox_mon_pay.setValue(int(Main.mon_payment))
        self.ui.spinBox_balance_amount.setValue(int(Main.balance_amount))
        print(Main.mon_payment, Main.total_price, Main.month_total)

    def check_net_connection(self):
        try:
            r = requests.get('http://ukrstat.gov.ua/operativ/operativ2015/ct/icv/icv_u/icv_pm15_u.html')
            print(r)
            if '[404]' in r:
                raise requests.ConnectionError
            else:
                page_answer = r.content
        except requests.ConnectionError:
            self.ui.statusbar.showMessage('Page with index inflation not found!')
            self.ui.checkBox.setEnabled(False)


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon("main.ico"))
    myClipBoard = QtGui.QApplication.clipboard()
    window = Main()
    window.show()
    sys.exit(app.exec_())
