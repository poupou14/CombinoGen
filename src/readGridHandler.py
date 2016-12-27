#!/usr/bin/python
import os,string, sys
from PySide.QtCore import  QUrl

class readGridHandler():

	def __init__(self):
		self._gridName = ""
		self._bookUrl = None
		self._gridList = []
		self._index = 0
		self._distributionUrl = ""

	def changeGrid(self, index):
		self._index = index
		return

	def gridList(self):
		return self._gridList

	def bookUrl(self):
		return self._bookUrl

	def distribUrl(self):
		return self._distributionUrl

	def handleHtmlPage(self, htmlPage):
		return

	def handleDistribHtmlPage(self, htmlPage):
		return

	def generateInputGrid(self):
		return

	def __str__(self):
		output_l = ""
		output_l = ''.join((output_l, "self.gridName:"))
		output_l = ''.join((output_l, str(self._gridName)))
		output_l = ''.join((output_l, "\nself.bookUrl:"))
		output_l = ''.join((output_l, str(self._bookUrl)))
		output_l = ''.join((output_l, "\nself.gridList:"))
		for grid in self._gridList :
			output_l = ''.join((output_l, str(grid)))

		return output_l
