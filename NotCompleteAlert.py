# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'NotCompleteAlert.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 300)
        self.confirm = QtWidgets.QPushButton(Dialog)
        self.confirm.setGeometry(QtCore.QRect(140, 240, 90, 32))
        self.confirm.setObjectName("confirm")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(70, 80, 291, 151))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setObjectName("label")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.confirm.setText(_translate("Dialog", "确定"))
        self.label.setText(_translate("Dialog", "请确保登记填完所有信息再开始实验！"))

