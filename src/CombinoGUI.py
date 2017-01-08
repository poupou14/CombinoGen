import os, sys
from PySide import QtCore, QtGui
from PySide.QtGui import QGridLayout, QLineEdit, QLabel
from PySide.QtCore import Signal, Slot, QDateTime
from PySide.QtNetwork import QNetworkReply
from CombinoNetworkManager import CombinoNetworkManager
from CombinoSource import CombinoSource
from CombinoEngine import CombinoEngine
from ui_mainwin import Ui_MainWin
from ReadGridHandlerFactory import ReadGridHandlerFactory
from ReadWinamax7Handler import ReadWinamax7Handler
from ReadWinamax12Handler import ReadWinamax12Handler
from ReadLoto15Handler import ReadLoto15Handler
from ReadLoto7Handler import ReadLoto7Handler
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
        self.__dynamicDistribWidgets = []
        self.__dynamicOddsWidgets = []

        self.initDistribTab()
        #self.initOddsTab()

        self.ui.pbUpdate.clicked.connect(self.do_update)
        self.ui.comboBookBox.activated[int].connect(self.do_changeBook)
        self.ui.comboGridBox.activated[int].connect(self.do_changeGrid)
        self.ui.pbGenerate.clicked.connect(self.do_generateInputGrid)
        self.ui.pbGenerateGrid.clicked.connect(self.do_generateGrid)
        self.ui.pbImport.clicked.connect(self.do_importGrid)
        self.ui.pb1Browse.clicked.connect(self.do_browseDir)
        self.ui.pbQuit.clicked.connect(self.do_quit)
        self.ui.progressBar.hide()

        self.__distribLayoutGridWidth = 0
        self.__gridIndex = -1
        self.__gridHandler = None
        self.__gridRequestor = GridRequestor()
        self.__gridRequestor.distribPageGenerated.sig.connect(self.do_handleDistribHtmlPage)
        self.__nextAction = actions[0]

        # other attribut
        self.__gridHandlerFactory = ReadGridHandlerFactory()
        self.__inputFileName = None
        self.__outputDirName =  ''.join((os.getcwd(), "/Output/"))
        self.__buttonGenerate = None
        self.__myBets = None
        self.__teamDisplay = []
        self.__combinoEngine = None

        self.__progressBar = None
        self.ui.outputDirLine.setText(self.__outputDirName)
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
            self.__gridHandler.handleOddsHtmlPage(htmlPage)
            self.ui.progressBar.hide()
            #self.updateOddsTab()
            self.updateDistribTab()
        elif self.__nextAction == 'CombinoGenResult':
            self.__gridHandler.handleHtmlPage(htmlPage)
            self.updateConfigTab()

        print "DISCONNECT"
        combinoManager = CombinoNetworkManager.Instance()
        combinoManager.manager.finished[QNetworkReply].disconnect(self.do_receiveHtml)

    def do_importGrid(self):
        print "input dir = %s" % ''.join((os.getcwd(), "/Input/"))
        self.__inputFileName = QtGui.QFileDialog.getOpenFileName(self, "Open xls", ''.join((os.getcwd(), "/Input/")), "xls Files (*.xls)")[0]
        print "Input file : %s" % self.__inputFileName
        print "Lecture fichier Source"
        self.__gridHandler = self.__gridHandlerFactory.createGridHandler(self.__inputFileName)
        # mySource = CombinoSource(self.__inputFileName)
        self.updateDistribTab()
        self.updateOddsTab()

    def do_updateDataGrid(self):
        print "do_updateDataGrid\n"
        self.readDistribInput()

    def do_changeGrid(self, index):
        self.__gridHandler.changeGrid(index)
        self.__gridIndex = index

    def do_changeBook(self, index):
        if index == 0:
            self.__gridHandler = ReadWinamax7Handler()
        elif index == 1:
            self.__gridHandler = ReadWinamax12Handler()
            print "Winamax 12"
        elif index == 2:
            print "LotoFoot 7"
            self.__gridHandler = ReadLoto7Handler()
        elif index == 3:
            print "LotoFoot 15"
            self.__gridHandler = ReadLoto15Handler()
        elif index == 4:
            print "Betclic 5"
        elif index == 5:
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
        #print(sourcePage)
        self.ui.progressBar.hide()
        self.__gridHandler.handleDistribHtmlPage(sourcePage.encode('utf-8'))
        self.do_generateOdds()

    def do_generateGrid(self):
        outputFileName = self.__outputDirName
        try:
                outputFileName = ''.join((self.__outputDirName,'/'))
                list = (self.__gridHandler.gridList())
                date = list[self.__gridIndex][0]
                outputFileName = ''.join((outputFileName,  self.__gridHandler.gridName()))
                outputFileName = ''.join((outputFileName, "-"))
                outputFileName = ''.join((outputFileName, str(date)))
                outputFileName = ''.join((outputFileName, ".csv"))
        except IndexError:
                indexSlash = self.__inputFileName.rfind("/")
                inputFileName = self.__inputFileName[indexSlash:]
                outputFileName = ''.join((outputFileName, inputFileName[0:-3]))
                outputFileName = ''.join((outputFileName, "csv"))
        self.__combinoEngine = CombinoEngine(self.__gridHandler.grid(), 1, outputFileName, self)
        #mainWindow_p.stopGenSig.connect(self.cancelGen)
        print "Grid generation"
        self.__combinoEngine.start()



    def do_generateOdds(self):
        self.__nextAction = 'CombinoGenOdds'
        print "Generate Odds"
        print "requested url = %s" % self.__gridHandler.oddsUrl()
        self.ui.progressBar.show()
        combinoManager = CombinoNetworkManager.Instance()
        combinoManager.setUrl(self.__gridHandler.oddsUrl())
        combinoManager.manager.finished[QNetworkReply].connect(self.do_receiveHtml)
        reponse = combinoManager.get() #send request
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

    def do_browseDir(self):
        print "run dir = %s" % ''.join((os.getcwd(), "/Output/"))
        outputDirName_l = QtGui.QFileDialog.getExistingDirectory(self, "Output directory",
                                                                 ''.join((os.getcwd(), "/Output/")),
                                                                 QtGui.QFileDialog.ShowDirsOnly | QtGui.QFileDialog.DontResolveSymlinks)
        self.__outputDirName = outputDirName_l.replace("\\", "/")
        self.ui.outputDirLine.setText(self.__outputDirName)
        #self.ui.outputDirLine.adjustSize()
        print "Output dir : %s" % self.__outputDirName

