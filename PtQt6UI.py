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

class Ui_Settings(object):
    def setupUi(self, Settings):
        Settings.setObjectName("Settings")
        Settings.resize(1000, 800)
        Settings.setStyleSheet("background-color: #1e1e1e; color: white;")
        self.centralwidget = QtWidgets.QWidget(parent=Settings)
        self.centralwidget.setObjectName("centralwidget")
        
        # Main layout
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout.setSpacing(20)
        self.verticalLayout.setContentsMargins(20, 20, 20, 20)
        
        # Title
        self.titleLabel = QtWidgets.QLabel(self.centralwidget)
        self.titleLabel.setObjectName("titleLabel")
        self.titleLabel.setStyleSheet("font-size: 28px; font-weight: bold; margin: 20px;")
        self.titleLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.verticalLayout.addWidget(self.titleLabel)
        
        # Account Management Group
        self.accountGroup = QtWidgets.QGroupBox("Account Management", self.centralwidget)
        self.accountGroup.setStyleSheet("""
            QGroupBox { 
                color: white; 
                border: 1px solid #3e3e3e; 
                margin-top: 20px;
                padding: 15px;
                font-size: 14px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
        """)
        self.accountLayout = QtWidgets.QVBoxLayout(self.accountGroup)
        self.accountLayout.setSpacing(15)
        
        # Change Password Section
        self.passwordGroup = QtWidgets.QGroupBox("Change Password", self.centralwidget)
        self.passwordGroup.setStyleSheet("""
            QGroupBox { 
                color: white; 
                border: 1px solid #3e3e3e; 
                margin-top: 10px;
                padding: 15px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
            QLineEdit {
                padding: 8px;
                font-size: 13px;
                min-height: 20px;
            }
            QLabel {
                font-size: 13px;
            }
        """)
        self.passwordLayout = QtWidgets.QGridLayout(self.passwordGroup)
        self.passwordLayout.setSpacing(10)
        self.passwordLayout.setContentsMargins(15, 15, 15, 15)
        
        self.oldPasswordLabel = QtWidgets.QLabel("Current Password:")
        self.oldPasswordInput = QtWidgets.QLineEdit()
        self.oldPasswordInput.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.passwordLayout.addWidget(self.oldPasswordLabel, 0, 0)
        self.passwordLayout.addWidget(self.oldPasswordInput, 0, 1)
        
        self.newPasswordLabel = QtWidgets.QLabel("New Password:")
        self.newPasswordInput = QtWidgets.QLineEdit()
        self.newPasswordInput.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.passwordLayout.addWidget(self.newPasswordLabel, 1, 0)
        self.passwordLayout.addWidget(self.newPasswordInput, 1, 1)
        
        self.confirmPasswordLabel = QtWidgets.QLabel("Confirm New Password:")
        self.confirmPasswordInput = QtWidgets.QLineEdit()
        self.confirmPasswordInput.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.passwordLayout.addWidget(self.confirmPasswordLabel, 2, 0)
        self.passwordLayout.addWidget(self.confirmPasswordInput, 2, 1)
        
        self.changePasswordButton = QtWidgets.QPushButton("Change Password")
        self.changePasswordButton.setStyleSheet("""
            QPushButton {
                background-color: #0078D7;
                color: white;
                padding: 5px;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #0063B1;
            }
        """)
        self.passwordLayout.addWidget(self.changePasswordButton, 3, 0, 1, 2)
        
        self.accountLayout.addWidget(self.passwordGroup)
        
        # Change Username Section
        self.usernameGroup = QtWidgets.QGroupBox("Change Username", self.centralwidget)
        self.usernameGroup.setStyleSheet("QGroupBox { color: white; border: 1px solid #3e3e3e; margin-top: 5px; }")
        self.usernameLayout = QtWidgets.QGridLayout(self.usernameGroup)
        
        self.currentUsernameLabel = QtWidgets.QLabel("Current Username:")
        self.currentUsernameValue = QtWidgets.QLabel("")
        self.usernameLayout.addWidget(self.currentUsernameLabel, 0, 0)
        self.usernameLayout.addWidget(self.currentUsernameValue, 0, 1)
        
        self.newUsernameLabel = QtWidgets.QLabel("New Username:")
        self.newUsernameInput = QtWidgets.QLineEdit()
        self.usernameLayout.addWidget(self.newUsernameLabel, 1, 0)
        self.usernameLayout.addWidget(self.newUsernameInput, 1, 1)
        
        self.usernamePasswordLabel = QtWidgets.QLabel("Current Password:")
        self.usernamePasswordInput = QtWidgets.QLineEdit()
        self.usernamePasswordInput.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.usernameLayout.addWidget(self.usernamePasswordLabel, 2, 0)
        self.usernameLayout.addWidget(self.usernamePasswordInput, 2, 1)
        
        self.changeUsernameButton = QtWidgets.QPushButton("Change Username")
        self.changeUsernameButton.setStyleSheet("""
            QPushButton {
                background-color: #0078D7;
                color: white;
                padding: 5px;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #0063B1;
            }
        """)
        self.usernameLayout.addWidget(self.changeUsernameButton, 3, 0, 1, 2)
        
        self.accountLayout.addWidget(self.usernameGroup)
        
        # Delete Account Section
        self.deleteGroup = QtWidgets.QGroupBox("Delete Account", self.centralwidget)
        self.deleteGroup.setStyleSheet("QGroupBox { color: white; border: 1px solid #3e3e3e; margin-top: 5px; }")
        self.deleteLayout = QtWidgets.QGridLayout(self.deleteGroup)
        
        self.deleteWarningLabel = QtWidgets.QLabel("Warning: This action cannot be undone!")
        self.deleteWarningLabel.setStyleSheet("color: #ff4444;")
        self.deleteLayout.addWidget(self.deleteWarningLabel, 0, 0, 1, 2)
        
        self.deletePasswordLabel = QtWidgets.QLabel("Enter Password to Confirm:")
        self.deletePasswordInput = QtWidgets.QLineEdit()
        self.deletePasswordInput.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.deleteLayout.addWidget(self.deletePasswordLabel, 1, 0)
        self.deleteLayout.addWidget(self.deletePasswordInput, 1, 1)
        
        self.deleteAccountButton = QtWidgets.QPushButton("Delete Account")
        self.deleteAccountButton.setStyleSheet("""
            QPushButton {
                background-color: #d83b01;
                color: white;
                padding: 5px;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #b32d00;
            }
        """)
        self.deleteLayout.addWidget(self.deleteAccountButton, 2, 0, 1, 2)
        
        self.accountLayout.addWidget(self.deleteGroup)
        
        self.verticalLayout.addWidget(self.accountGroup)
        
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
        self.closeButton.clicked.connect(Settings.close)
        self.verticalLayout.addWidget(self.closeButton)
        
        Settings.setCentralWidget(self.centralwidget)
        
        self.retranslateUi(Settings)
        QtCore.QMetaObject.connectSlotsByName(Settings)

    def retranslateUi(self, Settings):
        _translate = QtCore.QCoreApplication.translate
        Settings.setWindowTitle(_translate("Settings", "Settings"))
        self.titleLabel.setText(_translate("Settings", "Account Settings"))
        self.passwordGroup.setTitle(_translate("Settings", "Change Password"))
        self.usernameGroup.setTitle(_translate("Settings", "Change Username"))
        self.deleteGroup.setTitle(_translate("Settings", "Delete Account"))
        self.closeButton.setText(_translate("Settings", "Close"))

