#!/usr/bin/python 
import os,string, sys
import xlwt
from xlrd import open_workbook
from xlwt import Workbook,easyxf,Formula,Style
#from lxml import etree
import xlrd
from Match import Match
from CombinoTools import onlyascii


class Grille():
        def __init__(self):
                self.__matches = []
                self.__firstRankRate = 0.55
                self.__scndRankRate = 0.45
                self.__thirdRankRate = 0.00
                self.__returnRate = 0.75
                self.__jackpot = 0
                self.__nbPlayers = 0
                self.__workbook1 = None

        def export(self, fileName):
                workbook1 = Workbook()
                grilleSheet = workbook1.add_sheet("Grille", cell_overwrite_ok=True)
                configSheet = workbook1.add_sheet("Config", cell_overwrite_ok=True)
                grilleSheet.write(0, 4, "Pct1")
                grilleSheet.write(0, 5, "PctN")
                grilleSheet.write(0, 6, "Pct2")
                grilleSheet.write(0, 8, "C1")
                grilleSheet.write(0, 9, "CN")
                grilleSheet.write(0, 10, "C2")
                grilleSheet.write(0, 11, "CTot")
                i = 0
                while i < self.getSize():
                    grilleSheet.write(i+1, 0, "%d." % (i+1))
                    grilleSheet.write(i+1, 1, filter(onlyascii, self.getGame(i).team1()))
                    grilleSheet.write(i+1, 2, "/")
                    grilleSheet.write(i+1, 3, filter(onlyascii, self.getGame(i).team2()))
                    grilleSheet.write(i+1, 4, self.getGame(i).getRepartition(0))
                    grilleSheet.write(i+1, 5, self.getGame(i).getRepartition(1))
                    grilleSheet.write(i+1, 6, self.getGame(i).getRepartition(2))
                    total = self.getGame(i).getRepartition(0) + self.getGame(i).getRepartition(1) + self.getGame(i).getRepartition(2)
                    grilleSheet.write(i+1, 7, total)
                    grilleSheet.write(i+1, 8, self.getGame(i).getCotes(0))
                    grilleSheet.write(i+1, 9, self.getGame(i).getCotes(1))
                    grilleSheet.write(i+1, 10, self.getGame(i).getCotes(2))
                    ret = 1/self.getGame(i).getCotes(0) + 1/self.getGame(i).getCotes(1) + 1/self.getGame(i).getCotes(2)
                    grilleSheet.write(i+1, 11, ret)
                    i += 1

                configSheet.write(0, 0, "Return rate")
                configSheet.write(1, 0, "First rank")
                configSheet.write(2, 0, "Scnd rank")
                configSheet.write(3, 0, "Third rank")
                configSheet.write(0, 1, self.__returnRate)
                configSheet.write(1, 1, self.__firstRankRate)
                configSheet.write(2, 1, self.__scndRankRate)
                configSheet.write(3, 1, self.__thirdRankRate)
                configSheet.write(0, 2, "Jackpot")
                configSheet.write(1, 2, "Nb players")
                configSheet.write(0, 3, self.__jackpot)
                configSheet.write(1, 3, self.__nbPlayers)
                workbook1.save(fileName)
                print "Exported to %s" % fileName
                return



        def firstRankRate(self):
                return self.__firstRankRate

        def scndRankRate(self):
                return self.__scndRankRate

        def thirdRankRate(self):
                return self.__thirdRankRate

        def jackpot(self):
                return self.__jackpot

        def nbPlayers(self):
                return self.__nbPlayers

        def returnRate(self):
                return self.__returnRate

        def setFirstRankRate(self, rate):
                self.__firstRankRate = rate

        def setScndRankRate(self, rate):
                self.__scndRankRate = rate

        def setThirdRankRate(self, rate):
                self.__thirdRankRate = rate

        def setJackpot(self, jackpot):
                self.__jackpot = jackpot

        def setNbPlayers(self, nbPlayers):
                self.__nbPlayers = nbPlayers

        def setReturnRate(self, rate):
                self.__returnRate = rate

        def addGame(self, match_p):
                self.__matches.append(match_p)

        def getGame(self, index_p):
                return self.__matches[index_p]

        def getSize(self) :
                return len(self.__matches)

        def matches(self) :
                return self.__matches

        def __str__(self):
                stri = ""
                stri = ''.join((stri, "returnRate = %f" % self.__returnRate))
                stri = ''.join((stri, "firstRankRate = %f" % self.__firstRankRate))
                stri = ''.join((stri, "scndRankRate = %f" % self.__scndRankRate))
                stri = ''.join((stri, "thirdRankRate = %f" % self.__thirdRankRate))
                stri = ''.join((stri, "nbPlayers = %d" % self.__nbPlayers))
                stri = ''.join((stri, "Jackpot = %f" % self.__jackpot))
                for match in self.__matches :
                        stri = ''.join((stri, str(match)))
                        stri = ''.join((stri, "\n"))
                return stri
