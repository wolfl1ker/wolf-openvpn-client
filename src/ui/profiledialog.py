from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFileDialog, QHBoxLayout, QSpacerItem, QSizePolicy
from PySide6.QtCore import Qt
from .errorlabel import ErrorLabel

class ProfileDialog(QDialog):
    def __init__(self, app, parent=None):
        super(ProfileDialog, self).__init__(parent)
        self.app = app
        self.setWindowTitle("Add Profile")
        self.setGeometry(200, 200, 400, 300)
        self.setFixedSize(400, 300)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Display name label and error label
        display_name_layout = QHBoxLayout()
        display_name_label = QLabel("Display Name:")
        self.display_name_error = ErrorLabel("")
        display_name_layout.addWidget(display_name_label)
        display_name_layout.addWidget(self.display_name_error)
        layout.addLayout(display_name_layout)

        # Display name input
        self.display_name_input = QLineEdit()
        layout.addWidget(self.display_name_input)

        # File label and error label
        file_label_layout = QHBoxLayout()
        profile_file_label = QLabel("Configuration File:")
        self.profile_file_error = ErrorLabel("")
        file_label_layout.addWidget(profile_file_label)
        file_label_layout.addWidget(self.profile_file_error)
        layout.addLayout(file_label_layout)

        # File input
        file_layout = QHBoxLayout()
        self.profile_file_input = QLineEdit()
        file_selection_button = QPushButton("Select File")
        file_selection_button.setFixedSize(100, 40)
        file_selection_button.clicked.connect(self._select_file)
        file_layout.addWidget(self.profile_file_input)
        file_layout.addWidget(file_selection_button)
        layout.addLayout(file_layout)

        # Spacer
        spacer_item = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        layout.addItem(spacer_item)

        # Bottom buttons Save, Close
        buttons_layout = QHBoxLayout()
        spacing_label = QLabel("")
        spacing_label.setFixedSize(300, 40)
        close_button = QPushButton("Close")
        close_button.setFixedSize(100, 40)
        close_button.clicked.connect(self.reject)  # Close the dialog
        save_button = QPushButton("Save")
        save_button.setFixedSize(100, 40)
        save_button.clicked.connect(self._save_profile)
        buttons_layout.addWidget(spacing_label)
        buttons_layout.addWidget(close_button, alignment=Qt.AlignRight)
        buttons_layout.addWidget(save_button, alignment=Qt.AlignRight)
        layout.addLayout(buttons_layout)

        self.setLayout(layout)

    # @internal
    # Opens a File Select Dialog
    def _select_file(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Select OVPN Configuration File", "", "All Files (*)", options=options)
        if file_path:
            self.profile_file_input.setText(file_path)

    # @internal
    # Validates profile before send it to ProfilesWindow
    def _save_profile(self):
        display_name = self.display_name_input.text()
        profile_file = self.profile_file_input.text()

        # Check if display name empty
        if not display_name or display_name == '':
            self.display_name_error.setText("This field is required")
            return
        else:
            self.display_name_error.setText("")

        # Check if config file path empty
        if not profile_file or profile_file == '':
            self.profile_file_error.setText("This field is required")
            return
        else:
            self.profile_file_error.setText("")

        # Check if config file is not *.ovpn format file
        if not profile_file.endswith(".ovpn"):
            self.profile_file_error.setText("The filetype should be .ovpn")
            return
        else:
            self.profile_file_error.setText("")

        # Check already in use case
        for profile in self.app.profiler.get_profiles():
            if profile['name'] == display_name:
                self.display_name_error.setText("This profile name already in use")
                return
            if profile['path'] == profile_file or profile['path'].split('/')[-1] == profile_file.split('/')[-1]:
                self.profile_file_error.setText("This config file already in use")
                return
        self.display_name_error.setText("")
        self.profile_file_error.setText("")

        # if all passed -> accept dialog
        self.accept()