class Ui_Register(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(401, 362)
        self.Logo = QtWidgets.QLabel(parent=Form)
        self.Logo.setGeometry(QtCore.QRect(50, 10, 301, 101))
        self.Logo.setText("")
        self.Logo.setPixmap(QtGui.QPixmap("Assets/Logos/logo.png"))
        self.Logo.setScaledContents(True)
        self.Logo.setObjectName("Logo")
        self.LUsername = QtWidgets.QLabel(parent=Form)
        self.LUsername.setGeometry(QtCore.QRect(30, 149, 81, 31))
        self.LUsername.setObjectName("LUsername")
        self.LPassword = QtWidgets.QLabel(parent=Form)
        self.LPassword.setGeometry(QtCore.QRect(30, 200, 81, 31))
        self.LPassword.setObjectName("LPassword")
        self.PBRegister = QtWidgets.QPushButton(parent=Form)
        self.PBRegister.setGeometry(QtCore.QRect(160, 320, 81, 31))
        self.PBRegister.setObjectName("PBRegister")
        self.LPassword_2 = QtWidgets.QLabel(parent=Form)
        self.LPassword_2.setGeometry(QtCore.QRect(30, 260, 81, 31))
        self.LPassword_2.setObjectName("LPassword_2")
        self.LPassword_3 = QtWidgets.QLabel(parent=Form)
        self.LPassword_3.setGeometry(QtCore.QRect(30, 240, 81, 41))
        self.LPassword_3.setObjectName("LPassword_3")
        self.LEUsername = QtWidgets.QLineEdit(parent=Form)
        self.LEUsername.setGeometry(QtCore.QRect(112, 149, 261, 31))
        self.LEUsername.setObjectName("LEUsername")
        self.LEPassword = QtWidgets.QLineEdit(parent=Form)
        self.LEPassword.setGeometry(QtCore.QRect(112, 199, 261, 31))
        self.LEPassword.setObjectName("LEPassword")
        self.LEPasswordConfirm = QtWidgets.QLineEdit(parent=Form)
        self.LEPasswordConfirm.setGeometry(QtCore.QRect(112, 250, 261, 31))
        self.LEPasswordConfirm.setObjectName("LEPasswordConfirm")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)
        Form.setTabOrder(self.LEUsername, self.LEPassword)
        Form.setTabOrder(self.LEPassword, self.LEPasswordConfirm)
        Form.setTabOrder(self.LEPasswordConfirm, self.PBRegister)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.LUsername.setText(_translate("Form", "Username:"))
        self.LPassword.setText(_translate("Form", "Password:"))
        self.PBRegister.setText(_translate("Form", "Register"))
        self.LPassword_2.setText(_translate("Form", "Password:"))
        self.LPassword_3.setText(_translate("Form", "Confirm"))

