#!/usr/bin/python
import os,string, sys
from readGridHandler import readGridHandler
from PySide.QtCore import  QUrl, QRegExp
from PySide.QtNetwork import  *

class readWinamax7Handler(readGridHandler):

	def __init__(self):
		readGridHandler.__init__(self)
		print "Winamax 7"
		self._gridName = "Winamax 7"
		self._bookUrl = QUrl("https://www.winamax.fr/paris-sportifs-grilles/")
		print "W7: %s" % str(self)
		return

	def handleHtmlPage(self, htmlPage):
		tup = ()
		self._gridList = []
		wina7rx = QRegExp("\{\"pool_id\":7000(\\d+).*\"pool_end\":(\\d+).*\}")
		posi = wina7rx.indexIn(str(htmlPage))
		ngrille = wina7rx.cap(1)
		print "ngrille=%s" % ngrille
		#self.gridList.append(wina7rx.cap(1))
		date = wina7rx.cap(2)
		print "date=%s" % date
		tup = (ngrille, date)
		self._gridList.append(tup)
		while posi != -1 :
			posi = wina7rx.indexIn(str(htmlPage), posi+1)
			ngrille = wina7rx.cap(1)
			print "ngrille=%s" % ngrille
			date = wina7rx.cap(2)
			print "date=%s" % date
			tup = (ngrille, date)
			self._gridList.append(tup)
		print self._gridList

	def handleDistribHtmlPage(self, htmlPage):
		return

	def generateInputGrid(self):
		return


	def changeGrid(self, index):
		readGridHandler.changeGrid(self, index)
		self._distributionUrl = "https://www.winamax.fr/paris-sportifs-grilles/grille7-%s/grilles-publiques" % self.gridList[index][0]
		print "distributionUrl=%s" % self._distributionUrl
		return
