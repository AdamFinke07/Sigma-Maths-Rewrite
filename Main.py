from PyQt6.QtWidgets import QApplication, QMainWindow
import os
from MainMenu_ui import Ui_MainWindow
from Login import LoginScreen
from Settings import SettingsWindow
from ExamMode import ExamMode
from MarksView import MarksViewWindow
from Statistics import StatisticsWindow

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, username):
        super().__init__()
        self.setupUi(self) 
        self.username = username
        self.initUI()
        
    def initUI(self):
        self.PBQuit.clicked.connect(self.quit_application)
        self.PBSettings.clicked.connect(self.settings)
        self.PBExamMode.clicked.connect(self.exam_mode)
        self.PBViewMarks.clicked.connect(self.view_marks)
        self.PBStatistics.clicked.connect(self.show_statistics)

    def quit_application(self):
        QApplication.quit()

    def settings(self):
        self.settings_window = SettingsWindow()
        self.settings_window.show()

    def exam_mode(self):
        self.hide()  # Hide the main window instead of closing it
        self.exam_window = ExamMode(self.username)
        result = self.exam_window.run()
        
        if result == 'back_to_main':
            self.show()  # Show the main window again
        elif result == 'closed':
            self.show()  # Show the main window if exam mode was closed
            
    def view_marks(self):
        self.marks_window = MarksViewWindow()
        self.marks_window.show()

    def show_statistics(self):
        self.statistics_window = StatisticsWindow(self.username)
        self.statistics_window.show()

if __name__ == "__main__":
    app = QApplication([])
    main_window = None

    def show_main_window():
        global main_window
        login_screen.close()   
        main_window = MainWindow(login_screen.LEUsername.text())  # Pass username to MainWindow
        main_window.show()

    # THIS CALLBACK WORKS DO NOT TOUCH.
    login_screen = LoginScreen(show_main_callback=show_main_window)
    login_screen.show()

    # ACTUALLY RUN THE PROGRAM OR SOMETHING.
    exit_code = app.exec()
    os._exit(exit_code)



