from PyQt6 import QtCore, QtGui, QtWidgets

class Ui_StatisticsWindow(object):
    def setupUi(self, StatisticsWindow):
        StatisticsWindow.setObjectName("StatisticsWindow")
        StatisticsWindow.resize(800, 600)
        StatisticsWindow.setStyleSheet("background-color: #1e1e1e; color: white;")
        
        self.centralwidget = QtWidgets.QWidget(StatisticsWindow)
        self.centralwidget.setObjectName("centralwidget")
        
        # Main layout
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        
        # Title
        self.titleLabel = QtWidgets.QLabel(self.centralwidget)
        self.titleLabel.setObjectName("titleLabel")
        self.titleLabel.setStyleSheet("font-size: 24px; font-weight: bold; margin: 10px;")
        self.titleLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.verticalLayout.addWidget(self.titleLabel)
        
        # Overall Statistics
        self.overallGroup = QtWidgets.QGroupBox("Overall Statistics", self.centralwidget)
        self.overallGroup.setStyleSheet("QGroupBox { color: white; border: 1px solid #3e3e3e; margin-top: 10px; }")
        self.overallLayout = QtWidgets.QGridLayout(self.overallGroup)
        
        self.totalQuestionsLabel = QtWidgets.QLabel("Total Questions Attempted:")
        self.totalQuestionsValue = QtWidgets.QLabel("0")
        self.overallLayout.addWidget(self.totalQuestionsLabel, 0, 0)
        self.overallLayout.addWidget(self.totalQuestionsValue, 0, 1)
        
        self.correctQuestionsLabel = QtWidgets.QLabel("Correct Questions:")
        self.correctQuestionsValue = QtWidgets.QLabel("0")
        self.overallLayout.addWidget(self.correctQuestionsLabel, 1, 0)
        self.overallLayout.addWidget(self.correctQuestionsValue, 1, 1)
        
        self.accuracyLabel = QtWidgets.QLabel("Overall Accuracy:")
        self.accuracyValue = QtWidgets.QLabel("0%")
        self.overallLayout.addWidget(self.accuracyLabel, 2, 0)
        self.overallLayout.addWidget(self.accuracyValue, 2, 1)
        
        self.averageTimeLabel = QtWidgets.QLabel("Average Time per Question:")
        self.averageTimeValue = QtWidgets.QLabel("0 seconds")
        self.overallLayout.addWidget(self.averageTimeLabel, 3, 0)
        self.overallLayout.addWidget(self.averageTimeValue, 3, 1)
        
        self.verticalLayout.addWidget(self.overallGroup)
        
        # Topic Statistics
        self.topicGroup = QtWidgets.QGroupBox("Topic Statistics", self.centralwidget)
        self.topicGroup.setStyleSheet("QGroupBox { color: white; border: 1px solid #3e3e3e; margin-top: 10px; }")
        self.topicLayout = QtWidgets.QVBoxLayout(self.topicGroup)
        
        # Scroll area for topic statistics
        self.scrollArea = QtWidgets.QScrollArea()
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setStyleSheet("border: none;")
        
        self.scrollWidget = QtWidgets.QWidget()
        self.scrollLayout = QtWidgets.QVBoxLayout(self.scrollWidget)
        
        self.scrollArea.setWidget(self.scrollWidget)
        self.topicLayout.addWidget(self.scrollArea)
        
        self.verticalLayout.addWidget(self.topicGroup)
        
        # Close button
        self.closeButton = QtWidgets.QPushButton("Close", self.centralwidget)
        self.closeButton.setStyleSheet("""
            QPushButton {
                background-color: #3e3e3e;
                border: none;
                padding: 8px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #4e4e4e;
            }
        """)
        self.closeButton.clicked.connect(StatisticsWindow.close)
        self.verticalLayout.addWidget(self.closeButton)
        
        StatisticsWindow.setCentralWidget(self.centralwidget)
        
        self.retranslateUi(StatisticsWindow)
        QtCore.QMetaObject.connectSlotsByName(StatisticsWindow)

    def retranslateUi(self, StatisticsWindow):
        _translate = QtCore.QCoreApplication.translate
        StatisticsWindow.setWindowTitle(_translate("StatisticsWindow", "User Statistics"))
        self.titleLabel.setText(_translate("StatisticsWindow", "Your Statistics")) 