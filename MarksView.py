from PyQt6.QtWidgets import QMainWindow, QTableWidgetItem, QMessageBox
from PyQt6.QtCore import Qt
from MarksView_ui import Ui_MarksView
from Database import Database

class MarksViewWindow(QMainWindow, Ui_MarksView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.db = Database()
        self.init_ui()
        
    def init_ui(self):
        self.PBClose.clicked.connect(self.close)
        self.PBRefresh.clicked.connect(self.refresh_marks)
        self.CBFilter.currentTextChanged.connect(self.filter_marks)
        self.load_papers()
        self.refresh_marks()
        
    def load_papers(self):
        # Get unique papers from the database
        marks = self.db.get_all_users_marks()
        papers = set(mark[1] for mark in marks)
        self.CBFilter.addItem("All Papers")
        for paper in sorted(papers):
            self.CBFilter.addItem(paper)
            
    def refresh_marks(self):
        # Clear existing data
        self.TWMarks.setRowCount(0)
        
        # Get marks based on filter
        selected_paper = self.CBFilter.currentText()
        if selected_paper == "All Papers":
            marks = self.db.get_all_users_summary()
        else:
            marks = self.db.get_all_users_marks(selected_paper)
            
        # Set up table headers
        if selected_paper == "All Papers":
            self.TWMarks.setColumnCount(5)
            self.TWMarks.setHorizontalHeaderLabels(["Username", "Paper", "Total Marks", "Possible Marks", "Percentage"])
        else:
            self.TWMarks.setColumnCount(5)
            self.TWMarks.setHorizontalHeaderLabels(["Username", "Question", "Marks Earned", "Total Marks", "Percentage"])
            
        # Add data to table
        for row, mark in enumerate(marks):
            self.TWMarks.insertRow(row)
            
            if selected_paper == "All Papers":
                username, paper, earned, total, count = mark
                percentage = round((earned/total)*100, 1) if total > 0 else 0
                items = [
                    QTableWidgetItem(username),
                    QTableWidgetItem(paper),
                    QTableWidgetItem(str(earned)),
                    QTableWidgetItem(str(total)),
                    QTableWidgetItem(f"{percentage}%")
                ]
            else:
                username, paper, question, earned, total, timestamp = mark
                percentage = round((earned/total)*100, 1) if total > 0 else 0
                items = [
                    QTableWidgetItem(username),
                    QTableWidgetItem(question),
                    QTableWidgetItem(str(earned)),
                    QTableWidgetItem(str(total)),
                    QTableWidgetItem(f"{percentage}%")
                ]
                
            for col, item in enumerate(items):
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.TWMarks.setItem(row, col, item)
                
        # Resize columns to fit content
        self.TWMarks.resizeColumnsToContents()
        
    def filter_marks(self):
        self.refresh_marks() 