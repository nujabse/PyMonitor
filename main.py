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
        self.confirm.pressed.connect(self.check_machine_state)
        self.confirm.pressed.connect(self.recorder)
        self.confirm.pressed.connect(self.check_user_input)  # 注意这里不需要引号和括号，只需要写出函数名就可以了
        self.confirm.pressed.connect(self.data_writer)
        self.row = []

    def check_user_input(self):
        input_items = [self.name_box.toPlainText(), self.number_box.toPlainText()]
        toggle_items = [self.condition_right.checkState(), self.condition_wrong.checkState()]
        if any(not item for item in input_items):
            self.show_alerter()
        if all(item for item in input_items) and any(toggle_item for toggle_item in toggle_items):
            self.show_confirmation()

    def check_machine_state(self):
        if not self.condition_right.checkState() and not self.condition_wrong.checkState():
            self.show_alerter()
        if self.condition_right.checkState() and self.condition_wrong.checkState():
            self.duplicate_alerter()
        else:
            if self.condition_right.checkState():
                print("仪器正常，不错")
                self.row.append("正常")
            if self.condition_wrong.checkState():
                self.row.append("故障")
                self.malfunction_alerter()

    def recorder(self):
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

    def show_alerter(self):
        reply = QtWidgets.QMessageBox.warning(self, '警告', '请确保全部必选框都填完并且正确！', QtWidgets.QMessageBox.Yes)
        if reply == QtWidgets.QMessageBox.Yes:
            print('没有填完！')
            self.row = []

    def malfunction_alerter(self):
        reply = QtWidgets.QMessageBox.warning(self, '警告', '请务必描述仪器具体故障状况，发现故障的时间，并立即联系仪器负责人!', QtWidgets.QMessageBox.Yes)
        if reply == QtWidgets.QMessageBox.Yes:
            print("请务必描述仪器具体故障状况，发现故障的时间，并立即联系仪器负责人！")
            self.row = []

    def duplicate_alerter(self):
        reply = QtWidgets.QMessageBox.warning(self, '警告', '只能勾选一个！', QtWidgets.QMessageBox.Yes)
        if reply == QtWidgets.QMessageBox.Yes:
            print('重复选择！')
            self.row = []

    def show_confirmation(self):
        # convert list to string
        user_input = '\n'.join(self.row)
        reply = QtWidgets.QMessageBox.information(self, '请核对以下信息是否属实！', user_input, QtWidgets.QMessageBox.Yes |QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            print('登记完毕！')
            self.row = []


app = QtWidgets.QApplication(sys.argv)
application = MyWindow()
application.show()
#  TODO: prohibit user from exiting through pressing ESC
#  TODO: 解决无法输入中文的问题
sys.exit(app.exec_())