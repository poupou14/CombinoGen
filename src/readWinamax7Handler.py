#!/usr/bin/python
import os,string, sys
from readGridHandler import readGridHandler
from PySide.QtCore import  QUrl, QRegExp
from PySide.QtNetwork import  *
sys.path.append("../WinaScan/WinaScan/src/")
from WSParser import WSGridParser, onlyascii
import WSDataFormat

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
		print "handleDistribHtmlPage"
		print htmlPage
		myParser = WSGridParser()
		myParser.html = filter(onlyascii, htmlPage)
		myParser.feed(htmlPage)
		index_l = 0
		total = 0
		size_l = 7
		for i in range(0, size_l) :
			p1 = WSDataFormat.grille['croix_1'][i]
			pN = WSDataFormat.grille['croix_x'][i]
			p2 = WSDataFormat.grille['croix_2'][i]
			total = float(p1+pN+p2)
			r1 = p1/total*100
			r2 = p2/total*100
			rN = pN/total*100
			#print "{} vs {} \t{0:.3f}\t{0:.3f}\t{0:.3f}\n".format( WSDataFormat.grille['team1'][i], WSDataFormat.grille['team2'][i], r1, rN, r2)
			print "{} vs {}\t{:10.3f}\t{:10.3f}\t{:10.3f} ".format( WSDataFormat.grille['team1'][i].encode('utf-8'), WSDataFormat.grille['team2'][i].encode('utf-8'), r1,rN,r2)
		print "%d grilles" % total
		#self.__workbook1.save(self.__outPutFileName)
		return

	def generateInputGrid(self):
		return


	def changeGrid(self, index):
		readGridHandler.changeGrid(self, index)
		self._distributionUrl = "https://www.winamax.fr/paris-sportifs-grilles/grille7-%s/grilles-publiques" % self._gridList[index][0]
		print "distributionUrl=%s" % self._distributionUrl
		return
