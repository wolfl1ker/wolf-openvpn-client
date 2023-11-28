from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QDialogButtonBox, QSpacerItem, QSizePolicy

class QuitDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Exit confirmation")
        self.setGeometry(200, 200, 400, 100)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        question_label = QLabel("Are you sure you want to disconnect and quit the app?")
        layout.addWidget(question_label)

        spacer_item = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        layout.addItem(spacer_item)

        button_panel = QDialogButtonBox(QDialogButtonBox.Yes | QDialogButtonBox.No)
        button_panel.accepted.connect(self.accept)
        button_panel.rejected.connect(self.reject)
        layout.addWidget(button_panel)

        self.setLayout(layout)