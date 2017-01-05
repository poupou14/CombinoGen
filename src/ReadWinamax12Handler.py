#!/usr/bin/python
import os,string, sys
from ReadGridHandler import ReadGridHandler
from PySide.QtCore import  QUrl, QRegExp

class ReadWinamax12Handler(ReadGridHandler):

        def __init__(self):
                ReadGridHandler.__init__(self)
                print "Winamax 12"
                self.gridName = "Winamax 12"
                self.bookUrl = QUrl("https://www.winamax.fr/paris-sportifs-grilles/")
                self._gridSize = 12
                return

        def handleHtmlPage(self, htmlPage):
                self.gridList = []
                wina7rx = QRegExp("\"pool_id\":12000(\\d+)")
                posi = wina7rx.indexIn(str(htmlPage))
                self.gridList.append(wina7rx.cap(1))
                print "grille : %s" % self.gridList[0]
                while posi != -1 :
                        posi = wina7rx.indexIn(str(htmlPage), posi+1)
                        self.gridList.append(wina7rx.cap(1))

        def handleDistribHtmlPage(self, htmlPage):
                return

        def generateInputGrid(self):
                return
