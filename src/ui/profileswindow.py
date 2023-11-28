import sys
from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout, QWidget, QLabel, QPushButton, QTableWidget, QTableWidgetItem, QHeaderView, QDialog
from PySide6.QtCore import Qt
from .profiledialog import ProfileDialog

class ProfilesWindow(QWidget):
    def __init__(self, app, main_window):
        super(ProfilesWindow, self).__init__()
        self.app = app
        self.main_window = main_window
        self.setWindowTitle("Profiles")
        self.setGeometry(200, 200, 600, 500)
        self.setFixedSize(600, 500)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # First row with label and buttons
        label = QLabel("Configuration Profiles:")
        add_button = QPushButton("Add")
        add_button.setFixedSize(100, 35)
        add_button.clicked.connect(self._show_add_profile_dialog)
        delete_button = QPushButton("Delete")
        delete_button.setFixedSize(100, 35)
        delete_button.clicked.connect(self._delete_profile)
        # Adding to layout
        button_layout = QHBoxLayout()
        button_layout.addWidget(label)
        button_layout.addWidget(add_button)
        button_layout.addWidget(delete_button)
        layout.addLayout(button_layout)

        # Table view
        self.profiles_table = QTableWidget()
        self.profiles_table.setSelectionMode(QTableWidget.SingleSelection)
        self.profiles_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.profiles_table.setColumnCount(1)
        self.profiles_table.verticalHeader().setVisible(False)
        self.profiles_table.horizontalHeader().setVisible(False)
        self.profiles_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        layout.addWidget(self.profiles_table)
        self._update_profiles_table()

        # Save button
        save_button = QPushButton("Save")
        save_button.setFixedSize(100, 35)
        save_button.clicked.connect(self.close)
        layout.addWidget(save_button, alignment=Qt.AlignRight)

        self.setLayout(layout)

    # @internal
    # Updates the profiles table from Profiler.get_profiles()
    def _update_profiles_table(self):
        profiles = self.app.profiler.get_profiles()
        self.profiles_table.setRowCount(len(profiles))
        for row, profile in enumerate(profiles):
            item = QTableWidgetItem(profile['name'])
            self.profiles_table.setItem(row, 0, item)

    # @internal
    # Handler for Delete button
    def _delete_profile(self):
        selected_items = self.profiles_table.selectedItems()
        if not selected_items:
            return
        selected_row = selected_items[0].row()
        profile_name = self.profiles_table.item(selected_row, 0).text()
        self.app.profiler.delete_profile_by_name(profile_name)
        self._update_profiles_table()

    # @internal
    # Handler for Add button
    def _show_add_profile_dialog(self):
        profile_dialog = ProfileDialog(self.app, self)
        result = profile_dialog.exec_()
        if result == QDialog.Accepted:
            display_name = profile_dialog.display_name_input.text()
            config_file = profile_dialog.profile_file_input.text()
            self._add_profile(display_name, config_file)

    # @internal
    # Adds new profile {name='display_name', path='config_file'}
    def _add_profile(self, display_name, config_file):
        new_profile = {"name": display_name, "path": config_file}
        self.app.profiler.save_profile(new_profile)
        self._update_profiles_table()

    # on close ProfilesWindow, refresh the profile selector in MainWindow
    def closeEvent(self, event):
        self.main_window.update_profiles_table()
        event.accept()
