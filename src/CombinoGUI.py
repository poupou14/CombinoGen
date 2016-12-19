import os,string, sys
from PySide import QtCore, QtGui
from PySide.QtCore import  Signal, Slot
from CombinoSource import CombinoSource
from CombinoEngine import CombinoEngine

height_g = 600
width_g = 800

class CombinoGUI(QtGui.QMainWindow) :
	def __init__(self, parent_l=None):
		QtGui.QMainWindow.__init__(self, parent_l)
		self.resize(width_g,height_g)
		self.setFont(QtGui.QFont("Verdana"))
		self.setWindowTitle("Combino GUI")

		# widgets
		self.__quit1 = None 
		self.__menuquit = None 
		self.__menubar = None 
		self.__tabWidget = None 
		self.__pageGen = None 
		self.__pageGrille = None 
		self.__pageConfig = None 
	        self.__labelInputFileName = None
	        self.__labelInputFileMesg = None
	        self.__labelOutputDirName = None
	        self.__labelOutputDirMesg = None
	        self.__buttonInputChoseFile = None
		self.__ouputFileName = None
		self.__ouputFile= None

		# other attribut
	        self.__inputFileName = None
		self.__outputDirName = None
		self.__buttonGenerate = None
		self.__myBets = None

		self.__progressBar = QtGui.QProgressBar()
		self.__progressBar.setGeometry(300, 300, 280, 30)
		size_l = self.__progressBar.geometry()
		fen_l = QtGui.QDesktopWidget().screenGeometry()
		self.__progressBar.move((fen_l.width()-size_l.width())/2, (fen_l.height()-size_l.height())/2)
		self.__progressBar.setRange(0,100)
		self.__progressBar.setValue(0)
		self.__progressBar.update()
		self.__progressBar.setFocus()
		self.__progressBar.setWindowTitle("Generation progress")
		try:
			self.setWindowIcon(QtGui.Icon("icon.jpg"))
		except:pass

	def createWindow(self) :		
		# center the window
		fen_l = QtGui.QDesktopWidget().screenGeometry()
		size_l = self.geometry()
		self.move((fen_l.width()-size_l.width())/2, (fen_l.height()-size_l.height())/2)
		
		#Creation de la barre de statut avec les informations voulues.
		self.statusBar().showMessage("CombinoGUI")

		self.__menubar = self.menuBar() ## Creation d'une barre de menu
		file_l = self.__menubar.addMenu("Fichier") ## Ajout d'un menu.

		#Creation de l'action Fermer.
		#QAction recoit cinq parametres qui sont le titre, le parent,
		#le raccourci clavier, le message qui apparaitra dans la barre de statut et enfin le slot qui sera appele.
		self.__menuquit = QtGui.QAction("Fermer", self, shortcut=QtGui.QKeySequence.Close, statusTip="Quitter CombinoGUI", triggered=self.close)   
        
		#Ajout de l'action creee ci-dessus.
		file_l.addAction(self.__menuquit)

		#Ajout de la fenetre a onglets
		self.__tabWidget = QtGui.QTabWidget(self)
		self.__tabWidget.setGeometry(0,20,width_g,height_g-100)

		#Creation de deux QWidget qui permettront ensuite de creer les pages du QTabWidget
		self.__pageGen = QtGui.QWidget(self.__tabWidget)

		#A noter que le parent du QWidget peut aussi bien etre le QTabWidget 
		#QMainWindows. Personnellement, je prefere la premiere solution afin 
		#de garder une hierarchie coherente dans le code.
		self.__pageGrille = QtGui.QWidget(self.__tabWidget)
		self.__pageConfig = QtGui.QWidget(self.__tabWidget)

		#Ajout des QWidgets en temps que Tab du QTabWidget.
		#Le premier Tab portera le nom Entree et le deuxieme le nom Lecture.
		self.__tabWidget.addTab(self.__pageGrille, "Grille")
		self.__tabWidget.addTab(self.__pageGen, "General")
		self.__tabWidget.addTab(self.__pageConfig, "Config")
        
		#Modification de la couleur de fond des QWidget.
		self.__pageGen.setPalette(QtGui.QPalette(QtGui.QColor("white")))
		self.__pageGen.setAutoFillBackground(True)
		self.__pageGrille.setPalette(QtGui.QPalette(QtGui.QColor("white")))
		self.__pageGrille.setAutoFillBackground(True)

		self.fillPageGen()
		self.fillPageGrille()
		self.fillPageConfig()

		# Generate button
		self.__buttonGenerate = QtGui.QPushButton("Generate", self)
		buttonSize_l = self.__buttonGenerate.geometry()
		self.__buttonGenerate.move(self.width()-2*buttonSize_l.width()-30, self.height()-buttonSize_l.height()-30)
		self.__buttonGenerate.clicked.connect(self.generate)
		self.__buttonGenerate.setEnabled(False)

		# Quit button
		self.__quit1 = QtGui.QPushButton("Quitter", self)
		buttonSize_l = self.__quit1.geometry()
		self.__quit1.move(self.width()-buttonSize_l.width()-10, self.height()-buttonSize_l.height()-30)
		self.__quit1.clicked.connect(self.close)

		#self.__quit = QtGui.QPushButton("Quitter", self.__pageGen)
		#self.__quit.move(100, 100)
		#self.__quit.clicked.connect(self.close)


	def fillPageGen(self) :
		# Input File
	        self.__labelInputFileMesg = QtGui.QLabel("Fichier d'entree :", self.__pageGen)
	        self.__labelInputFileMesg.move(10, 40)
	        self.__labelInputFileMesg.show()

	        self.__labelInputFileName = QtGui.QLabel("...", self.__pageGen)
		self.__labelInputFileName.adjustSize()
		#self.__labelInputFileName.setGeometry(0,50,100,50)
	        self.__labelInputFileName.move(140, 40)
	        self.__labelInputFileName.show()

		# Input File button
		self.__buttonInputChoseFile = QtGui.QPushButton("Choisir...", self.__pageGen)
		buttonSize_l = self.__buttonInputChoseFile.geometry()
		self.__buttonInputChoseFile.move(self.width() - 100 ,40)
		self.__buttonInputChoseFile.clicked.connect(self.browseFile)

		# Generate grid
	        self.__labelOutputDirMesg = QtGui.QLabel("Repetoire de sortie :", self.__pageGen)
	        self.__labelOutputDirMesg.move(10, 80)
	        self.__labelOutputDirMesg.show()

	        self.__labelOutputDirName = QtGui.QLabel("...", self.__pageGen)
		self.__labelOutputDirName.adjustSize()
		#self.__labelInputFileName.setGeometry(0,50,100,50)
	        self.__labelOutputDirName.move(140, 80)
	        self.__labelOutputDirName.show()

		# Input File button
		self.__buttonOutputDir = QtGui.QPushButton("Choisir", self.__pageGen)
		buttonSize_l = self.__buttonOutputDir.geometry()
		self.__buttonOutputDir.move(self.width() - 100 ,80)
		self.__buttonOutputDir.clicked.connect(self.browseDir)

		#self.__quit = QtGui.QPushButton("Quitter", self.__pageGen)
	
	def fillPageConfig(self) :
		print "config"


	def fillPageGrille(self) :
		print "grille"


	def browseFile(self) :
		self.__inputFileName = QtGui.QFileDialog.getOpenFileName(self, "Open xls", ''.join((os.getcwd(), "/../Input/")), "xls Files (*.xls)")[0]
