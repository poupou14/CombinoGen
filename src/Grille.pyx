#!/usr/bin/python 
import os,string, sys
import time
import copy

from Match import Match


class Grille():
	def __init__(self):
		self.__matches = []
		self.__firstRankRate = 0.55
		self.__scndRankRate = 0.45
		self.__thirdRankRate = 0.00
		self.__returnRate = 0.75
		self.__jackpot = 0
		self.__nbPlayers = 0

	def firstRankRate(self):
		return self.__firstRankRate

	def scndRankRate(self):
		return self.__scndRankRate

	def thirdRankRate(self):
		return self.__thirdRankRate

	def jackpot(self):
		return self.__jackpot

	def nbPlayers(self):
		return self.__nbPlayers

	def returnRate(self):
		return self.__returnRate

	def setFirstRankRate(self, rate):
		self.__firstRankRate = rate

	def setScndRankRate(self, rate):
		self.__scndRankRate = rate

	def setThirdRankRate(self, rate):
		self.__thirdRankRate = rate

	def setJackpot(self, jackpot):
		self.__jackpot = jackpot

	def setNbPlayers(self, nbPlayers):
		self.__nbPlayers = nbPlayers

	def setReturnRate(self, rate):
		self.__returnRate = rate

	def addGame(self, match_p):
		self.__matches.append(match_p)

	def getGame(self, index_p):
		return self.__matches[index_p]

	def getSize(self) :
		return len(self.__matches)

	def matches(self) :
		return self.__matches

	def __str__(self):
		stri = ''
		for match in self.__matches :
			stri = ''.join((stri, str(match)))
		return stri
