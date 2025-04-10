from PyQt6 import QtCore, QtGui, QtWidgets

class Ui_MarksView(object):
    def setupUi(self, MarksView):
        MarksView.setObjectName("MarksView")
        MarksView.resize(800, 600)
        MarksView.setStyleSheet("background-color: #1E1E1E; color: white;")
        
        self.centralwidget = QtWidgets.QWidget(MarksView)
        self.centralwidget.setObjectName("centralwidget")
        
        # Main layout
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        
        # Title
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.label.setStyleSheet("font-size: 20px; font-weight: bold;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.verticalLayout.addWidget(self.label)
        
        # Filter layout
        self.filterLayout = QtWidgets.QHBoxLayout()
        self.filterLayout.setObjectName("filterLayout")
        
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setObjectName("label_2")
        self.filterLayout.addWidget(self.label_2)
        
        self.CBFilter = QtWidgets.QComboBox(self.centralwidget)
        self.CBFilter.setObjectName("CBFilter")
        self.CBFilter.setStyleSheet("background-color: #2D2D2D; color: white;")
        self.filterLayout.addWidget(self.CBFilter)
        
        self.PBRefresh = QtWidgets.QPushButton(self.centralwidget)
        self.PBRefresh.setObjectName("PBRefresh")
        self.PBRefresh.setStyleSheet("background-color: #0078D7; color: white; padding: 5px;")
        self.filterLayout.addWidget(self.PBRefresh)
        
        self.verticalLayout.addLayout(self.filterLayout)
        
        # Table widget
        self.TWMarks = QtWidgets.QTableWidget(self.centralwidget)
        self.TWMarks.setObjectName("TWMarks")
        self.TWMarks.setStyleSheet("""
            QTableWidget {
                background-color: #2D2D2D;
                color: white;
                gridline-color: #3D3D3D;
            }
            QHeaderView::section {
                background-color: #0078D7;
                color: white;
                padding: 5px;
            }
        """)
        self.TWMarks.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.TWMarks.setAlternatingRowColors(True)
        self.TWMarks.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
        self.verticalLayout.addWidget(self.TWMarks)
        
        # Close button
        self.PBClose = QtWidgets.QPushButton(self.centralwidget)
        self.PBClose.setObjectName("PBClose")
        self.PBClose.setStyleSheet("background-color: #0078D7; color: white; padding: 5px;")
        self.verticalLayout.addWidget(self.PBClose)
        
        MarksView.setCentralWidget(self.centralwidget)
        
        self.retranslateUi(MarksView)
        QtCore.QMetaObject.connectSlotsByName(MarksView)
        
    def retranslateUi(self, MarksView):
        _translate = QtCore.QCoreApplication.translate
        MarksView.setWindowTitle(_translate("MarksView", "View Marks"))
        self.label.setText(_translate("MarksView", "Global Marks View"))
        self.label_2.setText(_translate("MarksView", "Filter by Paper:"))
        self.PBRefresh.setText(_translate("MarksView", "Refresh"))
        self.PBClose.setText(_translate("MarksView", "Close")) 