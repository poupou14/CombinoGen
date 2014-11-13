#!/usr/bin/python 
import os,string, sys
import urllib
import time
import urllib2



class Bet():

	def __init__(self, grille_p): 
		self.__grille = grille_p
		self.__combin = []
		self.__esperance = 0.0
		self.__esperance_n_1 = 0.0
		self.__esperance_n_2 = 0.0
		self.__gainEst = 0.0
		self.__gainEst_n_1 = 0.0
		self.__gainEst_n_1_min = 0.0
		self.__gainEst_n_2 = 0.0
		self.__proba = 0.0
		self.__proba_n_1 = 0.0
		self.__proba_n_2 = 0.0
		self.__returnRate = 0.0
		self.__scndRankRate = 0.0
		self.__thirdRankRate = 0.0

	def setChoice(self, index_p, choice_p):
		#print "setChoice :", index_p, choice_p
		#print "taille combin :", len(self.__combin)
		if len(self.__combin) <= index_p :
			self.__combin.append(choice_p)
		else:
			self.__combin[index_p] = choice_p

	def getChoice(self, index_p):
		return self.__combin[index_p] 

	def setCombin(self, combin_p):
		self.__combin = combin_p
		self.updateEsperanceAndProba()

	def getRoughEsp(self):
		esperance_l = 1
		size_l = self.__grille.getSize()
		for index_l in range(0,size_l):
			bet_l = self.__combin[index_l]
			result_l = self.getResult(bet_l)
			# Proba first rank
			probaMatch_l = 1/self.__grille.getGame(index_l).getCotes(result_l)
			repartitionMatch_l = self.__grille.getGame(index_l).getRepartition(result_l)
			esperance_l = esperance_l * (probaMatch_l/repartitionMatch_l) 
	
		self.__esperance = esperance_l
		return esperance_l

	def updateEsperanceAndProba(self):
		esperance_l = 1
		gainEst_l = 1
		proba_l = 1
		self.__proba_n_1 = 0
		self.__proba_n_2 = 0
		proba_n_1_l = 1
		self.__gainEst_n_1 = 1
		self.__gainEst_n_2 = 1
		probaN_1_l = []
		gainEstN_1_l = []
		probaN_2_l = []
		gainEstN_2_l = []
		size_l = self.__grille.getSize()
		for index_l in range(0,size_l):
			probaN_2_l.append([0]*size_l)
			gainEstN_2_l.append([0]*size_l)
			bet_l = self.__combin[index_l]

			result_l = self.getResult(bet_l)

			# Proba first rank
			probaMatch_l = 1/self.__grille.getGame(index_l).getCotes(result_l)
			repartitionMatch_l = self.__grille.getGame(index_l).getRepartition(result_l)
			#esperance_l = esperance_l * (probaMatch_l/repartitionMatch_l) 
			if (self.__scndRankRate > 0) :
				# Proba and gain scnd rank
				probaN_1_l.append(proba_l * (1 - probaMatch_l)) 
				gainEstN_1_l.append(gainEst_l / (1 - repartitionMatch_l)) 
				for index_n_1_l in range(0, index_l) :
					gainEstN_1_l[index_n_1_l] = gainEstN_1_l[index_n_1_l] / repartitionMatch_l
					probaN_1_l[index_n_1_l] = probaN_1_l[index_n_1_l] * probaMatch_l

				#for index_n_1_l in range(0, index_l) :
			
			proba_l = proba_l * probaMatch_l
			gainEst_l = gainEst_l / repartitionMatch_l

		# Proba and gain third rank
		if (self.__thirdRankRate > 0) :
			for index_n_2_A_l in range(0, size_l) :
	#		if (index_n_1_l < size_l -1) :
				bet_n_2_A_l = self.__combin[index_n_2_A_l]
				result_n_2_A_l = self.getResult(bet_n_2_A_l)
				probaMatch_n_2_A_l =  1/self.__grille.getGame(index_n_2_A_l).getCotes(result_n_2_A_l)
				repartitionMatch_n_2_A_l = self.__grille.getGame(index_n_2_A_l).getRepartition(result_n_2_A_l)

				for index_n_2_B_l in range(index_n_2_A_l + 1, size_l) :
					proba_tmp_l = proba_l * (1 - probaMatch_n_2_A_l) / probaMatch_n_2_A_l
					gainEst_tmp_l = gainEst_l * repartitionMatch_n_2_A_l / (1 - repartitionMatch_n_2_A_l) 
					bet_n_2_B_l = self.__combin[index_n_2_B_l]
					result_n_2_B_l = self.getResult(bet_n_2_B_l)
					probaMatch_n_2_B_l = 1/self.__grille.getGame(index_n_2_B_l).getCotes(result_n_2_B_l)
					repartitionMatch_n_2_B_l = self.__grille.getGame(index_n_2_B_l).getRepartition(result_n_2_B_l)
					proba_tmp_l = proba_tmp_l * (1 - probaMatch_n_2_B_l) / probaMatch_n_2_B_l
					gainEst_tmp_l = gainEst_tmp_l * repartitionMatch_n_2_B_l / (1 - repartitionMatch_n_2_B_l) 
					gainEstN_2_l[index_n_2_A_l][index_n_2_B_l] = gainEst_tmp_l
					#probaN_2_l[index_n_1_l][index_n_2_l] = proba_tmp_l
					self.__proba_n_2 = self.__proba_n_2 + proba_tmp_l
					self.__gainEst_n_2 = self.__gainEst_n_2 + gainEst_tmp_l



		self.__proba = proba_l
		if (self.__scndRankRate > 0) :
			sommeInvGagnants_n_1 = 0
			sommeInvGagnants_n_1_max_l = 0
			sommeInvGagnants_n_2 = 0
			sommeInvGagnants_n_2_max_l = 0
			for index_n_1_l in range(0, size_l) :
				self.__proba_n_1 = self.__proba_n_1 + probaN_1_l[index_n_1_l]
				sommeInvGagnants_n_1 = sommeInvGagnants_n_1 + 1/gainEstN_1_l[index_n_1_l]
				sommeInvGagnants_n_1_max_l = max(sommeInvGagnants_n_1_max_l, 1/gainEstN_1_l[index_n_1_l])
				if self.__thirdRankRate > 0 :
					for index_n_2_l in range(0, size_l) :
						if (gainEstN_2_l[index_n_1_l][index_n_2_l] != 0) :
							sommeInvGagnants_n_2 = sommeInvGagnants_n_2 + 1/gainEstN_2_l[index_n_1_l][index_n_2_l]
							sommeInvGagnants_n_2_max_l = max(sommeInvGagnants_n_2_max_l, 1/gainEstN_2_l[index_n_1_l][index_n_2_l])
			gainEst_n_1_min_l = 1 / (sommeInvGagnants_n_1_max_l * size_l)
			gainEst_n_1_l = 1 / sommeInvGagnants_n_1
			#if sommeInvGagnants_n_2 != 0 :
				#gainEst_n_2_l = 1 / sommeInvGagnants_n_2
				#self.__gainEst_n_2 = gainEst_n_2_l
			#else :
				#self.__gainEst_n_2 = 0
			if sommeInvGagnants_n_2_max_l != 0 :
				gainEst_n_2_min_l = 2 / (sommeInvGagnants_n_2_max_l * (size_l-1) * size_l)
				self.__gainEst_n_2 = gainEst_n_2_min_l
			else :
				self.__gainEst_n_2 = 0
			if (size_l == 7) : # loto 7
				nbgagnantsMax_l = 1000000 / gainEst_n_1_min_l + 3000
				self.__gainEst_n_1_min = 1000000 / nbgagnantsMax_l
				nbgagnants_l = 1000000 / gainEst_n_1_l + 3000
				self.__gainEst_n_1 = 1000000 / nbgagnants_l
				esperance2ndMin_l = self.__gainEst_n_1_min * self.__proba_n_1
				self.__esperance_n_1_min = esperance2ndMin_l
				esperance2nd_l = self.__gainEst_n_1 * self.__proba_n_1
				self.__esperance_n_1 = esperance2nd_l
			else :
				self.__gainEst_n_1_min = gainEst_n_1_min_l
				esperance2ndMin_l = self.__gainEst_n_1_min * self.__proba_n_1
				self.__gainEst_n_1 = gainEst_n_1_l
				esperance2nd_l = self.__gainEst_n_1 * self.__proba_n_1
				self.__esperance_n_1 = esperance2nd_l
				esperance3rd_l = self.__gainEst_n_2 * self.__proba_n_2
				self.__esperance_n_2 = esperance3rd_l
		#self.__esperance = esperance_l
		# Dummy repartition (4%)
		if (size_l == 7) : # loto 7
			nbgagnants_l = 1000000/gainEst_l + 27 
			self.__gainEst = 1000000/nbgagnants_l 
		else :
			self.__gainEst = gainEst_l

	def getResult(self, bet_p) :
			if bet_p == '1' :
				result_l = 0
			elif bet_p == 'N' :
				result_l = 1
			elif bet_p == '2' :
				result_l = 2
			return result_l

	def getProba(self) :
		return self.__proba

	def getProbaN_1(self) :
		return self.__proba_n_1

	def getEsperance(self) :
		return self.__esperance
	
	def setReturnRate2(self, scndRankRate_p) :
		self.__scndRankRate = scndRankRate_p

	def setReturnRate3(self, thirdRankRate_p) :
		self.__thirdRankRate = thirdRankRate_p

	def getNetEsperance(self, returnRate_p, scndRankRate_p=0, thirdRankRate_p=0) :
		self.__returnRate = returnRate_p
		self.__scndRankRate = scndRankRate_p
		self.__thirdRankRate = thirdRankRate_p
		esperance_l = self.__esperance * returnRate_p + self.__esperance_n_1 * scndRankRate_p + self.__esperance_n_2 * thirdRankRate_p
		return esperance_l

	def __str__(self):
		output_l = ""
		for index_l in range(0, len(self.__combin)) :
			output_l = ''.join((output_l, self.__combin[index_l]))
			output_l = ''.join((output_l, "/"))

		output_l = ''.join((output_l, ";"))
		strProba_l =  "%.8f" % self.__proba
		output_l = ''.join((output_l, strProba_l))
		output_l = ''.join((output_l, ";"))
		netEsperance_l = self.__esperance * self.__returnRate
		strEsperance_l =  "%.4f" % netEsperance_l
		output_l = ''.join((output_l, strEsperance_l))
		output_l = ''.join((output_l, ";"))
		gainNet_l = self.__gainEst * self.__returnRate
		strGainEst_l =  "%.4f" % gainNet_l
		output_l = ''.join((output_l, strGainEst_l))
		if (self.__thirdRankRate > 0) :
			output_l = ''.join((output_l, ";"))
			strProba_n_1_l =  "%.8f" % self.__proba_n_1
			output_l = ''.join((output_l, strProba_n_1_l))
			output_l = ''.join((output_l, ";"))
			#gainNet_n_1_l = self.__gainEst_n_1 * self.__scndRankRate
			#netEsperance_n_1_l = self.__proba_n_1 * gainNet_n_1_l
			#strEsperance_n_1_l =  "%.8f" % netEsperance_n_1_l
			#output_l = ''.join((output_l, strEsperance_n_1_l))
			#output_l = ''.join((output_l, ";"))
			#strGainEst_n_1_l =  "%.8f" % gainNet_n_1_l
			#output_l = ''.join((output_l, strGainEst_n_1_l))
			#output_l = ''.join((output_l, ";"))
			gainNet_n_1_l = self.__gainEst_n_1_min * self.__scndRankRate
			netEsperance_n_1_l = self.__proba_n_1 * gainNet_n_1_l
			strEsperance_n_1_l =  "%.4f" % netEsperance_n_1_l
			output_l = ''.join((output_l, strEsperance_n_1_l))
			output_l = ''.join((output_l, ";"))
			strGainEst_n_1_l =  "%.2f" % gainNet_n_1_l
			output_l = ''.join((output_l, strGainEst_n_1_l))
			output_l = ''.join((output_l, ";"))
			strProba_n_2_l =  "%.8f" % self.__proba_n_2
			output_l = ''.join((output_l, strProba_n_2_l))
			output_l = ''.join((output_l, ";"))
			gainNet_n_2_l = self.__gainEst_n_2 * self.__thirdRankRate
			netEsperance_n_2_l = self.__proba_n_2 * gainNet_n_2_l
			strEsperance_n_2_l =  "%.4f" % netEsperance_n_2_l
			output_l = ''.join((output_l, strEsperance_n_2_l))
			output_l = ''.join((output_l, ";"))
			strGainEst_n_2_l =  "%.2f" % gainNet_n_2_l
			output_l = ''.join((output_l, strGainEst_n_2_l))
			output_l = ''.join((output_l, ";"))
			netEsperanceSum_l = netEsperance_l + netEsperance_n_1_l + netEsperance_n_2_l
			strNetEsperanceSum_l =  "%.4f" % netEsperanceSum_l
			output_l = ''.join((output_l, strNetEsperanceSum_l))
		elif (self.__scndRankRate > 0) :
			output_l = ''.join((output_l, ";"))
			strProba_n_1_l =  "%.8f" % self.__proba_n_1
			output_l = ''.join((output_l, strProba_n_1_l))
			output_l = ''.join((output_l, ";"))
			gainNet_n_1_l = self.__gainEst_n_1 * self.__scndRankRate
			#netEsperance_n_1_l = self.__proba_n_1 * gainNet_n_1_l
			#strEsperance_n_1_l =  "%.8f" % netEsperance_n_1_l
			#output_l = ''.join((output_l, strEsperance_n_1_l))
			#output_l = ''.join((output_l, ";"))
			#strGainEst_n_1_l =  "%.8f" % gainNet_n_1_l
			#output_l = ''.join((output_l, strGainEst_n_1_l))
			#output_l = ''.join((output_l, ";"))
			gainNet_n_1_l = self.__gainEst_n_1_min * self.__scndRankRate
			netEsperance_n_1_l = self.__proba_n_1 * gainNet_n_1_l
			strEsperance_n_1_l =  "%.4f" % netEsperance_n_1_l
			output_l = ''.join((output_l, strEsperance_n_1_l))
			output_l = ''.join((output_l, ";"))
			strGainEst_n_1_l =  "%.2f" % gainNet_n_1_l
			output_l = ''.join((output_l, strGainEst_n_1_l))
			output_l = ''.join((output_l, ";"))
			netEsperanceSum_l = netEsperance_l + netEsperance_n_1_l
			#netEsperanceSum_l = self.__esperance * self.__returnRate + self.__esperance_n_1 * self.__scndRankRate
			strNetEsperanceSum_l =  "%.4f" % netEsperanceSum_l
			output_l = ''.join((output_l, strNetEsperanceSum_l))
		output_l = ''.join((output_l, "\n"))
		return output_l.replace(".", ",")

		
