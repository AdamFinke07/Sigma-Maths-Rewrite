from PyQt6.QtWidgets import QMainWindow, QGroupBox, QGridLayout, QLabel
from Statistics_ui import Ui_StatisticsWindow
from Database import Database

class StatisticsWindow(QMainWindow, Ui_StatisticsWindow):
    def __init__(self, username):
        super().__init__()
        self.setupUi(self)
        self.username = username
        self.db = Database()
        self.load_statistics()

    def load_statistics(self):
        # Load overall statistics
        overall_stats = self.db.get_user_overall_statistics(self.username)
        
        # Update overall statistics labels
        self.totalQuestionsValue.setText(str(overall_stats['total_questions']))
        self.correctQuestionsValue.setText(str(overall_stats['correct_questions']))
        self.accuracyValue.setText(f"{overall_stats['overall_accuracy']:.1f}%")
        self.averageTimeValue.setText(f"{overall_stats['average_time_per_question']:.1f} seconds")
        
        # Load topic statistics
        topic_stats = self.db.get_user_statistics(self.username)
        
        # Clear existing topic widgets
        for i in reversed(range(self.scrollLayout.count())): 
            self.scrollLayout.itemAt(i).widget().setParent(None)
        
        # Add topic statistics
        for stat in topic_stats:
            topic_group = self.create_topic_group(stat)
            self.scrollLayout.addWidget(topic_group)
        
        # Add stretch at the end
        self.scrollLayout.addStretch()

    def create_topic_group(self, stat):
        group = QGroupBox(stat['topic'])
        group.setStyleSheet("""
            QGroupBox {
                color: white;
                border: 1px solid #3e3e3e;
                margin-top: 5px;
                padding-top: 10px;
            }
        """)
        
        layout = QGridLayout()
        
        # Total Questions
        total_label = QLabel("Total Questions:")
        total_value = QLabel(str(stat['total_questions']))
        layout.addWidget(total_label, 0, 0)
        layout.addWidget(total_value, 0, 1)
        
        # Correct Questions
        correct_label = QLabel("Correct Questions:")
        correct_value = QLabel(str(stat['correct_questions']))
        layout.addWidget(correct_label, 1, 0)
        layout.addWidget(correct_value, 1, 1)
        
        # Accuracy
        accuracy_label = QLabel("Accuracy:")
        accuracy_value = QLabel(f"{stat['accuracy']:.1f}%")
        layout.addWidget(accuracy_label, 2, 0)
        layout.addWidget(accuracy_value, 2, 1)
        
        # Marks
        marks_label = QLabel("Mark Percentage:")
        marks_value = QLabel(f"{stat['mark_percentage']:.1f}%")
        layout.addWidget(marks_label, 3, 0)
        layout.addWidget(marks_value, 3, 1)
        
        # Average Time
        time_label = QLabel("Average Time:")
        time_value = QLabel(f"{stat['average_time_per_question']:.1f} seconds")
        layout.addWidget(time_label, 4, 0)
        layout.addWidget(time_value, 4, 1)
        
        group.setLayout(layout)
        return group 