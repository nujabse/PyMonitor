import sys
from PyQt5 import QtWidgets
from reporter import Ui_Dialog


class myWindow(QtWidgets.QDialog):
    def __init__(self):
        super(myWindow, self).__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)


app = QtWidgets.QApplication(sys.argv)
application = myWindow()
application.show()
# check if user has inputted all the necessary items.
print(application.)
sys.exit(app.exec_())