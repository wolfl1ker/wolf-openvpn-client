from PySide6.QtWidgets import QMainWindow, QLabel, QComboBox, QPushButton, QVBoxLayout, QWidget, QDialog, QTableWidget, QTableWidgetItem, QHeaderView
from PySide6.QtGui import QAction
from PySide6.QtCore import Qt, QThread, Signal
from .profileswindow import ProfilesWindow
from .statuswindow import StatusWindow
from .aboutwindow import AboutWindow
from .quitdialog import QuitDialog

class ConnectorThread(QThread):
    status_signal = Signal(str)

    def __init__(self, connector, path):
        super(ConnectorThread, self).__init__()
        self.connector = connector
        self.profile = path

    def run(self):
        result = self.connector.connect(self.profile)
        self.status_signal.emit(result)

class MainWindow(QMainWindow):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.profile = {"name": "", "path": ""}

        self.setGeometry(300, 300, 300, 175)
        self.setFixedSize(300, 225)
        self.setWindowTitle("Wolf OpenVPN Client")

        self.init_menu_bar()
        self.init_ui()

    def init_menu_bar(self):
        menu_bar = self.menuBar()

        # File menu
        file_menu = menu_bar.addMenu("File")
        profiles_action = QAction("Profiles", self)
        exit_action = QAction("Exit", self)
        file_menu.addAction(profiles_action)
        file_menu.addAction(exit_action)

        # Connection menu
        connection_menu = menu_bar.addMenu("Connection")
        status_action = QAction("Status", self)
        connection_menu.addAction(status_action)

        # About menu
        about_menu = menu_bar.addMenu("About")
        about_action = QAction("About", self)
        about_menu.addAction(about_action)

        # Triggers
        profiles_action.triggered.connect(self._show_profiles_window)
        exit_action.triggered.connect(self.close)
        status_action.triggered.connect(self._show_status_window)
        about_action.triggered.connect(self._show_about_window)

    def _show_profiles_window(self):
        self.profiles_window = ProfilesWindow(self.app, self)
        self.profiles_window.show()

    def _show_status_window(self):
        self.status_window = StatusWindow(self.app, self.profile['path'])
        self.status_window.show()

    def _show_about_window(self):
        self.about_window = AboutWindow(self.app)
        self.about_window.show()

    def init_ui(self):
        # Set up the layout
        layout = QVBoxLayout()

        self.status_label = QLabel("Not Connected", self)
        self.status_label.setWordWrap(True)

        self.profiles_table = QTableWidget()
        self.profiles_table.setSelectionMode(QTableWidget.SingleSelection)
        self.profiles_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.profiles_table.setColumnCount(1)
        self.profiles_table.verticalHeader().setVisible(False)
        self.profiles_table.horizontalHeader().setVisible(False)
        self.profiles_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.update_profiles_table()

        self.connect_button = QPushButton("Connect", self)
        self.connect_button.clicked.connect(self._connect_function)

        layout.addWidget(self.status_label)
        layout.addWidget(self.profiles_table)
        layout.addWidget(self.connect_button)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def update_profiles_table(self):
        profiles = self.app.profiler.get_profiles()
        self.profiles_table.setRowCount(len(profiles))
        for row, profile in enumerate(profiles):
            item = QTableWidgetItem(profile['name'])
            self.profiles_table.setItem(row, 0, item)

    def _connect_function(self):
        selected_items = self.profiles_table.selectedItems()
        if not selected_items:
            self.status_label.setText("Select one of profile below")
            return
        selected_row = selected_items[0].row()
        profile_name = self.profiles_table.item(selected_row, 0).text()
        self.profile = self.app.profiler.get_profile_by_name(profile_name)

        # Thread, because it was freezing my main process
        self.thread = ConnectorThread(self.app.connector, self.profile['path'])
        self.thread.status_signal.connect(self._update_status)
        self.thread.start()

        self.status_label.setText(f"Trying connect to: {profile_name}. Please wait...")
        self.connect_button.clicked.disconnect(self._connect_function)
        self.connect_button.clicked.connect(self._disconnect_function)
        self.connect_button.setText("Disconnect")

    def _disconnect_function(self):
        self.app.connector.disconnect(self.profile['path'])
        # Cleaning up
        self.profile = {"name": "", "path": ""}
        self.app.connected = False
        self.status_label.setText("Not Connected")
        self.connect_button.clicked.disconnect(self._disconnect_function)
        self.connect_button.clicked.connect(self._connect_function)
        self.connect_button.setText("Connect")

    def _update_status(self, status):
        self.app.connected = True
        self.status_label.setText(f"Connected to: {self.profile['name']}")

    def _show_confirmation_dialog(self, event):
        dialog = QuitDialog(self)
        result = dialog.exec()

        if result == QDialog.Accepted:
            self.app.connector.disconnect(self.profile['path'])
            event.accept()
        else:
            event.ignore()
            return

    def closeEvent(self, event):
        if self.app.connected == True:
            self._show_confirmation_dialog(event)
        else:
            event.accept()