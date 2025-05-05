from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QApplication, QMainWindow
import os
from PtQt6UI import Ui_Register
import sqlite3
from Database import Database

class RegisterScreen(QtWidgets.QWidget, Ui_Register):
    def __init__(self, show_login_callback, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.show_login_callback = show_login_callback
        self.db = Database()  # Create an instance of Database
        self.init_ui()

    def init_ui(self):
        self.PBRegister.clicked.connect(self.handle_register)  # Connect button to handler

    def handle_register(self):
        # Get user input
        username = self.LEUsername.text().strip()
        password = self.LEPassword.text().strip()
        confirm_password = self.LEPasswordConfirm.text().strip()

        # Basic validation
        if not username or not password:
            QtWidgets.QMessageBox.warning(self, "Error", "Username and password cannot be empty.")
            return
        if password != confirm_password:
            QtWidgets.QMessageBox.warning(self, "Error", "Passwords do not match.")
            return
            
        # Check if username already exists
        if self.db.username_exists(username):
            QtWidgets.QMessageBox.warning(self, "Error", "Username already exists.")
            return
            
        # Try to add the user
        if self.db.add_user(username, password):
            QtWidgets.QMessageBox.information(self, "Success", "Registration successful! You can now login.")
            # After successful registration, trigger callback to return to login
            self.show_login_callback()
            self.close()  # Close the register window
        else:
            QtWidgets.QMessageBox.warning(self, "Error", "Failed to register user. Please try again.")

