import sys

from PyQt5.QtWidgets import QApplication

from delta_control.windows.main_window import MainWindow


def excepthook(cls, traceback, exception):
    sys.excepthook(cls, traceback, exception)


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.excepthook = excepthook
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