class Ui_MarksView(object):
    def setupUi(self, MarksView):
        MarksView.setObjectName("MarksView")
        MarksView.resize(800, 600)
        MarksView.setStyleSheet("background-color: #1E1E1E; color: white;")
        self.centralwidget = QtWidgets.QWidget(MarksView)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.label.setStyleSheet("font-size: 20px; font-weight: bold;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.verticalLayout.addWidget(self.label)
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

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 755)
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.Logo = QtWidgets.QLabel(parent=self.centralwidget)
        self.Logo.setGeometry(QtCore.QRect(30, 30, 731, 251))
        self.Logo.setText("")
        self.Logo.setPixmap(QtGui.QPixmap("Assets/Logos/logo.png"))
        self.Logo.setScaledContents(True)
        self.Logo.setObjectName("Logo")
        self.PBPractice = QtWidgets.QPushButton(parent=self.centralwidget)
        self.PBPractice.setGeometry(QtCore.QRect(30, 320, 341, 121))
        self.PBPractice.setObjectName("PBPractice")
        self.PBStatistics = QtWidgets.QPushButton(parent=self.centralwidget)
        self.PBStatistics.setGeometry(QtCore.QRect(410, 320, 351, 121))
        self.PBStatistics.setObjectName("PBStatistics")
        self.PBExamMode = QtWidgets.QPushButton(parent=self.centralwidget)
        self.PBExamMode.setGeometry(QtCore.QRect(30, 460, 731, 121))
        self.PBExamMode.setObjectName("PBExamMode")
        self.PBSettings = QtWidgets.QPushButton(parent=self.centralwidget)
        self.PBSettings.setGeometry(QtCore.QRect(30, 600, 731, 51))
        self.PBSettings.setObjectName("PBSettings")
        self.PBQuit = QtWidgets.QPushButton(parent=self.centralwidget)
        self.PBQuit.setGeometry(QtCore.QRect(30, 670, 731, 51))
        self.PBQuit.setObjectName("PBQuit")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(parent=MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.PBPractice.setText(_translate("MainWindow", "Practice"))
        self.PBStatistics.setText(_translate("MainWindow", "Statistics"))
        self.PBExamMode.setText(_translate("MainWindow", "Exam Mode"))
        self.PBSettings.setText(_translate("MainWindow", "Settings"))
        self.PBQuit.setText(_translate("MainWindow", "Quit"))

class Ui_Login(object):
    def setupUi(self, Login):
        Login.setObjectName("Login")
        Login.resize(401, 300)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("Assets/Logos/logosmall.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        Login.setWindowIcon(icon)
        self.Logo = QtWidgets.QLabel(parent=Login)
        self.Logo.setGeometry(QtCore.QRect(50, 10, 301, 101))
        self.Logo.setText("")
        self.Logo.setPixmap(QtGui.QPixmap("Assets/Logos/logo.png"))
        self.Logo.setScaledContents(True)
        self.Logo.setObjectName("Logo")
        self.LUsername = QtWidgets.QLabel(parent=Login)
        self.LUsername.setGeometry(QtCore.QRect(30, 149, 81, 31))
        self.LUsername.setObjectName("LUsername")
        self.LPassword = QtWidgets.QLabel(parent=Login)
        self.LPassword.setGeometry(QtCore.QRect(30, 200, 81, 31))
        self.LPassword.setObjectName("LPassword")
        self.PBRegister = QtWidgets.QPushButton(parent=Login)
        self.PBRegister.setGeometry(QtCore.QRect(50, 252, 111, 31))
        self.PBRegister.setObjectName("PBRegister")
        self.PBLogin = QtWidgets.QPushButton(parent=Login)
        self.PBLogin.setGeometry(QtCore.QRect(240, 252, 111, 31))
        self.PBLogin.setObjectName("PBLogin")
        self.LEPassword = QtWidgets.QLineEdit(parent=Login)
        self.LEPassword.setGeometry(QtCore.QRect(110, 200, 261, 31))
        self.LEPassword.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.LEPassword.setObjectName("LEPassword")
        self.LEUsername = QtWidgets.QLineEdit(parent=Login)
        self.LEUsername.setGeometry(QtCore.QRect(110, 150, 261, 31))
        self.LEUsername.setObjectName("LEUsername")

        self.retranslateUi(Login)
        QtCore.QMetaObject.connectSlotsByName(Login)
        Login.setTabOrder(self.LEUsername, self.LEPassword)
        Login.setTabOrder(self.LEPassword, self.PBRegister)
        Login.setTabOrder(self.PBRegister, self.PBLogin)

    def retranslateUi(self, Login):
        _translate = QtCore.QCoreApplication.translate
        Login.setWindowTitle(_translate("Login", "Login"))
        self.LUsername.setText(_translate("Login", "Username:"))
        self.LPassword.setText(_translate("Login", "Password:"))
        self.PBRegister.setText(_translate("Login", "Register"))
        self.PBLogin.setText(_translate("Login", "Login")) 