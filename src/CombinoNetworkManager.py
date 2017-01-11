#!/usr/bin/python
import os,string, sys
from PySide.QtCore import  QUrl, QThread, Signal, QObject
from PySide.QtNetwork import *


class Singleton:
        def __init__(self, decorated):
                self._decorated = decorated

        def Instance(self):
                try:
                        return self._instance
                except AttributeError:
                        self._instance = self._decorated()
                        return self._instance

        def __call__(self):
                raise TypeError('Singletons must be accessed through `Instance()`.')

        def __instancecheck__(self, inst):
                return isinstance(inst, self._decorated)

@Singleton
class CombinoNetworkManager:
        def __init__(self):
                self.manager = QNetworkAccessManager()
                self.__url = None

        def setUrl(self, url):
                self.__url = url

        def get(self):
                print "set url : %s" % self.__url
                request = QNetworkRequest(self.__url)
                print "get method"
                reponse = self.manager.get(request)
                print "get method done"
                return

