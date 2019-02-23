import sys
from PyQt5 import QtWidgets, QtCore, QtGui
import csv
import time
from reporter import Ui_Dialog
import psutil
import os
import subprocess


class MyWindow(QtWidgets.QDialog, Ui_Dialog):
    def __init__(self):
        super(MyWindow, self).__init__()
        # check if multiple instances are running.
        self.multi_run_alerter()
        self.setupUi(self)
        # set main window Icon
        self.setWindowIcon(QtGui.QIcon('Application.ico'))
        self.setWindowTitle("Agilent B2900A Quick IV Measurement Software")
        # hide error label first
        self.error_indicator.hide()
        self.ready_to_confirm = False
        self.ready_to_tray = False
        self.ready_to_exit = False
        # set systemtray Icon
        self.trayIcon = QtWidgets.QSystemTrayIcon(self)
        self.trayIcon.setIcon(QtGui.QIcon('tray.ico'))
        # self.trayIcon.activated.connect(self.trayClick)
        # set the * to change color when user enters text.
        # self.name_box.textEdited.connect(self.name_color_changer)
        self.input_watcher()
        # set app status monitor thread
        self.thread = StatusThread()
        self.thread.start()
        self.thread.device_status_signal.connect(self.status_refresh)
        # set confirm button event connect
        self.confirm.pressed.connect(self.check_machine_state)
        self.confirm.pressed.connect(self.recorder)
        self.confirm.pressed.connect(self.check_user_input)  # 注意这里不需要引号和括号，只需要写出函数名就可以了
        self.thread.start_time_signal.connect(self.start_time_log)
        self.thread.stop_time_signal.connect(self.usage_count)
        self.data = {
             "姓名": "",
             "学号": "",
             "仪器状况":"",
             "故障信息":"",
             "开始时间":"",
             "结束时间":""
        }

    def multi_run_alerter(self):
        if process_counter() > 2:
            reply = QtWidgets.QMessageBox.warning(self, '警告', '不能同时登记两个人！', QtWidgets.QMessageBox.Yes)
            if reply == QtWidgets.QMessageBox.Yes:
                self.close()

    def check_machine_state(self):
        if self.condition_right.checkState() and self.condition_wrong.checkState():
            self.duplicate_alerter()
        else:
            if self.condition_right.checkState():
                print("仪器正常，不错")
                self.data["仪器状况"] == "正常"
            if self.condition_wrong.checkState():
                self.data["仪器状况"] == "故障"
                self.malfunction_alerter()

    def recorder(self):
        print('Now recording user input')
        self.data["开始时间"] = time.asctime()
        self.data["姓名"] = self.name_box.text()
        self.data["学号"] = self.number_box.text()
        if self.error_box.toPlainText():
            self.data["故障信息"] = self.error_box.toPlainText()
        else:
            print("User input all recorded!")
        if self.condition_right.checkState():
            self.data["仪器状况"] = "良好"
            self.data["故障信息"] = "无"
        if self.condition_wrong.checkState():
            self.data["仪器状况"] = "故障"

    def check_user_input(self):
        input_items = [self.name_box.text(), self.number_box.text()]
        if all(item for item in input_items):
            if self.condition_right.checkState() and not self.condition_wrong.checkState():
                self.ready_to_confirm = True
                self.show_confirmation()
            if not self.condition_right.checkState() and self.condition_wrong.checkState() and self.error_box.toPlainText():
                self.ready_to_confirm = True
                self.show_confirmation()
        else:
            self.show_alerter()

    def name_color_changer(self):
        # changes color
        print('输入用户名！')
        self.name_indicator.hide()

    def number_color_changer(self):
        self.number_indicator.hide()

    def good_condition_color_changer(self):
        self.state_indicator.hide()
    
    def error_condition_color_changer(self):
        # changes color only when condition wrong is checked
        self.state_indicator.hide()
        self.error_indicator.show()


    def input_watcher(self):
        self.name_box.textEdited.connect(self.name_color_changer)
        self.number_box.textEdited.connect(self.number_color_changer)
        self.condition_right.toggled.connect(self.good_condition_color_changer)
        self.condition_wrong.toggled.connect(self.error_condition_color_changer)

    
    def data_writer(self):
        print(self.data)
        with open('monitor.csv', 'at') as f:
            fieldnames = ["姓名","学号","仪器状况","故障信息","开始时间","结束时间"]
            f_csv = csv.DictWriter(f, fieldnames=fieldnames)
            f_csv.writerow(self.data)

    def show_alerter(self):
        reply = QtWidgets.QMessageBox.warning(self, '警告', '请确保全部必选框都填完并且正确！', QtWidgets.QMessageBox.Yes)
        if reply == QtWidgets.QMessageBox.Yes:
            print('没有填完！')
            
    def malfunction_alerter(self):
        reply = QtWidgets.QMessageBox.warning(self, '警告', '请务必描述仪器具体故障状况，发现故障的时间，并立即联系仪器负责人!', QtWidgets.QMessageBox.Yes)
        if reply == QtWidgets.QMessageBox.Yes:
            print("请务必描述仪器具体故障状况，发现故障的时间，并立即联系仪器负责人！")
            
    def duplicate_alerter(self):
        reply = QtWidgets.QMessageBox.warning(self, '警告', '只能勾选一个！', QtWidgets.QMessageBox.Yes)
        if reply == QtWidgets.QMessageBox.Yes:
            print('重复选择！')
            
    def show_confirmation(self):
        if self.ready_to_confirm:
            # convert list to string
            user_input = "\n".join(("{}: {}".format(*i) for i in self.data.items()))
            reply = QtWidgets.QMessageBox.information(self, '请核对以下信息是否属实！', user_input, QtWidgets.QMessageBox.Yes |QtWidgets.QMessageBox.No)
            if reply == QtWidgets.QMessageBox.Yes:
                print('登记完毕！')
                self.ready_to_tray = True
                path1 = os.path.abspath('.')
                # use popen to run command async
                subprocess.Popen(path1 + "/Agilent B2900A Quick IV Measurement Software/B291xUtility.exe")
                self.to_system_tray()
            if reply == QtWidgets.QMessageBox.No:
                print('再确认一遍！')

    def closeEvent(self, event):
        # block user quitting
        print("user is asking to quit!")
        if self.ready_to_exit or process_counter() > 2:
            event.accept()
        else:
            event.ignore()
            print('请完善所有数据！')

    def keyPressEvent(self, QKeyEvent):
        # block esc key
        if QKeyEvent.key() == QtCore.Qt.Key_Escape:
            print("不能退出！")

    def status_refresh(self, status):
        self.device_state.setText(status)
    
    def start_time_log(self, starttime):
        self.ready_to_exit = True

    def usage_count(self, endtime):
        if self.ready_to_tray and self.ready_to_exit:
            self.data['结束时间'] = endtime
            self.data_writer()
            self.close()

    def trayClick(self, reason):
        if self.ready_to_tray:
            print('最大化到窗口！')
            if reason == QtWidgets.QSystemTrayIcon.DoubleClick:
                self.trayIcon.hide()
                self.showNormal()
    
    def to_system_tray(self):
        if self.ready_to_tray:
            print('最小化到托盘！')
            self.trayIcon.show()
            self.hide()


