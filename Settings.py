from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QMainWindow
from Settings_ui import Ui_Settings

class SettingsWindow(QMainWindow, Ui_Settings):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.init_ui()

    def init_ui(self):
        pass  # You can add any additional initialization here later