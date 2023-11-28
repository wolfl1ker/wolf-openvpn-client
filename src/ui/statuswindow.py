import sys
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSpacerItem, QSizePolicy
from PySide6.QtCore import Qt, QTimer, Slot

class StatusWindow(QWidget):
    def __init__(self, app, profile):
        super(StatusWindow, self).__init__()
        self.app = app
        self.profile = profile
        self.stats = {'BYTES_IN': None, 'BYTES_OUT': None, 'PACKETS_IN': None, 'PACKETS_OUT': None}

        self.setWindowTitle("Status")
        self.setGeometry(200, 200, 300, 200)
        self.setFixedSize(300, 200)

        # Call get_stats each 1 sec
        self.timer = QTimer()
        self.timer.timeout.connect(self.handleTimeout)
        self.timer.setInterval(1000)

        self.init_ui()
        self.timer.start()

    def init_ui(self):
        layout = QVBoxLayout()
        for stat_name in ['BYTES_IN', 'BYTES_OUT', 'PACKETS_IN', 'PACKETS_OUT']:
            new_layout = QHBoxLayout()
            name_label = QLabel(f"{stat_name}:")
            stat_label = QLabel("-")
            self.stats[stat_name] = stat_label
            new_layout.addWidget(name_label)
            new_layout.addWidget(stat_label)
            layout.addLayout(new_layout)
        spacer_item = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        layout.addItem(spacer_item)
        self.setLayout(layout)

    def closeEvent(self, event):
        if self.timer.isActive():
            self.timer.stop()
        del self.timer
        event.accept()

    @Slot()
    def handleTimeout(self):
        result = self.app.connector.get_stats(self.profile)
        if result:
            for stat_name, stat_label in self.stats.items():
                if result[stat_name]:
                    stat_label.setText(str(result[stat_name]))
                else:
                    stat_label.setText('-')