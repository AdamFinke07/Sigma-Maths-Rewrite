# Form implementation generated from reading ui file 'd:\Storage\Desktop\OneDrive_2025-02-28\NEA Sigma\Settings.ui'
#
# Created by: PyQt6 UI code generator 6.7.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_Settings(object):
    def setupUi(self, Settings):
        Settings.setObjectName("Settings")
        Settings.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(parent=Settings)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(parent=self.centralwidget)
        self.label.setGeometry(QtCore.QRect(30, 20, 751, 521))
        font = QtGui.QFont()
        font.setPointSize(72)
        self.label.setFont(font)
        self.label.setObjectName("label")
        Settings.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=Settings)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        self.menuSettings = QtWidgets.QMenu(parent=self.menubar)
        self.menuSettings.setObjectName("menuSettings")
        Settings.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=Settings)
        self.statusbar.setObjectName("statusbar")
        Settings.setStatusBar(self.statusbar)
        self.menubar.addAction(self.menuSettings.menuAction())

        self.retranslateUi(Settings)
        QtCore.QMetaObject.connectSlotsByName(Settings)

    def retranslateUi(self, Settings):
        _translate = QtCore.QCoreApplication.translate
        Settings.setWindowTitle(_translate("Settings", "MainWindow"))
        self.label.setText(_translate("Settings", "work in progress"))
        self.menuSettings.setTitle(_translate("Settings", "Settings"))
