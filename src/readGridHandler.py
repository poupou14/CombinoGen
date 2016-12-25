#!/usr/bin/python
import os,string, sys
from PySide.QtCore import  QUrl

class readGridHandler():

	def __init__(self):
		self.gridName = ""
		self.bookUrl = None
		self.gridList = []
		self.index = 0
		self.distributionUrl = ""

	def changeGrid(self, index):
		self.index = index
		return

	def handleHtmlPage(self, htmlPage):
		return

	def __str__(self):
		output_l = ""
		output_l = ''.join((output_l, "self.gridName:"))
		output_l = ''.join((output_l, str(self.gridName)))
		output_l = ''.join((output_l, "\nself.bookUrl:"))
		output_l = ''.join((output_l, str(self.bookUrl)))
		output_l = ''.join((output_l, "\nself.gridList:"))
		for grid in self.gridList :
			output_l = ''.join((output_l, str(grid)))

		return output_l
