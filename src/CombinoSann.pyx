#!/usr/bin/python 
import os,string, sys
import copy
#import chardet
#### SPECIFIC IMPORT #####
#sys.path.append("../Import/xlrd-0.7.1")
#sys.path.append("../Import/xlwt-0.7.2")
#sys.path.append("../Import/pyexcelerator-0.6.4.1")

import xlrd
import xlwt
import Grille
import Match
from xlrd import open_workbook
from xlwt import Workbook,easyxf,Formula,Style
from Grille import Grille
from Match import Match

def onlyascii(char_p):
        if ord(char_p) <= 0 or ord(char_p) > 127:
                return ''
        else:
                return char_p

def isnumber(s):
        try:
                float(s)
                return True
        except ValueError:
                return False

class CombinoScann():

        def __init__(self):
                self.__grille = None

        def getGrille(self) :
                cdef :
                        float cote1_l = 0.0
                        float coteN_l = 0.0
                        float cote2_l = 0.0
                        float rep1_l = 0.0
                        float repN_l = 0.0
                        float rep2_l = 0.0
                        int currRow_l, nbRows_l
                        int currCol_l, nbCols_l


                return self.__grille




def open_excel_sheet():
        """ Opens a reference to an Excel WorkBook and Worksheet objects """
        workbook = Workbook()
        worksheet = workbook.add_sheet("Sheet 1")
        return workbook, worksheet

def write_excel_header(worksheet, title_cols):
        """ Write the header line into the worksheet """
        cno = 0
        for title_col in title_cols:
                worksheet.write(0, cno, title_col)
                cno = cno + 1
        return

def write_excel_row(worksheet, rowNumber, columnNumber):
        """ Write a non-header row into the worksheet """
        cno = 0
        for column in columns:
                worksheet.write(lno, cno, column)
                cno = cno + 1
        return

def save_excel_sheet(workbook, output_file_name):
        """ Saves the in-memory WorkBook object into the specified file """
        workbook.save(output_file_name)
        return

