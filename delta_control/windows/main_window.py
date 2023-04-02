from time import sleep

from serial.tools import list_ports
from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5 import uic, QtCore

from delta_control.utils.port_listener import PortListener
from utils.angles import calculate_forward
from utils.worker_thread import WorkerThread


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.dialog = None
        self.worker = None
        self.portListener = None
        uic.loadUi('delta_control/windows/ui/main.ui', self)

        self.port = ""

        self.moveButton.clicked.connect(self.move)

        self.init_ui()

    def init_ui(self):
        self.setStyleSheet("QToolTip{color: black; font-size: 20px}")
        self.updatePortList()
        self.portListener = PortListener()
        self.portListener.update.connect(self.updatePortList)

    def move(self):
        self.worker = WorkerThread(self.comboBox.currentText())
        self.worker.messageReceived.connect(self.processBoardOutput)
        if self.comboBox.currentText() == '':
            self.dialog = self.create_dialog(
                'Ошибка подключения', 'Устройство не найдено. Переподключите и повторите попытку.')
            self.dialog.exec()
            return
        x = float(self.xDoubleSpinBox.value())
        y = float(self.yDoubleSpinBox.value())
        z = float(self.zDoubleSpinBox.value())
        print(calculate_forward(x, y, z))
        self.worker.serialDevice.write(b'move %f %f %f\n' % calculate_forward(x, y, z))
        dialog = self.create_dialog("Информация", "Операция выполнена успешно.")
        sleep(2)
        dialog.exec()

    def updatePortList(self):
        self.comboBox.clear()
        self.comboBox.setEditable(True)
        for port in list_ports.comports():
            self.comboBox.addItem(port.name)
        self.comboBox.lineEdit().setAlignment(QtCore.Qt.AlignCenter)
        self.comboBox.lineEdit().setReadOnly(True)
        self.comboBox.setStyleSheet('font-size: 20px; background-color: #e2e2e2')

    def processBoardOutput(self, text: str):
        pass

    def create_dialog(self, title, message):
        dialog = QMessageBox(self)
        dialog.setWindowTitle(title)
        dialog.setText(message)
        return dialog
