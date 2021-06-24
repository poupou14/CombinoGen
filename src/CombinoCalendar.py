#!/usr/bin/python
import os,string, sys
from PySide.QtCore import QDateTime, QDate, QTime

class CombinoCalendar():
    def __init__(self, jour_p, mois_p, annee_p, heure=0, min=0):
        self.__moisDlAnnee = ['janvier', 'fvrier', 'mars', 'avril', 'mai', 'juin', 'juillet', 'aot',
                              'septembre', 'octobre', 'novembre', 'dcembre']
        self.__jour = jour_p
        self.__annee = annee_p
        try:
            self.__mois = int(mois_p)
        except:
            if mois_p.isnumeric():
                self.__mois = mois_p
            elif self.__moisDlAnnee.index(mois_p) >= 0:
                self.__mois = self.__moisDlAnnee.index(mois_p) + 1
        self.__qdateTime = QDateTime(QDate(self.__annee, self.__mois, self.__jour))
        self.__qdateTime.setTime(QTime(heure, min, 0))

    def getDate(self):
        return self.__qdateTime.date()

    def epochDate(self):
        return self.__qdateTime.toMSecsSinceEpoch()
