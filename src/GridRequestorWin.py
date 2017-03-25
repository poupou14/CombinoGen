#!/usr/bin/python
import os,string, sys
from PySide.QtCore import  QUrl, QThread, Signal, QObject
from selenium import webdriver
from splinter import Browser

class DistribPageGeneratedSignal(QObject):
        sig = Signal(str)


class GridRequestorWin(QThread):
        def __init__(self, parent = None):
                QThread.__init__(self, parent)
                self.distribPageGenerated = DistribPageGeneratedSignal()
                self.__url = None

        def setUrl(self, url):
                self.__url = url

        def run(self):
		chrome_options = webdriver.ChromeOptions()

		browser = Browser('chrome', options=chrome_options)

		browser.visit(self.__url)
                # wait for the page to load
                WebDriverWait(browser, timeout=20)#.until(
                page_source = ""
		page_source = browser.html
                browser.quit()

                #print(page_source)
                self.distribPageGenerated.sig.emit(page_source)
