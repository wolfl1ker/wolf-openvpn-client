from PySide6.QtWidgets import QLabel

# ErrorLabel class from QLabel for custom red-style
class ErrorLabel(QLabel):
    def __init__(self, text):
        super().__init__(text)