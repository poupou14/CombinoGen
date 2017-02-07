#!/usr/bin/python 
import os,string, sys
from CombinoTools import onlyascii

class Match():
        def __init__(self, affiche_p ):
                self.__affiche = affiche_p
                self.__repartition = [33.0, 34.0, 33.0]
                self.__cotes = [3.0, 3.0, 3.0]
                self.__invSum = 1
                self.__team1 = None
                self.__team2 = None
                self.__cotesDisponibles = False

        def setTeam1(self, team1):
                self.__team1 = team1

        def setTeam2(self, team2):
                self.__team2 = team2

        def cotesDisponibles(self):
                return self.__cotesDisponibles

        def setCotesDisponibles(self, dispo):
                self.__cotesDisponibles = dispo

        def team1(self):
                return self.__team1

        def team2(self):
                return self.__team2

        def setRepartition(self, un_p, n_p, deux_p) :
                # Standard modification rep
                rep1_l = un_p
                rep2_l = deux_p
                repN_l = n_p
                total = rep1_l+repN_l+rep2_l
                self.__repartition[0] = rep1_l/total
                self.__repartition[1] = repN_l/total
                self.__repartition[2] = rep2_l/total


        def setCotes(self, cote1_p, coteN_p, cote2_p) :
                self.__invSum = 1/cote1_p + 1/coteN_p + 1/cote2_p
                self.__cotes[0] = cote1_p * self.__invSum
                self.__cotes[1] = coteN_p * self.__invSum
                self.__cotes[2] = cote2_p * self.__invSum

        def getRepartition(self, index_p) :
                return self.__repartition[index_p]

        def getCotes(self, index_p) :
                return self.__cotes[index_p]

        def __str__(self):
                str = filter(onlyascii, self.__affiche)
                str = ''.join((str, " %2.2f pct" % self.__repartition[0]))
                str = ''.join((str, " %2.2f pct" % self.__repartition[1]))
                str = ''.join((str, " %2.2f pct" % self.__repartition[2]))
                str = ''.join((str, " - %2.2f" % self.__cotes[0]))
                str = ''.join((str, " %2.2f" % self.__cotes[1]))
                str = ''.join((str, " %2.2f" % self.__cotes[2]))
                return str
