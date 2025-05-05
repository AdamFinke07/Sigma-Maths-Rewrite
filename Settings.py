from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QMainWindow, QMessageBox
from PtQt6UI import Ui_Settings
from Database import Database
import hashlib

class SettingsWindow(QMainWindow, Ui_Settings):
    def __init__(self, username, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.username = username
        self.db = Database()
        self.init_ui()

    def init_ui(self):
        # Set current username
        self.currentUsernameValue.setText(self.username)
        
        # Connect buttons to their handlers
        self.changePasswordButton.clicked.connect(self.change_password)
        self.changeUsernameButton.clicked.connect(self.change_username)
        self.deleteAccountButton.clicked.connect(self.delete_account)
        
    def change_password(self):
        old_password = self.oldPasswordInput.text()
        new_password = self.newPasswordInput.text()
        confirm_password = self.confirmPasswordInput.text()
        
        # Validate inputs
        if not old_password or not new_password or not confirm_password:
            QMessageBox.warning(self, "Error", "All password fields are required.")
            return
            
        if new_password != confirm_password:
            QMessageBox.warning(self, "Error", "New passwords do not match.")
            return
            
        # Verify old password
        if not self.db.verify_user(self.username, old_password):
            QMessageBox.warning(self, "Error", "Current password is incorrect.")
            return
            
        # Update password
        if self.db.update_password(self.username, new_password):
            QMessageBox.information(self, "Success", "Password updated successfully.")
            self.oldPasswordInput.clear()
            self.newPasswordInput.clear()
            self.confirmPasswordInput.clear()
        else:
            QMessageBox.warning(self, "Error", "Failed to update password.")
            
    def change_username(self):
        new_username = self.newUsernameInput.text()
        password = self.usernamePasswordInput.text()
        
        # Validate inputs
        if not new_username or not password:
            QMessageBox.warning(self, "Error", "All fields are required.")
            return
            
        # Verify password
        if not self.db.verify_user(self.username, password):
            QMessageBox.warning(self, "Error", "Password is incorrect.")
            return
            
        # Check if new username already exists
        if self.db.username_exists(new_username):
            QMessageBox.warning(self, "Error", "Username already exists.")
            return
            
        # Update username
        if self.db.update_username(self.username, new_username):
            QMessageBox.information(self, "Success", "Username updated successfully.")
            self.username = new_username
            self.currentUsernameValue.setText(new_username)
            self.newUsernameInput.clear()
            self.usernamePasswordInput.clear()
        else:
            QMessageBox.warning(self, "Error", "Failed to update username.")
            
    def delete_account(self):
        password = self.deletePasswordInput.text()
        
        # Validate input
        if not password:
            QMessageBox.warning(self, "Error", "Password is required.")
            return
            
        # Verify password
        if not self.db.verify_user(self.username, password):
            QMessageBox.warning(self, "Error", "Password is incorrect.")
            return
            
        # Confirm deletion
        reply = QMessageBox.question(self, "Confirm Deletion",
                                   "Are you sure you want to delete your account? This action cannot be undone.",
                                   QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        
        if reply == QMessageBox.StandardButton.Yes:
            if self.db.delete_user(self.username):
                QMessageBox.information(self, "Success", "Account deleted successfully.")
                self.close()
                # Signal to main window to return to login
                if hasattr(self.parent(), 'return_to_login'):
                    self.parent().return_to_login()
            else:
                QMessageBox.warning(self, "Error", "Failed to delete account.")