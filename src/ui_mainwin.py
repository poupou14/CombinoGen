# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwin.ui'
#
# Created: Tue Dec 20 22:28:12 2016
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_MainWin(object):
    def setupUi(self, MainWin):
        MainWin.setObjectName("MainWin")
        MainWin.resize(741, 472)
        self.centralWidget = QtGui.QWidget(MainWin)
        self.centralWidget.setObjectName("centralWidget")
        self.gridLayout = QtGui.QGridLayout(self.centralWidget)
        self.gridLayout.setObjectName("gridLayout")
        self.MainPanel = QtGui.QTabWidget(self.centralWidget)
        self.MainPanel.setObjectName("MainPanel")
        self.Config = QtGui.QWidget()
        self.Config.setObjectName("Config")
        self.gridLayout_2 = QtGui.QGridLayout(self.Config)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.pbUpdate = QtGui.QPushButton(self.Config)
        self.pbUpdate.setObjectName("pbUpdate")
        self.gridLayout_2.addWidget(self.pbUpdate, 0, 0, 1, 1)
        self.labelBook = QtGui.QLabel(self.Config)
        self.labelBook.setObjectName("labelBook")
        self.gridLayout_2.addWidget(self.labelBook, 1, 0, 1, 1)
        self.comboBookBox = QtGui.QComboBox(self.Config)
        self.comboBookBox.setObjectName("comboBookBox")
        self.gridLayout_2.addWidget(self.comboBookBox, 1, 1, 1, 1)
        self.labelGrid = QtGui.QLabel(self.Config)
        self.labelGrid.setObjectName("labelGrid")
        self.gridLayout_2.addWidget(self.labelGrid, 2, 0, 1, 1)
        self.comboGridBox = QtGui.QComboBox(self.Config)
        self.comboGridBox.setObjectName("comboGridBox")
        self.gridLayout_2.addWidget(self.comboGridBox, 2, 1, 1, 1)
        self.labelOutput = QtGui.QLabel(self.Config)
        self.labelOutput.setObjectName("labelOutput")
        self.gridLayout_2.addWidget(self.labelOutput, 3, 0, 1, 1)
        self.lineEdit = QtGui.QLineEdit(self.Config)
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout_2.addWidget(self.lineEdit, 3, 1, 1, 1)
        self.pb1Browse = QtGui.QPushButton(self.Config)
        self.pb1Browse.setObjectName("pb1Browse")
        self.gridLayout_2.addWidget(self.pb1Browse, 3, 2, 1, 1)
        self.pbGenerate = QtGui.QPushButton(self.Config)
        self.pbGenerate.setObjectName("pbGenerate")
        self.gridLayout_2.addWidget(self.pbGenerate, 4, 0, 1, 1)
        self.MainPanel.addTab(self.Config, "")
        self.Distrib = QtGui.QWidget()
        self.Distrib.setObjectName("Distrib")
        self.gridLayout_3 = QtGui.QGridLayout(self.Distrib)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.label_4 = QtGui.QLabel(self.Distrib)
        self.label_4.setObjectName("label_4")
        self.gridLayout_3.addWidget(self.label_4, 0, 0, 1, 1)
        self.label_5 = QtGui.QLabel(self.Distrib)
        self.label_5.setObjectName("label_5")
        self.gridLayout_3.addWidget(self.label_5, 0, 1, 1, 1)
        spacerItem = QtGui.QSpacerItem(68, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem, 0, 2, 1, 1)
        self.label_6 = QtGui.QLabel(self.Distrib)
        self.label_6.setObjectName("label_6")
        self.gridLayout_3.addWidget(self.label_6, 0, 3, 1, 1)
        self.label_7 = QtGui.QLabel(self.Distrib)
        self.label_7.setObjectName("label_7")
        self.gridLayout_3.addWidget(self.label_7, 0, 5, 1, 1)
        self.label_8 = QtGui.QLabel(self.Distrib)
        self.label_8.setObjectName("label_8")
        self.gridLayout_3.addWidget(self.label_8, 0, 7, 1, 1)
        self.label_9 = QtGui.QLabel(self.Distrib)
        self.label_9.setObjectName("label_9")
        self.gridLayout_3.addWidget(self.label_9, 1, 0, 1, 1)
        self.label_10 = QtGui.QLabel(self.Distrib)
        self.label_10.setObjectName("label_10")
        self.gridLayout_3.addWidget(self.label_10, 1, 1, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(68, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem1, 1, 2, 1, 1)
        self.lineEdit_2 = QtGui.QLineEdit(self.Distrib)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.gridLayout_3.addWidget(self.lineEdit_2, 1, 3, 1, 1)
        self.label_11 = QtGui.QLabel(self.Distrib)
        self.label_11.setObjectName("label_11")
        self.gridLayout_3.addWidget(self.label_11, 1, 4, 1, 1)
        self.lineEdit_3 = QtGui.QLineEdit(self.Distrib)
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.gridLayout_3.addWidget(self.lineEdit_3, 1, 5, 1, 1)
        self.label_12 = QtGui.QLabel(self.Distrib)
        self.label_12.setObjectName("label_12")
        self.gridLayout_3.addWidget(self.label_12, 1, 6, 1, 1)
        self.lineEdit_4 = QtGui.QLineEdit(self.Distrib)
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.gridLayout_3.addWidget(self.lineEdit_4, 1, 7, 1, 1)
        self.label_13 = QtGui.QLabel(self.Distrib)
        self.label_13.setObjectName("label_13")
        self.gridLayout_3.addWidget(self.label_13, 1, 8, 1, 1)
        spacerItem2 = QtGui.QSpacerItem(20, 233, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_3.addItem(spacerItem2, 2, 2, 1, 1)
        self.pbGenerateOdds = QtGui.QPushButton(self.Distrib)
        self.pbGenerateOdds.setObjectName("pbGenerateOdds")
        self.gridLayout_3.addWidget(self.pbGenerateOdds, 3, 0, 1, 1)
        self.pbImport = QtGui.QPushButton(self.Distrib)
        self.pbImport.setObjectName("pbImport")
        self.gridLayout_3.addWidget(self.pbImport, 3, 7, 1, 2)
        self.MainPanel.addTab(self.Distrib, "")
        self.Odds = QtGui.QWidget()
        self.Odds.setObjectName("Odds")
        self.gridLayout_4 = QtGui.QGridLayout(self.Odds)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.label_15 = QtGui.QLabel(self.Odds)
        self.label_15.setObjectName("label_15")
        self.gridLayout_4.addWidget(self.label_15, 0, 0, 1, 1)
        self.label_19 = QtGui.QLabel(self.Odds)
        self.label_19.setObjectName("label_19")
        self.gridLayout_4.addWidget(self.label_19, 0, 1, 1, 1)
        spacerItem3 = QtGui.QSpacerItem(124, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_4.addItem(spacerItem3, 0, 2, 1, 1)
        self.label_22 = QtGui.QLabel(self.Odds)
        self.label_22.setObjectName("label_22")
        self.gridLayout_4.addWidget(self.label_22, 0, 3, 1, 1)
        self.label_20 = QtGui.QLabel(self.Odds)
        self.label_20.setObjectName("label_20")
        self.gridLayout_4.addWidget(self.label_20, 0, 4, 1, 1)
        self.label_18 = QtGui.QLabel(self.Odds)
        self.label_18.setObjectName("label_18")
        self.gridLayout_4.addWidget(self.label_18, 0, 5, 1, 1)
        self.label_16 = QtGui.QLabel(self.Odds)
        self.label_16.setObjectName("label_16")
        self.gridLayout_4.addWidget(self.label_16, 1, 0, 1, 1)
        self.label_17 = QtGui.QLabel(self.Odds)
        self.label_17.setObjectName("label_17")
        self.gridLayout_4.addWidget(self.label_17, 1, 1, 1, 1)
        spacerItem4 = QtGui.QSpacerItem(124, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_4.addItem(spacerItem4, 1, 2, 1, 1)
        self.lineEdit_7 = QtGui.QLineEdit(self.Odds)
        self.lineEdit_7.setObjectName("lineEdit_7")
        self.gridLayout_4.addWidget(self.lineEdit_7, 1, 3, 1, 1)
        self.lineEdit_5 = QtGui.QLineEdit(self.Odds)
        self.lineEdit_5.setObjectName("lineEdit_5")
        self.gridLayout_4.addWidget(self.lineEdit_5, 1, 4, 1, 1)
        self.lineEdit_6 = QtGui.QLineEdit(self.Odds)
        self.lineEdit_6.setObjectName("lineEdit_6")
        self.gridLayout_4.addWidget(self.lineEdit_6, 1, 5, 1, 1)
        spacerItem5 = QtGui.QSpacerItem(20, 233, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_4.addItem(spacerItem5, 2, 2, 1, 1)
        self.pbGenerateGrid = QtGui.QPushButton(self.Odds)
        self.pbGenerateGrid.setObjectName("pbGenerateGrid")
        self.gridLayout_4.addWidget(self.pbGenerateGrid, 3, 0, 1, 1)
        self.MainPanel.addTab(self.Odds, "")
        self.gridLayout.addWidget(self.MainPanel, 0, 0, 1, 1)
        self.pbQuit = QtGui.QPushButton(self.centralWidget)
        self.pbQuit.setObjectName("pbQuit")
        self.gridLayout.addWidget(self.pbQuit, 1, 0, 1, 1)
        MainWin.setCentralWidget(self.centralWidget)
        self.menuBar = QtGui.QMenuBar(MainWin)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 741, 19))
        self.menuBar.setObjectName("menuBar")
        MainWin.setMenuBar(self.menuBar)
        self.mainToolBar = QtGui.QToolBar(MainWin)
        self.mainToolBar.setObjectName("mainToolBar")
        MainWin.addToolBar(QtCore.Qt.TopToolBarArea, self.mainToolBar)
        self.statusBar = QtGui.QStatusBar(MainWin)
        self.statusBar.setObjectName("statusBar")
        MainWin.setStatusBar(self.statusBar)
        self.toolBar = QtGui.QToolBar(MainWin)
        self.toolBar.setObjectName("toolBar")
        MainWin.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)

        self.retranslateUi(MainWin)
        self.MainPanel.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWin)

    def retranslateUi(self, MainWin):
        MainWin.setWindowTitle(QtGui.QApplication.translate("MainWin", "MainWin", None, QtGui.QApplication.UnicodeUTF8))
        self.pbUpdate.setText(QtGui.QApplication.translate("MainWin", "Update", None, QtGui.QApplication.UnicodeUTF8))
        self.labelBook.setText(QtGui.QApplication.translate("MainWin", "Book :", None, QtGui.QApplication.UnicodeUTF8))
        self.labelGrid.setText(QtGui.QApplication.translate("MainWin", "Grid :", None, QtGui.QApplication.UnicodeUTF8))
        self.labelOutput.setText(QtGui.QApplication.translate("MainWin", "Output dir :", None, QtGui.QApplication.UnicodeUTF8))
        self.pb1Browse.setText(QtGui.QApplication.translate("MainWin", "Browse", None, QtGui.QApplication.UnicodeUTF8))
        self.pbGenerate.setText(QtGui.QApplication.translate("MainWin", "Generate input File", None, QtGui.QApplication.UnicodeUTF8))
        self.MainPanel.setTabText(self.MainPanel.indexOf(self.Config), QtGui.QApplication.translate("MainWin", "Config", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("MainWin", "Team 1", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("MainWin", "Team 2", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setText(QtGui.QApplication.translate("MainWin", "1", None, QtGui.QApplication.UnicodeUTF8))
        self.label_7.setText(QtGui.QApplication.translate("MainWin", "N", None, QtGui.QApplication.UnicodeUTF8))
        self.label_8.setText(QtGui.QApplication.translate("MainWin", "2", None, QtGui.QApplication.UnicodeUTF8))
        self.label_9.setText(QtGui.QApplication.translate("MainWin", "SM Caen", None, QtGui.QApplication.UnicodeUTF8))
        self.label_10.setText(QtGui.QApplication.translate("MainWin", "SCO Angers", None, QtGui.QApplication.UnicodeUTF8))
        self.label_11.setText(QtGui.QApplication.translate("MainWin", "%", None, QtGui.QApplication.UnicodeUTF8))
        self.label_12.setText(QtGui.QApplication.translate("MainWin", "%", None, QtGui.QApplication.UnicodeUTF8))
        self.label_13.setText(QtGui.QApplication.translate("MainWin", "%", None, QtGui.QApplication.UnicodeUTF8))
        self.pbGenerateOdds.setText(QtGui.QApplication.translate("MainWin", "Generate Odds", None, QtGui.QApplication.UnicodeUTF8))
        self.pbImport.setText(QtGui.QApplication.translate("MainWin", "Import Input File", None, QtGui.QApplication.UnicodeUTF8))
        self.MainPanel.setTabText(self.MainPanel.indexOf(self.Distrib), QtGui.QApplication.translate("MainWin", "Distrib", None, QtGui.QApplication.UnicodeUTF8))
        self.label_15.setText(QtGui.QApplication.translate("MainWin", "Team 1", None, QtGui.QApplication.UnicodeUTF8))
        self.label_19.setText(QtGui.QApplication.translate("MainWin", "Team 2", None, QtGui.QApplication.UnicodeUTF8))
        self.label_22.setText(QtGui.QApplication.translate("MainWin", "1", None, QtGui.QApplication.UnicodeUTF8))
        self.label_20.setText(QtGui.QApplication.translate("MainWin", "N", None, QtGui.QApplication.UnicodeUTF8))
        self.label_18.setText(QtGui.QApplication.translate("MainWin", "2", None, QtGui.QApplication.UnicodeUTF8))
        self.label_16.setText(QtGui.QApplication.translate("MainWin", "SM Caen", None, QtGui.QApplication.UnicodeUTF8))
        self.label_17.setText(QtGui.QApplication.translate("MainWin", "SCO Angers", None, QtGui.QApplication.UnicodeUTF8))
        self.pbGenerateGrid.setText(QtGui.QApplication.translate("MainWin", "Generate Grid", None, QtGui.QApplication.UnicodeUTF8))
        self.MainPanel.setTabText(self.MainPanel.indexOf(self.Odds), QtGui.QApplication.translate("MainWin", "Odds", None, QtGui.QApplication.UnicodeUTF8))
        self.pbQuit.setText(QtGui.QApplication.translate("MainWin", "Quit", None, QtGui.QApplication.UnicodeUTF8))
        self.toolBar.setWindowTitle(QtGui.QApplication.translate("MainWin", "toolBar", None, QtGui.QApplication.UnicodeUTF8))
