#!/usr/bin/python
import os, string, sys
from PySide.QtCore import QUrl, QRegExp, QDateTime
from PySide import QtCore

sys.path.append("../WinaScan/WinaScan/src/")
from WSParser import onlyascii

BETEXPLORER_SOURCE = 0
ZULUBET_SOURCE = 1


class ReadGridHandler():
    def __init__(self):
        self._gridName = ""
        self._bookUrl = None
        self._oddsUrl = "http://www.betexplorer.com/next/soccer/"
        self._oddsUrl2 = "http://www.zulubet.com/tips-"
        self._gridList = []
        self._index = 0
        self._gridSize = 0
        self._grid = None
        self._distributionUrl = ""

    def writeHtmlToFile(self, html):
        try:
            # This will create a new file or **overwrite an existing file**.
            f = open("html.out", "w")
            try:
                f.write(html) # Write a string to a file
            finally:
                f.close()
        except IOError:
            pass

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

    @property
    def oddsUrl(self):
        url = self._oddsUrl
        epochDate = self._gridList[self._index][1]
        date = QDateTime()
        date.setMSecsSinceEpoch(int(epochDate) * 1000)
        day = date.date().day()
        month = date.date().month()
        year = date.date().year()
        urlComplement = "?year=%d" % year
        urlComplement = urlComplement + "&month=%d" % month
        urlComplement = urlComplement + "&day=%d" % day
        print "urlComplement=%s" % urlComplement
        return self._oddsUrl + urlComplement

    def oddsUrl2(self, dayMore=0):
        url = self._oddsUrl2
        epochDate = self._gridList[self._index][1]
        date = QDateTime()
        date.setMSecsSinceEpoch(int(epochDate) * 1000)
        print "date = %s" % date
        date = date.addDays(dayMore)
        print "date + dayMore = %s" % date
        day = date.date().day()
        month = date.date().month()
        year = date.date().year()
        urlComplement = "{0}-{1}-{2}.html".format(day, month, year)
        return self._oddsUrl2 + urlComplement

    def bookUrl(self):
        return self._bookUrl

    def distribUrl(self):
        return self._distributionUrl

    def handleHtmlPage(self, htmlPage):
        return

    def handleDistribHtmlPage(self, htmlPage):
        return

    def handleOddsHtmlPage(self, htmlPage, source=BETEXPLORER_SOURCE):
        print "handleOddsHtmlPage source = %d" % source
        epochDate = self._gridList[self._index][1]
        date = QDateTime()
        date.setMSecsSinceEpoch(int(epochDate) * 1000)
        deprecated = QDateTime.currentDateTime() > date.addDays(+1)

        strHtml = str(htmlPage)
        if source == BETEXPLORER_SOURCE:
            oddsRx = QRegExp(
                "<a href=.*data-odd-max=\"(\\d*\.\\d*)\".*data-odd-max=\"(\\d*\.\\d*)\".*data-odd-max=\"(\\d*\.\\d*)\".*>")
        elif source == ZULUBET_SOURCE:
            oddsRx = QRegExp(
                "<td\\s*class=\"aver_odds_full\"\\s*align=\"center\">(\\d*\.\\d*)</td><td\\s*class=\"aver_odds_full\"\\s*align=\"center\">(\\d*\.\\d*)</td><td\\s*class=\"aver_odds_full\"\\s*align=\"center\">(\\d*\.\\d*)</td>")

        for match in self._grid.matches():
            if not match.cotesDisponibles():
                if source == BETEXPLORER_SOURCE and not deprecated:
                    team1Rx = QRegExp(
                        "><span>(\\w*[\\'\\.-]?\\s*)*(%s)(\\w*[\\'\\.-]?\\s*)*</span>\\s*-\\s*<span>\\s*((\\w*[\\'\\.-]?\\s*)*)</span><" % match.team1())
                    team1Rx.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
                    team2Rx = QRegExp(
                        "><span>\\s*(\\w*[\\'\\.-]?\\s*)*</span>\\s*-\\s*<span>(\\w*[\\'\\.-]?\\s*)*(%s)(\\w*[\\'\\.-]?\\s*)*</span><" % match.team2())
                    team2Rx.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
                elif source == ZULUBET_SOURCE:
                    team1Rx = QRegExp(
                        #"<img\\s*src=\"http://www\.zulubet\.com/flags/flag-\\w*\.png\"\\s*class=\"flags\\s*flag-\\w*\"\\s*title=\"(\\w*\\'?\\s*-?)*,(\\w*\\'?\\s*-?)*\"\\s*width=\"\\d*\"\\s*height=\"\\d*\">\\s*(%s)\\s*-\\s*(\\w*\\'?\\s*-?)*<\img>" % match.team1())
                        "width=\"\\d*\"\\s*height=\"\\d*\">\\s*(%s)\\s*-\\s*(\\w*[\\'\\.-]?\\s*)*</td>" % match.team1())
                    team1Rx.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
                    team2Rx = QRegExp(
                        "width=\"\\d*\"\\s*height=\"\\d*\">(\\w*[\\'\\.-]?\\s*)*-\\s*(%s)\\s*</td>" % match.team2())
                    team2Rx.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
                else:
                    team1Rx = QRegExp("---deprecated---")
                    team2Rx = QRegExp("---deprecated---")

                # team2Rx = QRegExp(match.team2())
                teamXRx = team1Rx
                posi = teamXRx.indexIn(strHtml)
                posi2 = team2Rx.indexIn(strHtml)
                #if posi < 0:
                    #print "-1-%s- not found" % match.team1()
                    #teamXRx = team2Rx
                    #posi = teamXRx.indexIn(strHtml)
                #if (posi >= 0) and (posi2 >= 0):
                if (posi >= 0) and (posi2 == posi):
                    print "-%s- found" % ''.join((match.team1(), " vs " + match.team2()))
                else:  # try in an other way
                    print "-%s- not found, try another way" % ''.join((match.team1(), " vs " + match.team2()))
                    # split team names
                    team1list = match.team1().split(" ")
                    team2list = match.team2().split(" ")
                    # find the longest
                    maxLen = 0
                    miniTeam1 = ""
                    for elt1 in team1list:
                        if len(elt1) > maxLen:
                            maxLen = len(elt1)
                            miniTeam1 = filter(onlyascii, elt1)
                    maxLen = 0
                    miniTeam2 = ""
                    for elt2 in team2list:
                        if len(elt2) > maxLen:
                            maxLen = len(elt2)
                            miniTeam2 = filter(onlyascii, elt2)
                    print "Try with {0} vs {1}".format(miniTeam1, miniTeam2)
                    if source == BETEXPLORER_SOURCE and not deprecated:
                        teamRx = QRegExp(
                            "><span>\\s*(\\w*\\'?\\s*-?)*{0}(\\w*\\'?\\s*-?)*</span>\\s*-\\s*<span>(\\w*\\'?\\s*-?)*{1}(\\w*\\'?\\s*-?)*</span><".format(
                                miniTeam1, miniTeam2))
                    elif source == ZULUBET_SOURCE:
                        #teamRx = QRegExp(
                            #"<img\\s*src=\"http://www\.zulubet\.com/flags/flag-\\w*\.png\"\\s*class=\"flags\\s*flag-\\w*\"\\s*title=\"(\\w*\\'?\\s*-?)*,(\\w*\\'?\\s*-?)*\"\\s*width=\"\\d*\"\\s*height=\"\\d*\">(\\w*\\'?\\s*-?)*{0}(\\w*\\'?\\s*-?)*-(\\w*\\'?\\s*-?)*{1}(\\w*\\'?\\s*-?)*<\img>".format(
                                #miniTeam1, miniTeam2))
                        teamRx = QRegExp("\">(\\w*\\'?\\s*-?)*{0}(\\w*\\'?\\s*-?)*-(\\w*\\'?\\s*-?)*{1}(\\w*\\'?\\s*-?)*</td>".format(miniTeam1, miniTeam2))
                    else:
                        teamRx = QRegExp("---deprecated---")
                        print "---GRID DEPRECATED---"

                    teamRx.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
                    posi = teamRx.indexIn(strHtml)
                    if posi >= 0:
                        print "found : {0} vs {1}".format(miniTeam1, miniTeam2)
                    else:
                        print "still not found :'("
                        # print "Odds handling KO %s not found" % str(match)
                if posi >= 0:
                    print "posi = %d" % posi
                    posi = oddsRx.indexIn(strHtml, posi)
                    oddStr1 = oddsRx.cap(1)
                    oddStr2 = oddsRx.cap(2)
                    oddStr3 = oddsRx.cap(3)
                    print "read odds1 = %s" % oddStr1
                    try:
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
        for grid in self._gridList:
            output_l = ''.join((output_l, str(grid)))

        return output_l
