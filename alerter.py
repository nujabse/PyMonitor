import sys
from PyQt5 import QtWidgets
from NotCompleteAlert import Ui_Dialog


class AlertWindow(QtWidgets.QDialog, Ui_Dialog):
    def __init__(self):
        super(AlertWindow, self).__init__()
        self.setupUi(self)
        self.setWindowTitle("警告")
        self.confirm.pressed.connect(sys.exit)


app = QtWidgets.QApplication(sys.argv)
application = AlertWindow()
application.show()
sys.exit(app.exec_())