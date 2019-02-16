import sys
from PyQt5 import QtWidgets
from PyQt5.QtCore import QObject, pyqtSignal, Qt
from reporter import Ui_Dialog


class myWindow(QtWidgets.QDialog, Ui_Dialog):
    def __init__(self):
        super(myWindow, self).__init__()
        self.setupUi(self)
        self.setWindowTitle("实验登记")
        self.confirm.pressed.connect(self.check_user_input)  # 注意这里不需要引号和括号，只需要写出函数名就可以了
        self.confirm.pressed.connect(self.check_machine_state)

    def check_user_input(self):
        for item in [self.name_box, self.number_box]:
            if item.toPlainText():
                print(item.toPlainText())

    def check_machine_state(self):
        if self.condition_right.checkState() and self.condition_wrong.checkState():
            print("只能选一个！")
        else:
            if self.condition_right.checkState():
                print("仪器正常，不错")
            if self.condition_wrong.checkState():
                print("请务必描述仪器具体故障状况，发现故障的时间，并立即联系仪器负责人！")

    def prompt_report(self):
        if not self.condition_right.checkState():
            print("请确定是否需要输入故障信息！")


app = QtWidgets.QApplication(sys.argv)
application = myWindow()
application.show()
#  check if user has inputted all the necessary items.
sys.exit(app.exec_())