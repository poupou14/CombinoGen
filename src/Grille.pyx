#!/usr/bin/python 
import os,string, sys
import time
import copy

from Match import Match


class Grille():
	def __init__(self):
		self.__matches = []

	def addGame(self, match_p):
		self.__matches.append(match_p)

	def getGame(self, index_p):
		return self.__matches[index_p]

	def getSize(self) :
		return len(self.__matches)