# ################ End Slots ######################

    #def sendOddsRequest(self):
        #for match in self.__grid:

    def initDistribTab(self):
        self.__gridDistribLayout = QGridLayout()
        label1 = QLabel("Team1")
        label2 = QLabel("Team2")
        labelP1 = QLabel("1")
        labelPN = QLabel("N")
        labelP2 = QLabel("2")
        labelPTot = QLabel("Total")
        labelBarre = QLabel("|")
        labelC1 = QLabel("1")
        labelCN = QLabel("N")
        labelC2 = QLabel("2")
        labelCTot = QLabel("Total")
        self.__gridDistribLayout.addWidget(label1, 0, 0)
        self.__gridDistribLayout.addWidget(label2, 0, 1)
        self.__gridDistribLayout.addWidget(labelP1, 0, 2)
        self.__gridDistribLayout.addWidget(labelPN, 0, 4)
        self.__gridDistribLayout.addWidget(labelP2, 0, 6)
        self.__gridDistribLayout.addWidget(labelPTot, 0, 8)
        self.__gridDistribLayout.addWidget(labelBarre, 0, 9)
        self.__gridDistribLayout.addWidget(labelC1, 0, 10)
        self.__gridDistribLayout.addWidget(labelCN, 0, 11)
        self.__gridDistribLayout.addWidget(labelC2, 0, 12)
        self.__gridDistribLayout.addWidget(labelCTot, 0, 13)
        self.ui.DistribAndOdds.setLayout(self.__gridDistribLayout)
        return

    def cleanDistribTab(self):
        for widget in self.__dynamicDistribWidgets:
                self.__gridDistribLayout.removeWidget(widget)
                widget.deleteLater()
        self.__gridDistribLayout.removeWidget(self.ui.pbGenerateGrid)

    def updateOddsTab(self):
        return

    def updateDistribTab(self):
        self.cleanDistribTab()
        size = int(self.__gridHandler.gridSize())
        j=0
        for i in range(0, size):
                self.__dynamicDistribWidgets.append(QLabel(self.__gridHandler.grid().getGame(i).team1()))
                self.__gridDistribLayout.addWidget(self.__dynamicDistribWidgets[j], 1+i, 0)
                j+=1

                self.__dynamicDistribWidgets.append( QLabel(self.__gridHandler.grid().getGame(i).team2()))
                self.__gridDistribLayout.addWidget(self.__dynamicDistribWidgets[j], 1+i, 1)
                j+=1

                self.__dynamicDistribWidgets.append( QLineEdit())
                self.__dynamicDistribWidgets[j].setText("%.1f" % (self.__gridHandler.grid().getGame(i).getRepartition(0)*100))
                self.__dynamicDistribWidgets[j].editingFinished.connect(self.do_updateDataGrid)
                self.__gridDistribLayout.addWidget(self.__dynamicDistribWidgets[j], 1+i, 2)
                j+=1

                self.__dynamicDistribWidgets.append( QLabel("%"))
                self.__gridDistribLayout.addWidget(self.__dynamicDistribWidgets[j], 1+i, 3)
                j+=1

                self.__dynamicDistribWidgets.append( QLineEdit())
                self.__dynamicDistribWidgets[j].setText("%.1f" % (self.__gridHandler.grid().getGame(i).getRepartition(1)*100))
                self.__dynamicDistribWidgets[j].editingFinished.connect(self.do_updateDataGrid)
                self.__gridDistribLayout.addWidget(self.__dynamicDistribWidgets[j], 1+i, 4)
                j+=1

                self.__dynamicDistribWidgets.append( QLabel("%"))
                self.__gridDistribLayout.addWidget(self.__dynamicDistribWidgets[j], 1+i, 5)
                j+=1

                self.__dynamicDistribWidgets.append( QLineEdit())
                self.__dynamicDistribWidgets[j].setText("%.1f"% (self.__gridHandler.grid().getGame(i).getRepartition(2)*100))
                self.__dynamicDistribWidgets[j].editingFinished.connect(self.do_updateDataGrid)
                self.__gridDistribLayout.addWidget(self.__dynamicDistribWidgets[j], 1+i, 6)
                j+=1

                self.__dynamicDistribWidgets.append( QLabel("%"))
                self.__gridDistribLayout.addWidget(self.__dynamicDistribWidgets[j], 1+i, 7)
                j+=1

                total = self.__gridHandler.grid().getGame(i).getRepartition(0)
                total += self.__gridHandler.grid().getGame(i).getRepartition(1)
                total += self.__gridHandler.grid().getGame(i).getRepartition(2)
                self.__dynamicDistribWidgets.append(QLabel("%3.1f" % (total*100)))
                self.__gridDistribLayout.addWidget(self.__dynamicDistribWidgets[j], 1+i, 8)
                j+=1

                self.__dynamicDistribWidgets.append( QLabel("|"))
                self.__gridDistribLayout.addWidget(self.__dynamicDistribWidgets[j], 1+i, 9)
                j+=1

                self.__dynamicDistribWidgets.append( QLineEdit())
                self.__dynamicDistribWidgets[j].setText("%.2f" % (self.__gridHandler.grid().getGame(i).getCotes(0)))
                self.__dynamicDistribWidgets[j].editingFinished.connect(self.do_updateDataGrid)
                self.__gridDistribLayout.addWidget(self.__dynamicDistribWidgets[j], 1+i, 10)
                j+=1

                self.__dynamicDistribWidgets.append( QLineEdit())
                self.__dynamicDistribWidgets[j].setText("%.2f" % (self.__gridHandler.grid().getGame(i).getCotes(1)))
                self.__dynamicDistribWidgets[j].editingFinished.connect(self.do_updateDataGrid)
                self.__gridDistribLayout.addWidget(self.__dynamicDistribWidgets[j], 1+i, 11)
                j+=1

                self.__dynamicDistribWidgets.append( QLineEdit())
                self.__dynamicDistribWidgets[j].setText("%.2f"% (self.__gridHandler.grid().getGame(i).getCotes(2)))
                self.__dynamicDistribWidgets[j].editingFinished.connect(self.do_updateDataGrid)
                self.__gridDistribLayout.addWidget(self.__dynamicDistribWidgets[j], 1+i, 12)
                j+=1

                sigmaCotesMoinsUn = 1/self.__gridHandler.grid().getGame(i).getCotes(0) + 1/self.__gridHandler.grid().getGame(i).getCotes(1) + 1/self.__gridHandler.grid().getGame(i).getCotes(2)

                self.__dynamicDistribWidgets.append(QLabel("%1.2f" % sigmaCotesMoinsUn))
                self.__gridDistribLayout.addWidget(self.__dynamicDistribWidgets[j], 1+i, 13)
                j+=1

                ret0 = 1/(self.__gridHandler.grid().getGame(i).getRepartition(0)*self.__gridHandler.grid().getGame(i).getCotes(0)*sigmaCotesMoinsUn)
                ret1 = 1/(self.__gridHandler.grid().getGame(i).getRepartition(1)*self.__gridHandler.grid().getGame(i).getCotes(1)*sigmaCotesMoinsUn)
                ret2 = 1/(self.__gridHandler.grid().getGame(i).getRepartition(2)*self.__gridHandler.grid().getGame(i).getCotes(2)*sigmaCotesMoinsUn)

                self.__dynamicDistribWidgets.append( QLabel("|"))
                self.__gridDistribLayout.addWidget(self.__dynamicDistribWidgets[j], 1+i, 14)
                j+=1

                self.__dynamicDistribWidgets.append( QLabel("%2.2f" % ret0))
                self.__gridDistribLayout.addWidget(self.__dynamicDistribWidgets[j], 1+i, 15)
                j+=1

                self.__dynamicDistribWidgets.append( QLabel("%2.2f" % ret1))
                self.__gridDistribLayout.addWidget(self.__dynamicDistribWidgets[j], 1+i, 16)
                j+=1

                self.__dynamicDistribWidgets.append( QLabel("%2.2f" % ret2))
                self.__gridDistribLayout.addWidget(self.__dynamicDistribWidgets[j], 1+i, 17)
                j+=1

        self.__distribLayoutGridWidth = 18

        self.__gridDistribLayout.addWidget(self.ui.pbGenerateGrid, size+1, 0)
        return

    def readDistribInput(self):
        size = int(self.__gridHandler.gridSize())
        for i in range(0, size):
                #try:
                print "%s vs" % self.__gridHandler.grid().getGame(i).team1()
                print "%s : " % self.__gridHandler.grid().getGame(i).team2()
                distrib1 = float(self.__dynamicDistribWidgets[i*self.__distribLayoutGridWidth+2].text())
                print "%2.2f " % distrib1
                distribN = float(self.__dynamicDistribWidgets[i*self.__distribLayoutGridWidth+4].text())
                print "%2.2f " % distribN
                distrib2 = float(self.__dynamicDistribWidgets[i*self.__distribLayoutGridWidth+6].text())
                print "%2.2f | " % distrib2
                self.__gridHandler.grid().getGame(i).setRepartition(distrib1, distribN, distrib2)
                total = distrib1 + distrib2 + distribN
                cote1 = float(self.__dynamicDistribWidgets[i*self.__distribLayoutGridWidth+10].text())
                print "%2.2f " % cote1
                coteN = float(self.__dynamicDistribWidgets[i*self.__distribLayoutGridWidth+11].text())
                print "%2.2f " % coteN
                cote2 = float(self.__dynamicDistribWidgets[i*self.__distribLayoutGridWidth+12].text())
                print "%2.2f " % cote2
                self.__gridHandler.grid().getGame(i).setCotes(cote1, coteN, cote2)
                sigmaCotesMoinsUn = 1/cote1 + 1/coteN + 1/cote2

                ret0 = 1/(self.__gridHandler.grid().getGame(i).getRepartition(0)*self.__gridHandler.grid().getGame(i).getCotes(0)*sigmaCotesMoinsUn)
                ret1 = 1/(self.__gridHandler.grid().getGame(i).getRepartition(1)*self.__gridHandler.grid().getGame(i).getCotes(1)*sigmaCotesMoinsUn)
                ret2 = 1/(self.__gridHandler.grid().getGame(i).getRepartition(2)*self.__gridHandler.grid().getGame(i).getCotes(2)*sigmaCotesMoinsUn)

                self.__dynamicDistribWidgets[i*self.__distribLayoutGridWidth+8].setText("%3.1f" % total)
                self.__dynamicDistribWidgets[i*self.__distribLayoutGridWidth+8].repaint()
                self.__dynamicDistribWidgets[i*self.__distribLayoutGridWidth+13].setText("%1.2f" % sigmaCotesMoinsUn)
                self.__dynamicDistribWidgets[i*self.__distribLayoutGridWidth+13].repaint()
                self.__dynamicDistribWidgets[i*self.__distribLayoutGridWidth+15].setText("%2.2f" % ret0)
                self.__dynamicDistribWidgets[i*self.__distribLayoutGridWidth+15].repaint()
                self.__dynamicDistribWidgets[i*self.__distribLayoutGridWidth+16].setText("%2.2f" % ret1)
                self.__dynamicDistribWidgets[i*self.__distribLayoutGridWidth+16].repaint()
                self.__dynamicDistribWidgets[i*self.__distribLayoutGridWidth+17].setText("%2.2f" % ret2)
                self.__dynamicDistribWidgets[i*self.__distribLayoutGridWidth+17].repaint()
                #except:
                #        print "erreur de recup lors du %deme match" % i


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
        #        self.__inputFileName = QtGui.QFileDialog.getOpenFileName(self, "Open xls", os.getcwd(), "xls Files (*.xls)")
        self.__labelInputFileName.setText(self.__inputFileName)
        self.__labelInputFileName.adjustSize()
        print "Input file : %s" % self.__inputFileName
        if (self.__inputFileName != None) and (self.__outputDirName != None):
            self.__buttonGenerate.setEnabled(True)
        else:
            self.__buttonGenerate.setEnabled(False)

    def cancelGen(self):
        self.stopGenSig.emit()


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
