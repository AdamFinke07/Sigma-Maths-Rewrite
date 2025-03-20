from PyQt6.QtWidgets import QApplication, QMainWindow
import os
from MainMenu_ui import Ui_MainWindow
from Login import LoginScreen
from Settings import SettingsWindow

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self) 
        self.initUI()
        
    def initUI(self):
        self.PBQuit.clicked.connect(self.quit_application)
        self.PBSettings.clicked.connect(self.settings)

    def quit_application(self):
        QApplication.quit()

    def settings(self):
        self.settings_window = SettingsWindow()
        self.settings_window.show()
        


if __name__ == "__main__":
    app = QApplication([])
    main_window = None

    def show_main_window():
        global main_window
        login_screen.close()   
        main_window = MainWindow()  # CLOSES LOGIN SCREEN AND OPENS MAIN WINDOW I THINK???
        main_window.show()

    # THIS CALLBACK WORKS DO NOT TOUCH.
    login_screen = LoginScreen(show_main_callback=show_main_window)
    login_screen.show()

    # ACTUALLY RUN THE PROGRAM OR SOMETHING.
    exit_code = app.exec()
    os._exit(exit_code)



