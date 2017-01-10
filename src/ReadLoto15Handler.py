#!/usr/bin/python
import os,string, sys
from ReadLotoHandler import ReadLotoHandler
from PySide.QtCore import  QUrl, QRegExp, QDateTime, QDate
sys.path.append("../WinaScan/WinaScan/src/")
from Grille import Grille


class ReadLoto15Handler(ReadLotoHandler):

        def __init__(self):
                ReadLotoHandler.__init__(self)
                print "Loto 15"
                self._gridName = "Loto15"
                print "L15: %s" % str(self)
                self._bookUrl = QUrl("http://www.pronosoft.com/fr/concours/repartition_lotofoot.php")
                self._gridSize = 15
                self._grid = Grille()
                self._grid.setReturnRate(0.70)
                self._grid.setFirstRankRate(0.40)
                self._grid.setScndRankRate(0.20)
                self._grid.setThirdRankRate(0.20)
                jackpot = int(self._gridList[self._index][2]) / 0.70
                self._grid.setJackpot(jackpot)
                self._grid.setNbPlayers(jackpot)
                return

        def changeGrid(self, index):
                ReadLotoHandler.changeGrid(self, index)
                self._distributionUrl = "http://www.pronosoft.com/fr/concours/repartition_lotofoot.php?id15=%s" % self._gridList[index][0]
                print "distributionUrl=%s" % self._distributionUrl
                return

