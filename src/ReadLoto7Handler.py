#!/usr/bin/python
import os,string, sys
from ReadLotoHandler import ReadLotoHandler
from PySide.QtCore import QUrl
sys.path.append("../WinaScan/WinaScan/src/")


class ReadLoto7Handler(ReadLotoHandler):

        def __init__(self):
                ReadLotoHandler.__init__(self)
                print "Loto 7"
                self.gridName = "Loto7"
                print "L7: %s" % str(self)
                self._bookUrl = QUrl("http://www.pronosoft.com/fr/concours/repartition_lotofoot_7.php")
                self._gridSize = 15
                return

        def changeGrid(self, index):
                ReadLotoHandler.changeGrid(self, index)
                self._distributionUrl = "http://www.pronosoft.com/fr/concours/repartition_lotofoot.php?id7=%s" % self._gridList[index][0]
                print "distributionUrl=%s" % self._distributionUrl
                return
