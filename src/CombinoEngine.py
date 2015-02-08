#!/usr/bin/python 
import os,string, sys
from PySide import QtCore, QtGui
import math
import copy
from Bet import Bet

betChoice = ['1', 'N', '2']

class CombinoEngine():

	def __init__(self, grille_p, returnRate_p, expectedEsperance_p, file_p, jackpot_p, nbPlayers_p, scndRankRate_p=0, thirdRankRate_p=0, mainWindow_p=None): 
		self.__grille = grille_p
		self.__combinoBets = []
		self.__nbTotBet = 0
		self.__nbGenBets = 0
		self.__indexDisplayPct = 0
		self.__currentBet = None
		self.__returnRate = returnRate_p
		self.__returnRate2 = scndRankRate_p
		self.__returnRate3 = thirdRankRate_p
		self.__expectedEsperance = expectedEsperance_p
		self.__file = file_p
		self.__jackpot = jackpot_p
		self.__nbPlayers = nbPlayers_p
		self.__mainWindow=mainWindow_p
		if mainWindow_p != None :
			self.__progressBar = QtGui.QProgressBar()
			self.__progressBar.setWindowTitle("Generation progress")

	def getGrille(self):
		return self.__grille

	def getReturnRate(self):
		return self.__returnRate

	def getReturnRate2(self):
		return self.__returnRate2

	def getReturnRate3(self):
		return self.__returnRate3

	def getJackpot(self):
		return self.__jackpot

	def getNbPlayers(self):
		return self.__nbPlayers


	def generateCombinoBets(self):
		gridSize_l = self.__grille.getSize()
		if self.__mainWindow != None :
			self.__progressBar.setGeometry(300, 300, 280, 30)
			size_l = self.__progressBar.geometry()
			fen_l = QtGui.QDesktopWidget().screenGeometry()
			self.__progressBar.move((fen_l.width()-size_l.width())/2, (fen_l.height()-size_l.height())/2)
			self.__progressBar.setRange(0,100)
			self.__progressBar.setValue(0)
			self.__progressBar.show()
			self.__progressBar.update()
			self.__progressBar.setFocus()
		self.__nbTotBet = math.pow(3, gridSize_l)
		#print "Taille Grille : ", gridSize_l
		self.__currentBet = Bet(self)
		#self.__currentBet.setReturnRate2(self.__returnRate2)
		#self.__currentBet.setReturnRate3(self.__returnRate3)
		self.genCombinoBetRecurcive(0, 0)
		self.genCombinoBetRecurcive(0, 1)
		self.genCombinoBetRecurcive(0, 2)
		if self.__mainWindow != None :
			self.__progressBar.close()

	def genCombinoBetRecurcive(self, numGame_p, unNDeux_p):
		self.__currentBet.setChoice(numGame_p, betChoice[unNDeux_p])
		if numGame_p == (self.__grille.getSize() - 1) : # fin de grille
			if (self.__currentBet.getRoughEsp() > 1) or (self.__expectedEsperance == 0)  : # optimization
				self.__currentBet.updateEsperanceAndProba()
				if self.__currentBet.getNetEsperance(self) >= self.__expectedEsperance :
					self.__file.write(str(self.__currentBet))
					#self.__combinoBets.append(copy.deepcopy(self.__currentBet))
			#else :
				#print "optimzation"
			self.__nbGenBets += 1
			pct_l =  self.__nbGenBets / self.__nbTotBet * 100
			if pct_l > self.__indexDisplayPct :
				if self.__mainWindow != None :
					self.__progressBar.setValue(int(pct_l))
					self.__progressBar.update()
				else :
					self.__indexDisplayPct += 1
					print "%.0f pct" % pct_l
		else :	
			self.genCombinoBetRecurcive(numGame_p + 1, 0)
			self.genCombinoBetRecurcive(numGame_p + 1, 1)
			self.genCombinoBetRecurcive(numGame_p + 1, 2)
		return
	
	def __str__(self):
		output_l = ""
		for index_l in range(0, len(self.__combinoBets)) :
			output_l = ''.join((output_l, str(self.__combinoBets[index_l])))

		return output_l
