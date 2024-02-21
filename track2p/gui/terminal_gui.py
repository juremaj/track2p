from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QTextEdit

class ConsoleOutput(QTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)

    def write(self, text):
        self.insertPlainText(text)
        self.flush()

    def flush(self):
        QApplication.processEvents()
