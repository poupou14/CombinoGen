#!/usr/bin/python
import os,string, sys
from PySide.QtCore import  QUrl, QRegExp

class readGridHandler():

	def __init__(self):
		self._gridName = ""
		self._bookUrl = None
		self._oddsUrl = "http://www.betexplorer.com/next/soccer/"
		self._gridList = []
		self._index = 0
		self._gridSize = 0
		self._grid = None
		self._distributionUrl = ""

	def changeGrid(self, index):
		self._index = index
		return

	def gridList(self):
		return self._gridList

	def grid(self):
		return self._grid

	def gridSize(self):
		return self._gridSize

	def oddsUrl(self):
		return self._oddsUrl

	def bookUrl(self):
		return self._bookUrl

	def distribUrl(self):
		return self._distributionUrl

	def handleHtmlPage(self, htmlPage):
		return

	def handleDistribHtmlPage(self, htmlPage):
		return

	def handleOddsHtmlPage(self, htmlPage):
		strHtml = str(htmlPage)
		oddsRx = QRegExp("<a href=.*data-odd-max=\"(\\d*\.\\d*)\".*data-odd-max=\"(\\d*\.\\d*)\".*data-odd-max=\"(\\d*\.\\d*)\".*>")
		for match in self._grid.matches() :
			team1Rx = QRegExp(match.team1())
			team2Rx = QRegExp(match.team2())
			posi = team1Rx.indexIn(strHtml)
			if posi < 0:
				posi = team1Rx.indexIn(strHtml)
			if posi >= 0:
				posi = oddsRx.indexIn(strHtml, posi)
				oddStr1 = oddsRx.cap(1)
				oddStr2 = oddsRx.cap(2)
				oddStr3 = oddsRx.cap(3)
				print "read odds1 = %s" % oddStr1
				try :
					match.setCotes(float(oddsRx.cap(1)), float(oddsRx.cap(2)), float(oddsRx.cap(3)))
					print "Odds handling OK : %s" % str(match)
				except:
					print "Odds handling KO for %s, cant read odds" % str(match)
			else:
				print "Odds handling KO %s not found" % str(match)

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
