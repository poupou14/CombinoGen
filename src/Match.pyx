#!/usr/bin/python 
import os,string, sys
import time
import copy


class Match():
	def __init__(self, affiche_p ):
		self.__affiche = affiche_p
		self.__repartition = [33.0, 34.0, 33.0]
		self.__cotes = [3.0, 3.0, 3.0]
		self.__invSum = 1

	def setRepartition(self, un_p, n_p, deux_p) :
		self.__repartition[0] = un_p
		self.__repartition[1] = n_p
		self.__repartition[2] = deux_p


	def setCotes(self, cote1_p, coteN_p, cote2_p) :
		self.__invSum = 1/cote1_p + 1/coteN_p + 1/cote2_p
		self.__cotes[0] = cote1_p * self.__invSum
		self.__cotes[1] = coteN_p * self.__invSum
		self.__cotes[2] = cote2_p * self.__invSum

	def getRepartition(self, index_p) :
		return self.__repartition[index_p]

	def getCotes(self, index_p) :
		return self.__cotes[index_p]
