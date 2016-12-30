import os, sys
from PySide import QtCore, QtGui
from PySide.QtGui import QGridLayout, QLineEdit, QLabel
from PySide.QtCore import Signal, Slot, QDateTime
from PySide.QtNetwork import QNetworkReply
from CombinoNetworkManager import CombinoNetworkManager
from CombinoSource import CombinoSource
from CombinoEngine import CombinoEngine
from ui_mainwin import Ui_MainWin
from readGridHandler import readGridHandler
from readWinamax7Handler import readWinamax7Handler
from readWinamax12Handler import readWinamax12Handler
from GridRequestor import GridRequestor, DistribPageGeneratedSignal

height_g = 600
width_g = 800
actions = ('CombinoGenBook', 'CombinoGenDistrib', 'CombinoGenOdds','CombinoGenResult')




class CombinoGUI(QtGui.QMainWindow):
    stopGenSig = Signal()

    def __init__(self, parent_l=None):
        QtGui.QMainWindow.__init__(self, parent_l)
        self.resize(width_g, height_g)
        self.setFont(QtGui.QFont("Verdana"))
        self.setWindowTitle("Combino GUI")
        # ui
        self.ui = Ui_MainWin()
        self.ui.setupUi(self)

	self.initDistribTab()

        self.ui.pbUpdate.clicked.connect(self.do_update)
        self.ui.comboBookBox.activated[int].connect(self.do_changeBook)
        self.ui.comboGridBox.activated[int].connect(self.do_changeGrid)
        self.ui.pbGenerate.clicked.connect(self.do_generateInputGrid)
	self.ui.pbGenerateOdds.clicked.connect(self.do_generateOdds)
	self.ui.pbQuit.clicked.connect(self.do_quit)
	self.ui.progressBar.hide()

        self.__grid = None
        self.__gridHandler = None
	self.__gridRequestor = GridRequestor()
	self.__gridRequestor.distribPageGenerated.sig.connect(self.do_handleDistribHtmlPage)
        self.__nextAction = actions[0]

        # other attribut
        self.__inputFileName = None
        self.__outputDirName = None
        self.__buttonGenerate = None
        self.__myBets = None
	self.__teamDisplay = []

        self.__progressBar = None
        # fen_l = QtGui.QDesktopWidget().screenGeometry()
        try:
            self.setWindowIcon(QtGui.Icon("icon.jpg"))
        except:
            pass

# ################ Slots ######################
    def do_receiveHtml(self, reply):
        print "do_receiveHtml"
        htmlPage = reply.readAll()
        if self.__nextAction == 'CombinoGenBook':
            self.__gridHandler.handleHtmlPage(htmlPage)
            self.updateConfigTab()
	elif self.__nextAction == 'CombinoGenOdds':
	    #self.__gridHandler.handleOddsHtmlPage(htmlPage)
	    #self.updateOdddsTab()
	    pass
	elif self.__nextAction == 'CombinoGenResult':
            self.__gridHandler.handleHtmlPage(htmlPage)
	    self.updateConfigTab()

	print "DISCONNECT"
	combinoManager = CombinoNetworkManager.Instance()
	combinoManager.manager.finished[QNetworkReply].disconnect(self.do_receiveHtml)

    def do_changeGrid(self, index):
        self.__gridHandler.changeGrid(index)

    def do_changeBook(self, index):
        if index == 0:
            self.__gridHandler = readWinamax7Handler()
        elif index == 1:
            self.__gridType = "winamax12"
            print "Winamax 12"
        elif index == 2:
            self.__gridType = "lotofoot7"
            print "LotoFoot 7"
        elif index == 3:
            self.__gridType = "lotofoot15"
            print "LotoFoot 15"
        elif index == 4:
            self.__gridType = "betclic5"
            print "Betclic 5"
        elif index == 5:
            self.__gridType = "betclic8"
            print "Betclic 8"
        else:
            print "index = %s" % index
	# try :
	combinoManager = CombinoNetworkManager.Instance()
	combinoManager.setUrl(self.__gridHandler.bookUrl())
	combinoManager.manager.finished[QNetworkReply].connect(self.do_receiveHtml)
	# request.setAttribute(QNetworkRequest.RedirectionTargetAttribute, True)
	reponse = combinoManager.get() #send request

    def do_handleDistribHtmlPage(self, sourcePage):
	print(sourcePage)
	self.ui.progressBar.hide()
	self.__grid = self.__gridHandler.handleDistribHtmlPage(sourcePage)
	self.updateDistribTab()

    def do_generateOdds(self):
	#self.sendOddsRequest(self)
	#self.updateOddsTab()
	return


    def do_generateInputGrid(self):
	self.__nextAction = 'CombinoGenDistrib'
	self.__gridRequestor.setUrl(self.__gridHandler.distribUrl())
	print "requested url = %s" % self.__gridHandler.distribUrl()
	self.__gridRequestor.start()
	self.ui.progressBar.show()
	return

    def do_quit(self):
	QtCore.QCoreApplication.instance().quit()

    def do_update(self):
	self.__nextAction = 'CombinoGenBook'
	self.ui.comboBookBox.addItem("Winamax 7")
	self.ui.comboBookBox.addItem("Winamax 12")
	self.ui.comboBookBox.addItem("LotoFoot 7")
	self.ui.comboBookBox.addItem("LotoFoot 15")
	self.ui.comboBookBox.addItem("Betclic 5")
	self.ui.comboBookBox.addItem("Betclic 8")
	self.do_changeBook(0)
	print "updated !"