#	self.__inputFileName = QtGui.QFileDialog.getOpenFileName(self, "Open xls", os.getcwd(), "xls Files (*.xls)")
		self.__labelInputFileName.setText(self.__inputFileName)
		self.__labelInputFileName.adjustSize()
		if (self.__inputFileName != None) and  (self.__outputDirName != None) :
			self.__buttonGenerate.setEnabled(True)
		else :
			self.__buttonGenerate.setEnabled(False)
		
	def browseDir(self) :
		outputDirName_l = QtGui.QFileDialog.getExistingDirectory(self, "Output directory", ''.join((os.getcwd(), "/../Output/")), QtGui.QFileDialog.ShowDirsOnly | QtGui.QFileDialog.DontResolveSymlinks)
		self.__outputDirName = outputDirName_l.replace("\\", "/")
		self.__labelOutputDirName.setText(self.__outputDirName)
		self.__labelOutputDirName.adjustSize()
		if (self.__inputFileName != None) and  (self.__outputDirName != None) :
			self.__buttonGenerate.setEnabled(True)
		else :
			self.__buttonGenerate.setEnabled(False)
		

	def generate(self) :
		self.__progressBar.show()
		espMin_l = 1 # default value
		mySource_l = CombinoSource(self.__inputFileName)
		myGrille_l = mySource_l.getGrille()
		# create outputfile name
		print "Lecture fichier Source : %s" % self.__inputFileName
		self.__outputDirName = ''.join((self.__outputDirName, "/")) 
		self.__ouputFileName = ''.join((self.__inputFileName[0:-3], "csv"))
		print "outputfile etape 1: %s" % self.__ouputFileName
		indexStartFileName_l = self.__ouputFileName.rfind("/")
		#print "separateur : %s" % os.sep
		self.__ouputFileName = ''.join((self.__outputDirName, self.__ouputFileName[indexStartFileName_l:])) 
		print "outputfile final :", self.__outputDirName
		print "Destination :", self.__ouputFileName

		print "Calcul Proba et Esperances des grilles"
		self.__outputFile=open(self.__ouputFileName, 'w+')
		self.__outputFile.write("Game;Proba-Rg1;Esp-Rg1;Estim-Rg1;Proba-Rg2;Esp-Rg2;Estim-Rg2;Proba-Rg3;Esp-Rg3;Estim-Rg3;Esp-tot\n")
		returnRate_l = mySource_l.getReturnRate()
		firstRankRate_l = mySource_l.getFirstRankRate()
		scndRankRate_l = mySource_l.getScndRankRate()
		thirdRankRate_l = mySource_l.getThirdRankRate()
		jackpot_l = mySource_l.getJackpot()
		nbPlayers_l = mySource_l.getNbPlayers()
		totalRate_l = returnRate_l * firstRankRate_l
		if thirdRankRate_l != -1 :
			totalRate2nd_l = returnRate_l * scndRankRate_l
			totalRate3rd_l = returnRate_l * thirdRankRate_l
			print "Min Esp : %f" % espMin_l
			print "1st rank rate Esp : %f" % firstRankRate_l
			print "2nd rank rate Esp : %f" % scndRankRate_l
			print "3rd rank rate Esp : %f" % thirdRankRate_l
			print "Jackpot : %f Euros" % jackpot_l
			print "Nb Players Esp : %f" % nbPlayers_l
			self.__myBets = CombinoEngine(myGrille_l, totalRate_l, espMin_l, self.__outputFile, jackpot_l, nbPlayers_l, totalRate2nd_l, totalRate3rd_l, self)
		elif scndRankRate_l != -1 :
			totalRate2nd_l = returnRate_l * scndRankRate_l
			print "1st rank rate Esp : %f" % firstRankRate_l
			print "2nd rank rate Esp : %f" % scndRankRate_l
			print "Jackpot : %f Euros" % jackpot_l
			print "Nb Players Esp : %f" % nbPlayers_l
			self.__myBets = CombinoEngine(myGrille_l, totalRate_l, espMin_l, self.__outputFile, jackpot_l, nbPlayers_l, totalRate2nd_l, 0, self)
		else :
			print "1st rank rate Esp : %f" % firstRankRate_l
			print "Jackpot : %f Euros" % jackpot_l
			print "Nb Players Esp : %f" % nbPlayers_l
			self.__myBets = CombinoEngine(myGrille_l, totalRate_l, espMin_l, self.__outputFile, jackpot_l, nbPlayers_l, 0, 0, self)
		# Finished generation
 		self.__myBets.finishedSig.connect(self.on_finished)
 		self.__myBets.progressSig.connect(self.on_progressed)
		self.__progressBar.show()
		self.__myBets.start()

	@Slot(int)
	def on_progressed(self, prog):
		self.__progressBar.setValue(prog)
		self.__progressBar.update()

	@Slot()
	def on_finished(self ):
		print "Fichier genere :", self.__ouputFileName
		self.__outputFile.write(str(self.__myBets))
		self.__progressBar.hide()


app_l = QtGui.QApplication(sys.argv)
combinoGui_l = CombinoGUI()
combinoGui_l.createWindow()
combinoGui_l.show()
sys.exit(app_l.exec_())

