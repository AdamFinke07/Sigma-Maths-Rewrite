from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QApplication, QMainWindow
import os
from Login_ui import Ui_Login
import sqlite3
from Register import RegisterScreen
from Database import Database


class LoginScreen(QtWidgets.QWidget, Ui_Login):
    def __init__(self, show_main_callback, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.show_main_callback = show_main_callback  # CALLBACK TO MAIN SCREEN (WORKS DONT TOUCH)
        self.db = Database()  # Create an instance of Database
        self.init_ui()

    def show_login_window(self):
            global main_window
            RegisterScreen.close()   
            login_screen = LoginScreen()
            login_screen.show()

    def init_ui(self):
        self.PBLogin.clicked.connect(self.handle_login)
        self.PBRegister.clicked.connect(self.register)

    def register(self):
        # Create and show register screen with callback to return to login
        self.register_screen = RegisterScreen(show_login_callback=self.show)
        self.register_screen.show()
        self.hide()  # Hide login window while register is shown

    def handle_login(self):
        username = self.LEUsername.text().strip()
        password = self.LEPassword.text().strip()
        
        if not username or not password:
            QtWidgets.QMessageBox.warning(self, "Login Failed", "Username and password cannot be empty")
            return
            
        if self.db.verify_user(username, password):
            print("Login successful")
            self.show_main_callback()
        else:
            QtWidgets.QMessageBox.warning(self, "Login Failed", "Invalid username or password")

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key.Key_Return or event.key() == QtCore.Qt.Key.Key_Enter:
            self.handle_login()
        else:
            super().keyPressEvent(event)