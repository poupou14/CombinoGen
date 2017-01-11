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
                tup = ()
                self._gridList = []
                loto15rx = QRegExp("<option selected=\"selected\" value=\"(\\d+)\">")
                loto15DateRx = QRegExp("\\d*\\s*du\\s*(\\d*\/\\d*\/\\d*)<\/option>")
                posi_encours = loto15rx.indexIn(str(htmlPage))
                ngrille = loto15rx.cap(1)
                print "ngrille=%s" % ngrille
                posi = loto15DateRx.indexIn(str(htmlPage), posi_encours)
                date = loto15DateRx.cap(1)
                print "Date=%s" % date
                dmy = string.split(date, "/")
                qdatetime = QDateTime()
                qdatetime.setDate(QDate(int("20"+dmy[2]), int(dmy[1]), int(dmy[0])))
                epochDate = qdatetime.toMSecsSinceEpoch()/1000
                print "epochDate=%d" % epochDate
                tup = (ngrille, epochDate, 0)
                self._gridList.append(tup)
                loto15rx = QRegExp("<option value=\"(\\d+)\">")
                posi = 0
                while posi != -1 and posi < posi_encours:
                        posi = loto15rx.indexIn(str(htmlPage), posi+1)
                        ngrille = loto15rx.cap(1)
                        print "ngrille=%s" % ngrille
                        posi = loto15DateRx.indexIn(str(htmlPage), posi)
                        date = loto15DateRx.cap(1)
                        print "Date=%s" % date
                        dmy = string.split(date, "/")
                        qdatetime = QDateTime()
                        qdatetime.setDate(QDate(int("20"+dmy[2]), int(dmy[1]), int(dmy[0])))
                        epochDate = qdatetime.toMSecsSinceEpoch()/1000
                        print "epochDate=%d" % epochDate
                        tup = (ngrille, epochDate, 0)
                        self._gridList.append(tup)
                #print self._gridList

        def handleDistribHtmlPage(self, htmlPage):
                print "handleDistribHtmlPage"
                jackpot = int(self._gridList[self._index][2]) / 0.70
                self._grid.setJackpot(jackpot)
                self._grid.setNbPlayers(jackpot)
                htmlStrPage = filter(onlyascii, str(htmlPage))
                teamString = "<td class=\"center matchs_av\">((\\w*\.?\\s*)*)<\/td>"
                loto15Teamrx = QRegExp(teamString)
                repString = ">(\\d*,*\\d*)\\s*\%<"
                loto15Reprx = QRegExp(repString)
                index_l = 0
                total = 0
                posi = 0
                i = 0
                #try:
                if True :
                        posi= loto15Teamrx.indexIn(htmlStrPage, posi+1)
                        print "posi = %d" % posi
                        while posi != -1:
                                i+=1
                                team1 = loto15Teamrx.cap(1)
                                posi= loto15Teamrx.indexIn(htmlStrPage, posi+1)
                                print "posi2 = %d" % posi
                                print "posi2 = %d" % posi
                                print "team1 = %s" % team1
                                team2 = loto15Teamrx.cap(1)
                                print "posi3 = %d" % posi
                                print "indice %i" % i
                                print "team2 = %s" % team2
                                match = Match(team1 + " vs " + team2)
                                match.setTeam1(team1)
                                match.setTeam2(team2)
                                posi= loto15Reprx.indexIn(htmlStrPage, posi+1)
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
                                self._grid.addGame(match)
                                print "game added : %d" % i
                                posi= loto15Teamrx.indexIn(htmlStrPage, posi+1)
                                print "posi1 = %d" % posi
                        print "%d grilles" % i
                        self._gridSize = i
                #except:
                        #msg = QMessageBox()
                        #msg.setText("Loading page error")
                        #msg.exec_()
                #self.__workbook1.save(self.__outPutFileName)
                return
