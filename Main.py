from PyQt6.QtWidgets import QApplication, QMainWindow
import os
from MainMenu_ui import Ui_MainWindow
from Login import LoginScreen
from Settings import SettingsWindow
from ExamMode import ExamMode
from MarksView import MarksViewWindow

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

    def quit_application(self):
        QApplication.quit()

    def settings(self):
        self.settings_window = SettingsWindow()
        self.settings_window.show()

    def exam_mode(self):
        self.exam_window = ExamMode(self.username)
        self.close()  # Close the main window
        selected_paper = self.exam_window.run()
        if selected_paper:
            print(f"Selected paper: {selected_paper}")
            
    def view_marks(self):
        self.marks_window = MarksViewWindow()
        self.marks_window.show()

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



