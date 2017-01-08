#!/usr/bin/python
import os,string, sys
from ReadGridHandler import ReadGridHandler
from PySide.QtCore import  QUrl, QRegExp
from PySide.QtGui import  QMessageBox
from PySide.QtNetwork import  *
sys.path.append("../WinaScan/WinaScan/src/")
from WSParser import WSGridParser, onlyascii
from Grille import Grille
from Match import Match
from WSDataFormat import WSDataFormat

class ReadWinamax7Handler(ReadGridHandler):

        def __init__(self):
                ReadGridHandler.__init__(self)
                print "Winamax7"
                self._gridName = "Winamax7"
                print "W7: %s" % str(self)
                self._gridSize = 7
                self._bookUrl = QUrl("https://www.winamax.fr/paris-sportifs-grilles/")
                return

        def handleHtmlPage(self, htmlPage):
                tup = ()
                self._gridList = []
                wina7rx = QRegExp("\{\"pool_id\":7000(\\d+).*\"pool_end\":(\\d+).*\"guaranteed_amount\":(\\d+).*\}")
                posi = wina7rx.indexIn(str(htmlPage))
                ngrille = wina7rx.cap(1)
                print "ngrille=%s" % ngrille
                #self.gridList.append(wina7rx.cap(1))
                date = wina7rx.cap(2)
                print "date=%s" % date
                jackpot = wina7rx.cap(3)
                print "jackpot=%s" % jackpot
                tup = (ngrille, date, jackpot)
                self._gridList.append(tup)
                while posi != -1 :
                        posi = wina7rx.indexIn(str(htmlPage), posi+1)
                        ngrille = wina7rx.cap(1)
                        print "ngrille=%s" % ngrille
                        date = wina7rx.cap(2)
                        print "date=%s" % date
                        jackpot = wina7rx.cap(3)
                        print "jackpot=%s" % jackpot
                        tup = (ngrille, date, jackpot)
                        self._gridList.append(tup)
                print self._gridList

        def handleDistribHtmlPage(self, htmlPage):
                self._grid = Grille()
                self._grid.setReturnRate(0.75)
                self._grid.setFirstRankRate(0.55)
                self._grid.setScndRankRate(0.45)
                jackpot = int(self._gridList[self._index][2]) / 0.75
                self._grid.setJackpot(jackpot)
                self._grid.setNbPlayers(jackpot)
                #print "handleDistribHtmlPage"
                #print htmlPage
                myParser = WSGridParser()
                myParser.html = filter(onlyascii, htmlPage)
                myParser.feed(htmlPage)
                index_l = 0
                total = 0
                size_l = 7
                try:
                    for i in range(0, size_l) :
                        print "indice %i" % i
                        team1 = myParser.wsDataFormat.grille['team1'][i]
                        team2 = myParser.wsDataFormat.grille['team2'][i]
                        match = Match(team1 + " vs " + team2)
                        match.setTeam1(team1)
                        match.setTeam2(team2)
                        p1 = myParser.wsDataFormat.grille['croix_1'][i]
                        pN = myParser.wsDataFormat.grille['croix_x'][i]
                        p2 = myParser.wsDataFormat.grille['croix_2'][i]
                        total = float(p1+pN+p2)
                        r1 = p1/total*100
                        r2 = p2/total*100
                        rN = pN/total*100
                        match.setRepartition(p1/total, pN/total, p2/total)
                        #print "{} vs {} \t{0:.3f}\t{0:.3f}\t{0:.3f}\n".format( WSDataFormat.grille['team1'][i], WSDataFormat.grille['team2'][i], r1, rN, r2)
                        #print "{} vs {}\t{:10.3f}\t{:10.3f}\t{:10.3f} ".format( myParser.wsDataFormat.grille['team1'][i].encode('utf-8'), myParser.wsDataFormat.grille['team2'][i].encode('utf-8'), r1,rN,r2)
                        self._grid.addGame(match)
                    print "%d grilles" % total
                except:
                        msg = QMessageBox()
                        msg.setText("Loading page error")
                        msg.exec_()
                #self.__workbook1.save(self.__outPutFileName)
                return

        def generateInputGrid(self):
                return


        def changeGrid(self, index):
                ReadGridHandler.changeGrid(self, index)
                self._distributionUrl = "https://www.winamax.fr/paris-sportifs-grilles/grille7-%s/grilles-publiques" % self._gridList[index][0]
                print "distributionUrl=%s" % self._distributionUrl
                return
