#!/usr/bin/python
import os,string, sys
from PySide.QtCore import  QUrl, QRegExp, QDateTime
from PySide import  QtCore
sys.path.append("../WinaScan/WinaScan/src/")
from WSParser import onlyascii


class ReadGridHandler():

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
                print "index = %d" % index
                return

        def gridName(self):
                return self._gridName

        def gridList(self):
                return self._gridList

        def setGrid(self, grid):
                self._grid = grid

        def grid(self):
                return self._grid

        def gridSize(self):
                return self._gridSize

        def oddsUrl(self):
                url = self._oddsUrl
                epochDate = self._gridList[self._index][1]
                date = QDateTime()
                date.setMSecsSinceEpoch(int(epochDate)*1000)
                day = date.date().day()
                month = date.date().month()
                year = date.date().year()
                urlComplement = "?year=%d" % year
                urlComplement = urlComplement+ "&month=%d" % month
                urlComplement = urlComplement + "&day=%d" % day
                print "urlComplement"
                return self._oddsUrl+urlComplement

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
                for match in self._grid.matches():
                        team1Rx = QRegExp("><span>(\\w*\\'?\\s*-?)*(%s)(\\w*\\'?\\s*-?)*</span>\\s*-\\s*<span>\\s*((\\w*\\'?\\s*-?)*)</span><" % match.team1())
                        team1Rx.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
                        team2Rx = QRegExp("><span>\\s*(\\w*\\'?\\s*-?)*</span>\\s*-\\s*<span>(\\w*\\'?\\s*-?)*(%s)(\\w*\\'?\\s*-?)*</span><" % match.team2())
                        team2Rx.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
                        #team2Rx = QRegExp(match.team2())
                        teamXRx = team1Rx
                        posi = teamXRx.indexIn(strHtml)
                        if posi < 0:
                                print "-%s- not found" % match.team1()
                                print "-1- not found"
                                teamXRx = team2Rx
                                posi = teamXRx.indexIn(strHtml)
                        if posi >= 0:
                                print "-%s- found" % ''.join((teamXRx.cap(1), " vs " + teamXRx.cap(2)))
                                posi = oddsRx.indexIn(strHtml, posi)
                                oddStr1 = oddsRx.cap(1)
                                oddStr2 = oddsRx.cap(2)
                                oddStr3 = oddsRx.cap(3)
                                print "read odds1 = %s" % oddStr1
                                try :
                                        match.setCotes(float(oddsRx.cap(1)), float(oddsRx.cap(2)), float(oddsRx.cap(3)))
                                        team1 = filter(onlyascii, match.team1())
                                        team2 = filter(onlyascii, match.team2())
                                        print "Odds handling OK : %s" % team1 + " vs " + team2
                                        print "Odds handling OK : "
                                        match.setCotesDisponibles(True)
                                except:
                                        team1 = filter(onlyascii, match.team1())
                                        team2 = filter(onlyascii, match.team2())
                                        print "Odds handling OK : cant read odds for %s" % team1 + " vs " + team2
                        else:
                                print "-%s- not found" % match.team2()
                                #print "Odds handling KO %s not found" % str(match)
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
