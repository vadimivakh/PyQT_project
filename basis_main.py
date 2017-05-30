# -*- coding: utf-8 -*-

import os
import sys
from PyQt4 import QtCore
from PyQt4 import QtGui
import datetime

os.popen(r'C:\Python34\Lib\site-packages\PyQt4\pyuic window.ui>>main_window.py')
from main_window import Ui_MainWindow  # import generated window

_fromUtf8 = QtCore.QString.fromUtf8


class Main(QtGui.QMainWindow):
    def __init__(self):

        QtGui.QMainWindow.__init__(self, None)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.resize(self.sizeHint())

        self.result()

        QtCore.QObject.connect(self.ui.date_start, QtCore.SIGNAL(_fromUtf8("dateChanged(QDate)")), self.result)
        QtCore.QObject.connect(self.ui.date_end, QtCore.SIGNAL(_fromUtf8("dateChanged(QDate)")), self.result)
        QtCore.QObject.connect(self.ui.spinBox_prepainment, QtCore.SIGNAL(_fromUtf8("valueChanged(QString)")),
                               self.result)
        QtCore.QObject.connect(self.ui.SpinBox_square, QtCore.SIGNAL(_fromUtf8("valueChanged(QString)")),
                               self.result)
        QtCore.QObject.connect(self.ui.spinBox_price, QtCore.SIGNAL(_fromUtf8("valueChanged(QString)")),
                               self.result)


    def result(self):
        apartment_square = self.ui.SpinBox_square.value()
        price_m2 = self.ui.spinBox_price.value()
        Main.total_price = apartment_square * price_m2
        Main.rest = Main.total_price - self.ui.spinBox_prepainment.value()
        finish_time = self.ui.date_end.date().toPyDate()
        start_time = self.ui.date_start.date().toPyDate()
        delta_time = finish_time - start_time
        delta_now = datetime.date.today() - start_time
        Main.month_total = round(delta_time.days/30.0)
        Main.month_pay = Main.rest / (Main.month_total - 1)
        Main.month_total = round(delta_time.days/30.0)

        self.ui.spinBox_total.setValue(int(Main.total_price))
        self.ui.spinBox_mon_pay.setValue(int(Main.month_pay))
        self.ui.spinBox_balance_amount.setValue(int(Main.rest))


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon("main.ico"))
    myClipBoard = QtGui.QApplication.clipboard()
    window = Main()
    window.show()
    sys.exit(app.exec_())
