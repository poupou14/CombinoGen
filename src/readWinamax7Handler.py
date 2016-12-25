#!/usr/bin/python
import os,string, sys
from readGridHandler import readGridHandler
from PySide.QtCore import  QUrl, QRegExp

class readWinamax7Handler(readGridHandler):

	def __init__(self):
		readGridHandler.__init__(self)
		print "Winamax 7"
		self.gridName = "Winamax 7"
		self.bookUrl = QUrl("https://www.winamax.fr/paris-sportifs-grilles/")
		print "W7: %s" % str(self)
		return

	def handleHtmlPage(self, htmlPage):
		tup = ()
		self.gridList = []
		wina7rx = QRegExp("\{\"pool_id\":7000(\\d+).*\"pool_end\":(\\d+).*\}")
		posi = wina7rx.indexIn(str(htmlPage))
		ngrille = wina7rx.cap(1)
		print "ngrille=%s" % ngrille
		#self.gridList.append(wina7rx.cap(1))
		date = wina7rx.cap(2)
		print "date=%s" % date
		tup = (ngrille, date)
		self.gridList.append(tup)
		while posi != -1 :
			posi = wina7rx.indexIn(str(htmlPage), posi+1)
			ngrille = wina7rx.cap(1)
			print "ngrille=%s" % ngrille
			date = wina7rx.cap(2)
			print "date=%s" % date
			tup = (ngrille, date)
			self.gridList.append(tup)
		print self.gridList


	def changeGrid(self, index):
		readGridHandler.changeGrid(self, index)
		self.distributionUrl = "https://www.winamax.fr/paris-sportifs-grilles/grille7-%s/grilles-publiques" % self.gridList[index][0]
		print "distributionUrl=%s" % self.distributionUrl
		return