class StatusThread(QtCore.QThread):
    device_status_signal = QtCore.pyqtSignal(str)
    start_time_signal = QtCore.pyqtSignal(str)
    stop_time_signal = QtCore.pyqtSignal(str)
    multiple_run_signal = QtCore.pyqtSignal(str)

    def __init__(self):
        super(StatusThread, self).__init__()

    def run(self, name='B291xUtility.exe', refresh_rate=0.5):
        # prevent user from opening multiple instances of this program.
        if process_counter() == 2:
            print('开了一个程序！')
        else:
            print('开了多个程序！')
            self.multiple_run_signal.emit('不能多开程序！')

        while 1:
            if name in [proc.name() for proc in psutil.process_iter(attrs=['pid', 'name'])]:
                print('安捷伦软件已启动！')
                self.device_status_signal.emit('已开启')
                self.start_time_signal.emit(time.asctime())
                time.sleep(refresh_rate)
            else:
                print('安捷伦软件已关闭！')
                self.device_status_signal.emit('已关闭')
                self.stop_time_signal.emit(time.asctime())
                time.sleep(refresh_rate)


def process_counter(name='main.exe'):
        count = [p.name() for p in psutil.process_iter()].count(name)
        return count

# TODO: add data encryption.
app = QtWidgets.QApplication(sys.argv)
application = MyWindow()
application.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
# disable minimize and maximize.
application.setWindowFlags(application.windowFlags() & ~QtCore.Qt.WindowMinimizeButtonHint & ~QtCore.Qt.WindowMaximizeButtonHint)
application.show()
sys.exit(app.exec_())