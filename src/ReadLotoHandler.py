#!/usr/bin/python
import os,string, sys
from ReadGridHandler import ReadGridHandler
from PySide.QtCore import  QUrl, QRegExp, QDateTime, QDate
from Match import Match
from CombinoTools import onlyascii
import string


class ReadLotoHandler(ReadGridHandler):

        def __init__(self):
                ReadGridHandler.__init__(self)
                return

        def handleHtmlPage(self, htmlPage):
                self._gridList = []
                #loto15rx = QRegExp("<option\\s*(selected=\"selected\"\\s*)value=\"(\/\\w*)*\/lf\\d*\/(\\d*)-grille-(\\d+)\/\">")
                loto15rx = QRegExp("<option\\s*value=\"(\/\\w*)*\/l\\w*-*f\\w*-*\\d*\/(\\d*)-grille-(\\d+)\/\"\\s*(selected=\"selected\"\\s*)>")
                #loto15rx = QRegExp("<option\\s*value=\"(\/\\w*)*\/l\\w*-*f\\w*-*\\d*\/(\\d*)-grille-(\\d+)\/\"\\s*(selected=\"selected\"\\s*)>")
                #loto15DateRx = QRegExp("\\d*\\s*du\\s*(\\d*\/\\d*\/\\d*)<\/option>")
                loto15DateRx = QRegExp("LF\\d*\\s*n.\\d*\\s*-\\s*(\\d*\/\\d*\/\\d*)*(auj\.)*\\s*\\w*\\s*(\\d*h\\d*)<\/option>")
                posi_encours = loto15rx.indexIn(str(htmlPage))
                print "posi_encours=%s" % posi_encours
                ngrille = loto15rx.cap(3)
                print "ngrille=%s" % ngrille
                posi = loto15DateRx.indexIn(str(htmlPage), posi_encours)
                date = loto15DateRx.cap(1)
                print "Date=%s" % date
                dmy = string.split(date, "/")
                print "dmy :%s" % str(dmy)
                qdatetime = QDateTime()
                try:
                        qdatetime.setDate(QDate(int("20"+dmy[2]), int(dmy[1]), int(dmy[0])))
                except IndexError:
                        qdatetime.setDate(QDateTime.currentDateTime().date())
                qdatetime = qdatetime.addDays(1).addSecs(-1) # next day
                epochDate = qdatetime.toMSecsSinceEpoch()/1000
                print "epochDate=%d" % epochDate
                tup = (ngrille, epochDate, 0)
                self._gridList.append(tup)
                loto15rx = QRegExp("<option value=\"(\\d+)\">")
                posi = 0
                posi = loto15rx.indexIn(str(htmlPage), posi+1)
                print "posi_2=%s" % posi
                while posi != -1 :#and posi < posi_encours:
                        ngrille = loto15rx.cap(1)
                        print "ngrille=%s" % ngrille
                        posi = loto15DateRx.indexIn(str(htmlPage), posi)
                        date = loto15DateRx.cap(1)
                        print "Date=%s" % date
                        dmy = string.split(date, "/")
                        qdatetime = QDateTime()
                        qdatetime.setDate(QDate(int("20"+dmy[2]), int(dmy[1]), int(dmy[0])))
                        qdatetime = qdatetime.addDays(1).addSecs(-1) # next day
                        epochDate = qdatetime.toMSecsSinceEpoch()/1000
                        print "epochDate=%d" % epochDate
                        tup = (ngrille, epochDate, 0)
                        self._gridList.append(tup)
                        posi = loto15rx.indexIn(str(htmlPage), posi+1)
                #print self._gridList

        def handleDistribHtmlPage(self, htmlPage):
                print "handleDistribHtmlPage"
                jackpot = int(self._gridList[self._index][2]) / 0.70
                self._grid.setJackpot(jackpot)
                self._grid.setNbPlayers(jackpot)
                htmlStrPage = filter(onlyascii, str(htmlPage))
                startOfGridString = "<div class=\"repart_inside\">"
                #teamString = "<td class=\"team\">((\\(?\\)?\\d*\\w*\\.?'?-?\\s*)*)<\/td>"
                teamString = "<span class=\"team\">((\\(?\\)?\\d*\\w*\\.?'?\\s*)*)\\s*-\\s*((\\(?\\)?\\d*\\w*\\.?'?\\s*)*)<\/span>"
                enfOfGridString = "<div class=\"legend_repart\">"
                loto15Teamrx = QRegExp(teamString)
                endOfGridRx = QRegExp(enfOfGridString)
                startOfGridRx = QRegExp(startOfGridString)
                posiEndOfGrid= endOfGridRx.indexIn(htmlStrPage, 0)
                repString = ">(\\d*,*\\d*)\\s*\%<"
                loto15Reprx = QRegExp(repString)
                index_l = 0
                total = 0
                posi = 0
                i = 0
                #try:
                if True :
                        posi= startOfGridRx.indexIn(htmlStrPage, posi+1)
                        posiMax = endOfGridRx.indexIn(htmlStrPage, posi+1)
                        print "posi = %d" % posi
                        posi= loto15Teamrx.indexIn(htmlStrPage, posi+1)
                        while posi != -1:
                                i+=1
                                print "indice %i" % i
                                team1 = loto15Teamrx.cap(1)
                                print "team1 = %s" % team1
                                team2 = loto15Teamrx.cap(3)
                                #posiMax= loto15Teamrx.indexIn(htmlStrPage, posi+1)
                                #if posiMax < 0:
                                        #posiMax = posiEndOfGrid
                                print "posi3 = %d" % posi
                                print "team2 = %s" % team2
                                match = Match(team1 + " vs " + team2)
                                match.setTeam1(team1)
                                match.setTeam2(team2)
                                posiInter= loto15Reprx.indexIn(htmlStrPage, posi+1)
                                print "posiInter = %d" % posiInter
                                print "posiMax = %d" % posiMax
                                if (posiInter > 0) and (posiInter <= posiMax) :
                                        posi = posiInter
                                        print "posi4 = %d" % posi
                                        p1 = float(loto15Reprx.cap(1).replace(",","."))
                                        posi= loto15Reprx.indexIn(htmlStrPage, posi+1)
                                        print "posi5 = %d" % posi
                                        pN = float(loto15Reprx.cap(1).replace(",","."))
                                        posi= loto15Reprx.indexIn(htmlStrPage, posi+1)
                                        print "posi6 = %d" % posi
                                        p2 = float(loto15Reprx.cap(1).replace(",","."))
                                        total = float(p1+pN+p2)
                                        r1 = p1/total*100
                                        r2 = p2/total*100
                                        rN = pN/total*100
                                        match.setRepartition(p1/total, pN/total, p2/total)
                                        print "match :\n %s" % match
                                self._grid.addGame(match)
                                print "game added : %d" % i
                                posi= loto15Teamrx.indexIn(htmlStrPage, posiInter+1)
                                print "posi1 = %d" % posi
                        print "%d grilles" % i
                        self._gridSize = i
                #except:
                        #msg = QMessageBox()
                        #msg.setText("Loading page error")
                        #msg.exec_()
                #self.__workbook1.save(self.__outPutFileName)
                return
