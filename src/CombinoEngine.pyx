#!/usr/bin/python 
import os,string, sys
from PySide import QtCore, QtGui
from PySide.QtCore import  Signal, Slot
from PySide.QtCore import *
import math
import copy
from Bet import Bet

betChoice = ['1', 'N', '2']

class CombinoEngine(QThread):
	progressSig = Signal(int)
	finishedSig = Signal()

	def __init__(self, grille_p, returnRate_p, expectedEsperance_p, file_p, jackpot_p, nbPlayers_p, scndRankRate_p=0, thirdRankRate_p=0, mainWindow_p=None, parent = None): 
		QThread.__init__(self, mainWindow_p)
		self.exiting = False
		self.__grille = grille_p
		self.__combinoBets = []
		self.__nbTotBet = 0
		self.__nbGenBets = 0
		self.__currentBet = None
		self.__returnRate = returnRate_p
		self.__returnRate2 = scndRankRate_p
		self.__returnRate3 = thirdRankRate_p
		self.__expectedEsperance = expectedEsperance_p
		self.__file = file_p
		self.__jackpot = jackpot_p
		self.__nbPlayers = nbPlayers_p
		self.__cancel = False
		mainWindow_p.stopGenSig.connect(self.cancelGen)

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


	def run(self):
		gridSize_l = self.__grille.getSize()
		self.__nbTotBet = math.pow(3, gridSize_l)
		#print "Taille Grille : ", gridSize_l
		self.__currentBet = Bet(self)
		#self.__currentBet.setReturnRate2(self.__returnRate2)
		#self.__currentBet.setReturnRate3(self.__returnRate3)
		self.genCombinoBetRecurcive(0, 0)
		self.genCombinoBetRecurcive(0, 1)
		self.genCombinoBetRecurcive(0, 2)
		self.finishedSig.emit()

	def genCombinoBetRecurcive(self, int numGame_p, int unNDeux_p):
		cdef:
			float pct_l = 0.0
			int   pctInt = 0
		if self.__cancel:
			return
		self.__currentBet.setChoice(numGame_p, betChoice[unNDeux_p])
		if numGame_p == (self.__grille.getSize() - 1) : # fin de grille
			if (self.__currentBet.getRoughEsp() > 1) or (self.__expectedEsperance == 0)  : # optimization
				self.__currentBet.updateEsperanceAndProba()
				if self.__currentBet.getNetEsperance(self) >= self.__expectedEsperance :
					self.__file.write(str(self.__currentBet))
					#self.__combinoBets.append(copy.deepcopy(self.__currentBet))
			#else :
				#print "optimzation"
			pctInt =  int(self.__nbGenBets / self.__nbTotBet * 100)
			self.__nbGenBets += 1
			pct_l =  self.__nbGenBets / self.__nbTotBet * 100
			if int(pct_l) > pctInt :
				self.progressSig.emit(int(pct_l))
				#print "%.0f PCT" % pct_l
		else :	
			self.genCombinoBetRecurcive(numGame_p + 1, 0)
			self.genCombinoBetRecurcive(numGame_p + 1, 1)
			self.genCombinoBetRecurcive(numGame_p + 1, 2)
		return
	def cancelGen(self):
		print "cancelGen slot"
		self.__cancel = True

	def __str__(self):
		cdef int index_l
		output_l = ""
		for index_l in range(0, len(self.__combinoBets)) :
			output_l = ''.join((output_l, str(self.__combinoBets[index_l])))

		return output_l