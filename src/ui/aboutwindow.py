import sys
import os
from PySide6.QtWidgets import QLabel, QWidget, QHBoxLayout
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap

class AboutWindow(QWidget):
    def __init__(self, app):
        super(AboutWindow, self).__init__()
        self.app = app
        self.setWindowTitle("About")
        self.setGeometry(400, 400, 620, 150)
        self.setFixedSize(640, 200)
        self.init_ui()

    def init_ui(self):
        layout = QHBoxLayout()

        icon_label = QLabel()
        icon_label.setFixedSize(150, 150)
        icon_pixmap = QPixmap(os.path.join(self.app.app_dir, "Resources/murzik_circle.png"))
        icon_label.setPixmap(icon_pixmap)
        layout.addWidget(icon_label)

        text_label = QLabel("""
An OpenVpn3 client for Linux operating systems.<br>
Built on PySide6 using Python3.<br>
This is free-for-use application<br>
<br>
Developed by Andrei Baev (<a href="https://www.linkedin.com/in/wolfl1ker">@wolfl1ker</a>
or <a href="https://steamcommunity.com/id/wolfl1ker">steam:@wolfl1ker</a>)<br>
""")
        text_label.setFixedSize(420, 150)
        text_label.setOpenExternalLinks(True)
        text_label.setTextFormat(Qt.RichText)
        text_label.setWordWrap(True)
        text_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(text_label)

        self.setLayout(layout)
