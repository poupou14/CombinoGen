#!/usr/bin/python
import os,string, sys
from ReadLotoHandler import ReadLotoHandler
from PySide.QtCore import QUrl
sys.path.append("../WinaScan/WinaScan/src/")
from Grille import Grille


class ReadLoto8Handler(ReadLotoHandler):

        def __init__(self):
                ReadLotoHandler.__init__(self)
                print "Loto 8"
                self._gridName = "Loto8"
                print "L8: %s" % str(self)
                self._bookUrl = QUrl("https://www.pronosoft.com/fr/lotofoot/repartition/lf7/")
                self._gridSize = 8
                self._grid = Grille()
                self._grid.setReturnRate(0.70)
                self._grid.setFirstRankRate(0.45)
                self._grid.setScndRankRate(0.55)
                self._grid.setThirdRankRate(0.00)
                return

        def changeGrid(self, index):
                ReadLotoHandler.changeGrid(self, index)
                self._distributionUrl = "http://www.pronosoft.com/fr/concours/repartition_lotofoot.php?id7=%s" % self._gridList[index][0]
                print "distributionUrl=%s" % self._distributionUrl
                return

