import sys
from PyQt5 import QtWidgets
import csv
import time
from reporter import Ui_Dialog
# from alerter import AlertWindow


class MyWindow(QtWidgets.QDialog, Ui_Dialog):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.setupUi(self)
        self.setWindowTitle("实验登记")
        # set confirm button event connect
        self.confirm.pressed.connect(self.check_user_input)  # 注意这里不需要引号和括号，只需要写出函数名就可以了
        self.confirm.pressed.connect(self.check_machine_state)
        self.confirm.pressed.connect(self.recorder)
        self.confirm.pressed.connect(self.data_writer)
        self.row = []

    def check_user_input(self):
        items = [self.name_box.toPlainText(), self.number_box.toPlainText(), self.condition_right.checkState(), self.condition_wrong.checkState()]
        if any(not item for item in items):
            self.show_alerter()

    def check_machine_state(self):
        if self.condition_right.checkState() and self.condition_wrong.checkState():
            print("只能选一个！")
        else:
            if self.condition_right.checkState():
                print("仪器正常，不错")
                self.row.append("正常")
            if self.condition_wrong.checkState():
                print("请务必描述仪器具体故障状况，发现故障的时间，并立即联系仪器负责人！")
                self.row.append("故障")

    def recorder(self):
        """
        record all the user input message to a list for data_writer to write to file
        :return: self.row
        """
        print('Now recording user input')
        self.row.append(time.asctime())
        for item in [self.name_box, self.number_box]:
            self.row.append(item.toPlainText())
        if self.error_box.toPlainText():
            self.row.append(self.error_box.toPlainText())
        else:
            print("User input all recorded!")

    def data_writer(self):
        print(self.row)
        with open('monitor.csv', 'at') as f:
            f_csv = csv.writer(f)
            f_csv.writerow(self.row)

    # noinspection PyCallByClass
    def show_alerter(self):
        reply = QtWidgets.QMessageBox.warning(self, '警告', '请确保输入信息完整正确！', QtWidgets.QMessageBox.Yes |QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            print('继续吧')
            self.row = []


app = QtWidgets.QApplication(sys.argv)
application = MyWindow()
application.show()
#  TODO: prohibit user from exiting through pressing ESC
#  TODO: 解决无法输入中文的问题
sys.exit(app.exec_())