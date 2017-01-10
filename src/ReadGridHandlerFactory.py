#!/usr/bin/python
import os,string, sys
from CombinoSource import CombinoSource
from Grille import Grille
from ReadGridHandler import ReadGridHandler
from ReadWinamax12Handler import ReadWinamax12Handler
from ReadWinamax7Handler import ReadWinamax7Handler
from ReadLoto7Handler import ReadLoto7Handler
from ReadLoto15Handler import ReadLoto15Handler

class ReadGridHandlerFactory:
        def __init__(self):
                pass

        def createGridHandler(self, inputFile):
                source = CombinoSource(inputFile)
                grille = source.getGrille()
                if grille.getSize() == 7 and source.getReturnRate() == 0.75 and source.getFirstRankRate() == 0.55:
                        print "Factory generate Wina7"
                        return_l = ReadWinamax7Handler()
                elif grille.getSize() == 12:
                        print "Factory generate Wina12"
                        return_l = ReadWinamax12Handler()
                if grille.getSize() == 7 and source.getReturnRate() == 0.70 and source.getFirstRankRate() == 0.45:
                        print "Factory generate Loto7"
                        return_l = ReadLoto7Handler()
                if grille.getSize() == 14 and source.getReturnRate() == 0.70 and source.getFirstRankRate() == 0.40:
                        print "Factory generate Loto15"
                        return_l = ReadLoto15Handler()
                else:
                        print "Factory generate None !!!"
                        return None
                print "Factory grille : %s" % str(grille)
                return_l.setGrid(grille)

                return return_l



