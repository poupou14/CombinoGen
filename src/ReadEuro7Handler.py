#!/usr/bin/python
import os,string, sys
from ReadGridHandler import ReadGridHandler
from PySide.QtNetwork import  *
from WSParser import WSGridParser, onlyascii
from PySide.QtCore import QUrl, QRegExp, QDateTime, QDate
from Grille import Grille
from Match import Match
from CombinoCalendar import CombinoCalendar
from CombinoTools import onlyascii


class ReadEuro7Handler(ReadGridHandler):

        def __init__(self):
                ReadGridHandler.__init__(self)
                print "Euro7"
                self._gridName = "Euro7"
                print "E7: %s" % str(self)
                self._gridSize = 7
                self._bookUrl = QUrl("https://www.france-pari.fr/grilles/type/4")
                return

        def handleHtmlPage(self, htmlPage):
                tup = ()
                self._gridList = []
                htmlAscii = filter(onlyascii, str(htmlPage))
                #print "html = %s" % htmlAscii
                euro7NumGrillerx = QRegExp("<div class=\"grid grid-4\" data-grid-id=\"(\\d+)\" data-grid-type=\"4\">")
                euro7DateRx = QRegExp("<span\\s*class=\"date\">[\\s\\n\\r]*(\\w+)\\s*(\\d+)\\s*(\\w+)\\s*(\\d+)\\s*.{0,6}\\s*(\\d+):(\\d+)\\s*</span>")
                euro7JackpotRx = QRegExp("<p class=\"montant-jackpot\">Jackpot\\s*garanti\\s*<span>\\s*(\\d+)")
                posi = euro7NumGrillerx.indexIn(str(htmlAscii))
                ngrille = euro7NumGrillerx.cap(1)
                print "ngrille=%s" % ngrille
                posi = euro7DateRx.indexIn(str(htmlAscii), posi+1)
                jour = euro7DateRx.cap(1)
                numJour = euro7DateRx.cap(2)
                mois = euro7DateRx.cap(3)
                annee = euro7DateRx.cap(4)
                heure = euro7DateRx.cap(5)
                minute = euro7DateRx.cap(6)
                mois = filter(onlyascii, mois)
                print "jour=%s" % jour
                print "mois=%s" % mois
                print "annee=%s" % annee
                print "heure=%s" % heure
                print "minute=%s" % minute
                date = CombinoCalendar(int(numJour), mois, int(annee), int(heure), int(minute))
                epochDate = date.epochDate()/1000
                print "date=%s" % (jour + str(numJour) + mois + str(annee))
                print "epochDate=%d" % epochDate
                #self.gridList.append(euro7rx.cap(1))
                posi = euro7JackpotRx.indexIn(str(htmlAscii), posi+1)
                jackpot = euro7JackpotRx.cap(1)
                print "jackpot=%s" % jackpot
                tup = (ngrille, epochDate, jackpot)
                self._gridList.append(tup)
                posi = euro7NumGrillerx.indexIn(str(htmlAscii), posi+1)
                while posi != -1 :
                        ngrille = euro7NumGrillerx.cap(1)
                        print "ngrille=%s" % ngrille
                        posi = euro7DateRx.indexIn(str(htmlAscii), posi+1)
                        jour = euro7DateRx.cap(1)
                        numJour = euro7DateRx.cap(2)
                        mois = euro7DateRx.cap(3)
                        annee = euro7DateRx.cap(4)
                        heure = euro7DateRx.cap(5)
                        minute = euro7DateRx.cap(6)
                        mois = filter(onlyascii, mois)
                        print "jour=%s" % jour
                        print "mois=%s" % mois
                        print "annee=%s" % annee
                        print "heure=%s" % heure
                        print "minute=%s" % minute
                        print "date=%s" % (jour + str(numJour) + mois + str(annee))
                        date = CombinoCalendar(int(numJour), mois, int(annee), int(heure), int(minute))
                        epochDate = date.epochDate()/1000
                        print "epochDate=%d" % epochDate
                        posi = euro7JackpotRx.indexIn(str(htmlAscii), posi+1)
                        jackpot = euro7JackpotRx.cap(1)
                        print "jackpot=%s" % jackpot
                        tup = (ngrille, epochDate, jackpot)
                        self._gridList.append(tup)
                        posi = euro7NumGrillerx.indexIn(str(htmlAscii), posi+1)
                print self._gridList

        def handleDistribHtmlPage(self, htmlPage):
                euro7startRx = QRegExp("data-grid-id=\"(\\d*)\"")
                indexGrille = ""
                posi = 0
                while posi != -1 and indexGrille != self._gridList[self._indexGrille][0]:
                    print "posi = %d" % posi
                    print "indexGrille = %s" % indexGrille
                    print "self._indexGrille = %s" % self._gridList[self._indexGrille][0]
                    posi= euro7startRx.indexIn(htmlPage, posi+1)
                    indexGrille = euro7startRx.cap(1)
                euro7TeamRx = QRegExp("<label for=\"[^\"]*\">([^<]*)<\/label>")
                self._grid = Grille()
                self._grid.setReturnRate(0.75)
                self._grid.setFirstRankRate(0.55)
                self._grid.setScndRankRate(0.45)
                jackpot = int(self._gridList[self._index][2])
                self._grid.setJackpot(jackpot)
                self._grid.setNbPlayers(jackpot)
                index_l = 0
                total = 0
                #size_l = 5
                i=0
                #try:
                if True:
                    posi= euro7TeamRx.indexIn(htmlPage, posi)
                    print "posi = %d" % posi
                    while posi != -1 and i < self._gridSize:
                        i += 1
                        team1 = euro7TeamRx.cap(1)
                        print "team1 = %s" % team1
                        posi= euro7TeamRx.indexIn(htmlPage, posi+1)
                        posi= euro7TeamRx.indexIn(htmlPage, posi+1)
                        team2 = euro7TeamRx.cap(1)
                        print "indice %i" % i
                        print "team2 = %s" % team2
                        match = Match(team1 + " vs " + team2)
                        match.setTeam1(team1)
                        match.setTeam2(team2)
                        p1 = 0.33
                        pN = 0.33
                        p2 = 0.33
                        total = p1 + pN +p2
                        r1 = p1/total*100
                        r2 = p2/total*100
                        rN = pN/total*100
                        match.setRepartition(p1/total, pN/total, p2/total)
                        self._grid.addGame(match)
                        print "game added : %d" % i
                        posi= euro7TeamRx.indexIn(htmlPage, posi+1)
                #except:
                        #msg = QMessageBox()
                        #msg.setText("Loading page error")
                        #msg.exec_()
                #self.__workbook1.save(self.__outPutFileName)
                return

        def generateInputGrid(self):
                return


        def changeGrid(self, index):
                ReadGridHandler.changeGrid(self, index)
                self._indexGrille = index
                self._distributionUrl = "https://www.france-pari.fr/grilles/type/4"
                print "distributionUrl=%s" % self._distributionUrl
                return
