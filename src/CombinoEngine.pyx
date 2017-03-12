#!/usr/bin/python 
import os,string, sys
from PySide import QtCore, QtGui
from PySide.QtCore import  Signal, Slot
from PySide.QtCore import *
from multiprocessing import Process, Lock, Queue
import math
import copy
from Bet import Bet

writeLock = Lock()
betChoice = ['1', 'N', '2']
headerWritten = False

class CombinoEngine(Process, QObject):
        #progressSig = Signal(int)
        #finishedSig = Signal()

        def __init__(self, grille_p, expectedEsperance_p, fileName_p, firstRecParam_p, progressQueue, parent = None):
                Process.__init__(self)
                QObject.__init__(self)
                self.exiting = False
                self.__grille = grille_p
                self.__combinoBets = []
                self.__nbTotBet = 0
                self.__nbGenBets = 0
                self.__currentBet = None
                self.__returnRate = grille_p.returnRate() * grille_p.firstRankRate()
                self.__returnRate2 = grille_p.scndRankRate() * grille_p.returnRate()
                self.__returnRate3 = grille_p.thirdRankRate() * grille_p.returnRate()
                self.__expectedEsperance = expectedEsperance_p
                self.__progressQueue = progressQueue
                self.__fileName = fileName_p
                self.__firstRecParam = firstRecParam_p
                self.__file = None
                self.__jackpot = grille_p.jackpot()
                self.__nbPlayers = grille_p.nbPlayers()
                self.__cancel = False

        def getGrille(self):
                return self.__grille

        def getReturnRate(self):
                return self.__returnRate

        def getReturnRate2(self):
                return self.__returnRate2

        def getReturnRate3(self):
                return self.__returnRate3

        def getJackpot(self):
                return self.__jackpot

        def getNbPlayers(self):
                return self.__nbPlayers


        def run(self):
                gridSize_l = self.__grille.getSize()
                self.__nbTotBet = math.pow(3, gridSize_l)
                print "Grille : %s " % self.__grille
                self.__currentBet = Bet(self)
                try:
                    os.remove(self.__fileName)
                except OSError:
                    print "file already removed"
                print "fileName =%s" % self.__fileName
                #if (not headerWritten):
                        #self.__file.write("Game;Proba-Rg1;Esp-Rg1;Estim-Rg1;Proba-Rg2;Esp-Rg2;Estim-Rg2;Proba-Rg3;Esp-Rg3;Estim-Rg3;Esp-tot\n")
                        #headerWritten = True

                #self.__currentBet.setReturnRate2(self.__returnRate2)
                #self.__currentBet.setReturnRate3(self.__returnRate3)
                self.genCombinoBetRecurcive(0, self.__firstRecParam)
                #self.genCombinoBetRecurcive(0, 1)
                #self.genCombinoBetRecurcive(0, 2)
                #self.finishedSig.emit()
                print "closing %s" % self.__fileName


        def genCombinoBetRecurcive(self, int numGame_p, int unNDeux_p):
                cdef:
                        float pct_l = 0.0
                        int   pctInt = 0
                if self.__cancel:
                        return
                self.__currentBet.setChoice(numGame_p, betChoice[unNDeux_p])
                if numGame_p == (self.__grille.getSize() - 1) : # fin de grille
                        if (self.__currentBet.getRoughEsp() > 1) or (self.__expectedEsperance == 0)  : # optimization
                                self.__currentBet.updateEsperanceAndProba()
                                if self.__currentBet.getNetEsperance(self) >= self.__expectedEsperance :
                                        writeLock.acquire()
                                        self.__file=open(self.__fileName, 'a+')
                                        self.__file.write(str(self.__currentBet))
                                        self.__file.close()
                                        writeLock.release()
                                        #self.__combinoBets.append(copy.deepcopy(self.__currentBet))
                        #else :
                                #print "optimzation"
                        pctInt =  int(self.__nbGenBets / self.__nbTotBet * 100)
                        self.__nbGenBets += 1
                        pct_l =  self.__nbGenBets / self.__nbTotBet * 100
                        if int(pct_l) > pctInt :
                                #self.progressSig.emit(int(pct_l))
                                if not self.__progressQueue.empty():
                                    prog = self.__progressQueue.get() + 1
                                    self.__progressQueue.put(prog)
                                else :
                                    print "empty Queue pid=%d" % os.getpid()
                                #print "%.0f PCT" % pct_l
                else :
                        self.genCombinoBetRecurcive(numGame_p + 1, 0)
                        self.genCombinoBetRecurcive(numGame_p + 1, 1)
                        self.genCombinoBetRecurcive(numGame_p + 1, 2)
                return

        def cancelGen(self):
                print "cancelGen slot"
                self.__cancel = True

        def __str__(self):
                cdef int index_l
                output_l = ""
                for index_l in range(0, len(self.__combinoBets)) :
                        output_l = ''.join((output_l, str(self.__combinoBets[index_l])))

                return output_l
