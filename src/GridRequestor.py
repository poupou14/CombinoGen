#!/usr/bin/python
import sys
sys.path.insert(0, "/home/poupou/.local/lib/python2.7/site-packages/pyvirtualdisplay/")
import httplib
import time
from PySide.QtCore import QThread, Signal, QObject
from contextlib import closing
#from selenium.webdriver import Firefox # pip install selenium
from selenium.webdriver import Firefox # pip install selenium
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common import exceptions
from pyvirtualdisplay import Display

class DistribPageGeneratedSignal(QObject):
        sig = Signal(str)


class GridRequestor(QThread):
        def __init__(self, parent = None):
                QThread.__init__(self, parent)
                self.distribPageGenerated = DistribPageGeneratedSignal()
                self.__url = None
                self.__display = None

        def setUrl(self, url):
                self.__url = url

        def pass_bad_status_line_exc(wrapped_function):
            """
            Silently pass this exception `http.client.BadStatusLine` decorator
            """
            def _wrapper(*args, **kwargs):
                try:
                    result = wrapped_function(*args, **kwargs)
                except httplib.BadStatusLine, exceptions.WebDriverException:
                    return
                return result
            return _wrapper

        @pass_bad_status_line_exc
        def run(self):
                self.__display = Display(visible=0, size=(800, 600))
                self.__display.start()
                page_source = ""
                try :
                    # use firefox to get page with javascript generated content
                    with closing(Firefox()) as browser:
                        browser = Firefox()
                        browser.get(self.__url)
			time.sleep(3)
                        # wait for the page to load
                        WebDriverWait(browser, timeout=20)#.until(
                        #lambda x: x.find_element_by_id('someId_that_must_be_on_new_page'))
                        # store it to string variable
                        page_source = browser.page_source
                        self.distribPageGenerated.sig.emit(page_source)
                        self.__display.stop()
                        print "browser quit !!"
                        browser.quit()
                        print "End browser quit !!"

                except AttributeError, exceptions.WebDriverException:
                    print "browser quit AttributeError issue... don't care, go on !"
                    pass
                #print(page_source)
                #self.__display.delete()