# ################ End Slots ######################

    #def sendOddsRequest(self):
	#for match in self.__grid:

    def initDistribTab(self):
	self.__gridDistribLayout = QGridLayout()
	label1 = QLabel("Team1")
	label2 = QLabel("Team2")
	self.__gridDistribLayout.addWidget(label1, 0, 0)
	self.__gridDistribLayout.addWidget(label2, 0, 1)
	return

    def updateDistribTab(self):
	size = int(self.__gridHandler.gridSize())
	for i in range(0, size):
		label1 = QLabel(self.__gridHandler.grid().getGame(i).team1())
		self.__gridDistribLayout.addWidget(label1, 1+i, 0)
		label1 = QLabel(self.__gridHandler.grid().getGame(i).team2())
		self.__gridDistribLayout.addWidget(label1, 1+i, 1)
		lineEdit1 = QLineEdit()
		lineEdit1.setText("%.2f" % (self.__gridHandler.grid().getGame(i).getRepartition(0)*100))
		lineEditN = QLineEdit()
		lineEditN.setText("%.2f" % (self.__gridHandler.grid().getGame(i).getRepartition(1)*100))
		lineEdit2 = QLineEdit()
		lineEdit2.setText("%.2f"% (self.__gridHandler.grid().getGame(i).getRepartition(2)*100))
		self.__gridDistribLayout.addWidget(lineEdit1, 1+i, 2)
		labelPct = QLabel("%")
		self.__gridDistribLayout.addWidget(labelPct, 1+i, 3)
		self.__gridDistribLayout.addWidget(lineEditN, 1+i, 4)
		labelPct = QLabel("%")
		self.__gridDistribLayout.addWidget(labelPct, 1+i, 5)
		self.__gridDistribLayout.addWidget(lineEdit2, 1+i, 6)
		labelPct = QLabel("%")
		self.__gridDistribLayout.addWidget(labelPct, 1+i, 7)

	#self.__gridDistribLayout.addWidget(self.ui.pbGenerateOdds, size+1, 0)
	self.__gridDistribLayout.addWidget(self.ui.pbImport, size+1, 7)
	self.ui.Distrib.setLayout(self.__gridDistribLayout)
	return

    def updateConfigTab(self):
	# clean the comboGridBox
        index = self.ui.comboGridBox.count()
        while index != 0:
            print "remove index %d" % index
            self.ui.comboGridBox.removeItem(index - 1)
            index = self.ui.comboGridBox.count()
	# fill the comboGridBox with new values
	index = 0
	selected = False
        now = QDateTime.currentMSecsSinceEpoch() / 1000  # in sec
        print "now=%d" % now
        for gridNumber in self.__gridHandler.gridList():
            print "add grid n %s" % gridNumber[0]
            self.ui.comboGridBox.addItem(gridNumber[0])
            try:
                if int(now) >= int(gridNumber[1]):
                    print "disabled"
		    self.ui.comboGridBox.model().item(index).setEnabled(False)
		elif not selected:
		    self.ui.comboGridBox.setCurrentIndex(index)
		    self.do_changeGrid(index)
		    selected = True
            except ValueError:
		pass
	    index+=1


    def browseFile(self):
        print "input dir = %s" % ''.join((os.getcwd(), "/Input/"))
        self.__inputFileName = \
        QtGui.QFileDialog.getOpenFileName(self, "Open xls", ''.join((os.getcwd(), "/Input/")), "xls Files (*.xls)")[0]
        #	self.__inputFileName = QtGui.QFileDialog.getOpenFileName(self, "Open xls", os.getcwd(), "xls Files (*.xls)")
        self.__labelInputFileName.setText(self.__inputFileName)
        self.__labelInputFileName.adjustSize()
        print "Input file : %s" % self.__inputFileName
        if (self.__inputFileName != None) and (self.__outputDirName != None):
            self.__buttonGenerate.setEnabled(True)
        else:
            self.__buttonGenerate.setEnabled(False)

    def cancelGen(self):
        self.stopGenSig.emit()

    def browseDir(self):
        print "run dir = %s" % ''.join((os.getcwd(), "/Output/"))
        outputDirName_l = QtGui.QFileDialog.getExistingDirectory(self, "Output directory",
                                                                 ''.join((os.getcwd(), "/Output/")),
                                                                 QtGui.QFileDialog.ShowDirsOnly | QtGui.QFileDialog.DontResolveSymlinks)
        self.__outputDirName = outputDirName_l.replace("\\", "/")
        self.__labelOutputDirName.setText(self.__outputDirName)
        self.__labelOutputDirName.adjustSize()
        print "Output dir : %s" % self.__outputDirName
        if (self.__inputFileName != None) and (self.__outputDirName != None):
            self.__buttonGenerate.setEnabled(True)
        else:
            self.__buttonGenerate.setEnabled(False)

    def generate(self):
        espMin_l = 1  # default value
        print "Lecture fichier Source : %s" % self.__inputFileName
        mySource_l = CombinoSource(self.__inputFileName)
        myGrille_l = mySource_l.getGrille()
        # create outputfile name
        self.__outputDirName = ''.join((self.__outputDirName, "/"))
        self.__outputFileName = ''.join((self.__inputFileName[0:-3], "csv"))
        print "outputfile etape 1: %s" % self.__outputFileName
        indexStartFileName_l = self.__outputFileName.rfind("/")
        # print "separateur : %s" % os.sep
        self.__outputFileName = ''.join((self.__outputDirName, self.__outputFileName[indexStartFileName_l:]))
        print "outputfile final :", self.__outputDirName
        print "Destination :", self.__outputFileName

        print "Calcul Proba et Esperances des grilles"
        self.__outputFile = open(self.__outputFileName, 'w+')
        self.__outputFile.write(
            "Game;Proba-Rg1;Esp-Rg1;Estim-Rg1;Proba-Rg2;Esp-Rg2;Estim-Rg2;Proba-Rg3;Esp-Rg3;Estim-Rg3;Esp-tot\n")
        returnRate_l = mySource_l.getReturnRate()
        firstRankRate_l = mySource_l.getFirstRankRate()
        scndRankRate_l = mySource_l.getScndRankRate()
        thirdRankRate_l = mySource_l.getThirdRankRate()
        jackpot_l = mySource_l.getJackpot()
        nbPlayers_l = mySource_l.getNbPlayers()
        totalRate_l = returnRate_l * firstRankRate_l
        if thirdRankRate_l != -1:
            totalRate2nd_l = returnRate_l * scndRankRate_l
            totalRate3rd_l = returnRate_l * thirdRankRate_l
            print "Min Esp : %f" % espMin_l
            print "1st rank rate Esp : %f" % firstRankRate_l
            print "2nd rank rate Esp : %f" % scndRankRate_l
            print "3rd rank rate Esp : %f" % thirdRankRate_l
            print "Jackpot : %f Euros" % jackpot_l
            print "Nb Players Esp : %f" % nbPlayers_l
            self.__myBets = CombinoEngine(myGrille_l, totalRate_l, espMin_l, self.__outputFile, jackpot_l, nbPlayers_l,
                                          totalRate2nd_l, totalRate3rd_l, self)
        elif scndRankRate_l != -1:
            totalRate2nd_l = returnRate_l * scndRankRate_l
            print "1st rank rate Esp : %f" % firstRankRate_l
            print "2nd rank rate Esp : %f" % scndRankRate_l
            print "Jackpot : %f Euros" % jackpot_l
            print "Nb Players Esp : %f" % nbPlayers_l
            self.__myBets = CombinoEngine(myGrille_l, totalRate_l, espMin_l, self.__outputFile, jackpot_l, nbPlayers_l,
                                          totalRate2nd_l, 0, self)
        else:
            print "1st rank rate Esp : %f" % firstRankRate_l
            print "Jackpot : %f Euros" % jackpot_l
            print "Nb Players Esp : %f" % nbPlayers_l
            self.__myBets = CombinoEngine(myGrille_l, totalRate_l, espMin_l, self.__outputFile, jackpot_l, nbPlayers_l,
                                          0, 0, self)
        # Finished generation
        self.__myBets.finishedSig.connect(self.on_finished)
        self.__myBets.progressSig.connect(self.on_progressed)
        self.__progressBar.setValue(0)
        self.__progressBar.show()
        self.__buttonCancelGen.show()
        self.__myBets.start()

    @Slot(int)
    def on_progressed(self, prog):
        print "%d pct" % prog
        self.__progressBar.setValue(prog)
        self.__progressBar.update()

    @Slot()
    def on_finished(self):
        print "Fichier genere :", self.__outputFileName
        self.__outputFile.write(str(self.__myBets))
        self.__progressBar.hide()
        self.__buttonCancelGen.hide()


app_l = QtGui.QApplication(sys.argv)
combinoGui_l = CombinoGUI()
combinoGui_l.show()
sys.exit(app_l.exec_())
