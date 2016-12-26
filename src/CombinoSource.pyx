#!/usr/bin/python 
import os,string, sys
import copy
#import chardet
#### SPECIFIC IMPORT #####
#sys.path.append("../Import/xlrd-0.7.1")
#sys.path.append("../Import/xlwt-0.7.2")
#sys.path.append("../Import/pyexcelerator-0.6.4.1")

from pyExcelerator import *
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

class CombinoSource():

	def __init__(self, fileName_p): 
		self.__workbook = open_workbook(fileName_p)
		self.__grille = None
		self.__worksheet = self.__workbook.sheet_by_name('Grille')
		try :
			self.__worksheetConfig = self.__workbook.sheet_by_name('Config')
		except :	
			self.__worksheetConfig = None
		
	def getReturnRate(self) :
		currRow_l = 0 
		currCol_l = 1 
		returnRate_l = 0.7
		if (self.__worksheetConfig != None) :
			cellValue_l = self.__worksheetConfig.cell_value(currRow_l, currCol_l)
			returnRate_l = float(cellValue_l)
		return returnRate_l
	
	def getNbPlayers(self) :
		currRow_l = 1 
		currCol_l = 3 
		nbPlayers_l = -1
		if (self.__worksheetConfig != None) :
			try :
				cellValue_l = self.__worksheetConfig.cell_value(currRow_l, currCol_l)
				nbPlayers_l = float(cellValue_l)
			except (ValueError, IndexError) :
				nbPlayers_l = -1
	
		return nbPlayers_l

	def getJackpot(self) :
		currRow_l = 0 
		currCol_l = 3 
		jackpot_l = -1
		if (self.__worksheetConfig != None) :
			try :
				cellValue_l = self.__worksheetConfig.cell_value(currRow_l, currCol_l)
				jackpot_l = float(cellValue_l)
			except (ValueError, IndexError) :
				jackpot_l = -1
	
		return jackpot_l

	def getScndRankRate(self) :
		currRow_l = 2 
		currCol_l = 1 
		scndRankRate_l = -1
		if (self.__worksheetConfig != None) :
			try :
				cellValue_l = self.__worksheetConfig.cell_value(currRow_l, currCol_l)
				scndRankRate_l = float(cellValue_l)
			except (ValueError, IndexError) :
				scndRankRate_l = -1
	
		return scndRankRate_l

	def getFirstRankRate(self) :
		currRow_l = 1 
		currCol_l = 1 
		firstRankRate_l = 0.45
		if (self.__worksheetConfig != None) :
			cellValue_l = self.__worksheetConfig.cell_value(currRow_l, currCol_l)
			firstRankRate_l = float(cellValue_l)
		return firstRankRate_l

	def getThirdRankRate(self) :
		currRow_l = 3 
		currCol_l = 1 
		thirdRankRate_l = -1
		if (self.__worksheetConfig != None) :
			try :
				cellValue_l = self.__worksheetConfig.cell_value(currRow_l, currCol_l)
				thirdRankRate_l = float(cellValue_l)
			except (ValueError, IndexError) :
				thirdRankRate_l = -1
	
		return thirdRankRate_l


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

		self.__grille = Grille()
		nbRows_l = self.__worksheet.nrows - 1
		nbCols_l = self.__worksheet.ncols - 1
		currRow_l = 0 # forget title line
		while currRow_l < nbRows_l:
			matchTitle_l = ""
			currRow_l += 1
			row_l = self.__worksheet.row(currRow_l)
			print 'Row:', currRow_l
			if self.__worksheet.cell_type(currRow_l, 0) != 0 : # not emty cell
				currCol_l = 0 # first col unused
				while currCol_l < nbCols_l:
					currCol_l += 1
					# Cell Types: 0=Empty, 1=Text, 2=Number, 3=Date, 4=Boolean, 5=Error, 6=Blank
					cellType_l = self.__worksheet.cell_type(currRow_l, currCol_l)
					cellValue_l = self.__worksheet.cell_value(currRow_l, currCol_l)
					print '	', cellType_l, ':', cellValue_l
					if currCol_l <= 3 :
						matchTitle_l = ''.join((matchTitle_l, cellValue_l))
					elif currCol_l == 4 :
						currMatch_l = Match(matchTitle_l)
						rep1_l= float(cellValue_l)
						rep1_l = rep1_l + 0.02
					elif currCol_l == 5 :
						repN_l = float(cellValue_l)
						repN_l = repN_l + 0.02
					elif currCol_l == 6 :
						rep2_l = float(cellValue_l)
						rep2_l = rep2_l + 0.02
						repTot_l = rep1_l + repN_l + rep2_l
						rep1_l = rep1_l / repTot_l
						repN_l = repN_l / repTot_l
						rep2_l = rep2_l / repTot_l
						currMatch_l.setRepartition(rep1_l, repN_l, rep2_l)
					elif currCol_l == 8 :
						cote1_l= float(cellValue_l)
					elif currCol_l == 9 :
						coteN_l = float(cellValue_l)
					elif currCol_l == 10 :
						cote2_l = float(cellValue_l)
						coteTot_l = 1/cote1_l + 1/coteN_l + 1/cote2_l
						cote1_l = cote1_l / coteTot_l
						coteN_l = coteN_l / coteTot_l
						cote2_l = cote2_l / coteTot_l
						currMatch_l.setCotes(cote1_l, coteN_l, cote2_l)

				self.__grille.addGame(copy.deepcopy(currMatch_l))

			else :
				nbRows_l = currRow_l
		
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

