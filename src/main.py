import sys
import os
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QFile, QTextStream

from ui.mainwindow import MainWindow
from core.profiler import Profiler
from core.connector import Connector

class MyApp(QApplication):
    def __init__(self, argv):
        super().__init__(argv)
        self.app_dir = "/opt/wolfopenvpnclient/src"
        self.connector = Connector()
        self.profiler = Profiler()
        self.connected = False

def main():
    app = MyApp(sys.argv)

    script_dir = os.path.dirname(os.path.abspath(__file__))
    styles_file_path = os.path.join(script_dir, "Resources", "main.qss")

    styles_file = QFile(styles_file_path)
    if styles_file.open(QFile.ReadOnly | QFile.Text):
        stream = QTextStream(styles_file)
        app.setStyleSheet(stream.readAll())
        styles_file.close()

    main_window = MainWindow(app)
    main_window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()