#!/usr/bin/python 
import os,string, sys
import urllib
import time
import urllib2


class Bet:
	def __init__(self, myCombinoEngine_p): 
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
		self.__engine = myCombinoEngine_p
		self.__combin = []
		self.__returnRate = myCombinoEngine_p.getReturnRate()
		self.__scndRankRate = myCombinoEngine_p.getReturnRate2()
		self.__thirdRankRate = myCombinoEngine_p.getReturnRate3()

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
		cdef int result_l
		cdef int index_l
		result_l = -1
		grille_l = self.__engine.getGrille() 
		esperance_l = 1
		size_l = grille_l.getSize()
		for index_l in range(0,size_l):
			bet_l = self.__combin[index_l]
			result_l = self.getResult(bet_l)
			# Proba first rank
			probaMatch_l = 1/grille_l.getGame(index_l).getCotes(result_l)
			repartitionMatch_l = grille_l.getGame(index_l).getRepartition(result_l)
			esperance_l = esperance_l * (probaMatch_l/repartitionMatch_l) 
	
		self.__esperance = esperance_l
		return esperance_l

	def getResult(self, bet_p) :
		cdef int result_l
		result_l = -1
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

	def getNetEsperance(self, combinoEngine_p) :
		esperance_l = self.__esperance * self.__returnRate + self.__esperance_n_1 * self.__scndRankRate + self.__esperance_n_2 * self.__thirdRankRate
		return esperance_l

	def __str__(self):
		cdef int index_l
		output_l = ""
		for index_l in range(0, len(self.__combin)) :
			output_l = ''.join((output_l, self.__combin[index_l]))
			output_l = ''.join((output_l, "/"))

		output_l = ''.join((output_l, ";"))
		strProba_l =  "%.8f" % self.__proba
		output_l = ''.join((output_l, strProba_l))
		output_l = ''.join((output_l, ";"))
		netEsperance_l = self.__esperance * self.__returnRate
		#netEsperance_l = self.__gainEst * self.__proba * self.__returnRate
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

		
	def updateEsperanceAndProba(self):
		cdef:
			int result_l, index2ndRank_l, size_l, index_l, index_n_2_A_l, index_n_2_B_l
			double esperance_l,gainEst_l,proba_l, proba_n_1_l, cote2ndRank_l,result2ndRank_l, probaMatch_l, repartitionMatch_l, proba_tmp_l, probaMatch_n_2_A_l, probaMatch_n_2_B_l, esperance2ndMin_l, esperance2nd_l, esperance3rd_l, gainEst_tmp_l, gainEst_n_1_l, gainEst_n_2_l, gainEst_n_2_min_l, repartitionMatch_n_2_A_l, repartitionMatch_n_2_B_l, sommeInvGagnants_n_1, sommeInvGagnants_n_1_max_l, sommeInvGagnants_n_2, sommeInvGagnants_n_2_max_l, nbgagnantsMax_l, nbgagnants_l, nbPlayers_l
			double probaN_1_l[20]
			double gainEstN_1_l[20]
			#float probaN_2_l[20]
			double gainEstN_2_l[20][20]
		result_l = -1
		grille_l = self.__engine.getGrille() 
		esperance_l = 1
		gainEst_l = 1
		proba_l = 1
		self.__proba_n_1 = 0
		self.__proba_n_2 = 0
		proba_n_1_l = 1
		self.__gainEst_n_1 = 1
		self.__gainEst_n_2 = 1
		cote2ndRank_l = 100000 # maximum !!
		index2ndRank_l = 0
		result2ndRank_l = 0
		size_l = grille_l.getSize()
		for index_l from 0 <= index_l < size_l:
			bet_l = self.__combin[index_l]

			result_l = self.getResult(bet_l)

			# Proba first rank
			probaMatch_l = 1/grille_l.getGame(index_l).getCotes(result_l)
			repartitionMatch_l = grille_l.getGame(index_l).getRepartition(result_l)

			for index_n_1_l from 0 <= index_n_1_l < size_l:
				gainEstN_2_l[index_l][index_n_1_l] = 0
			
			if (self.__scndRankRate > 0) :
				# Proba and gain scnd rank
				probaN_1_l[index_l] = proba_l * (1 - probaMatch_l)
				gainEstN_1_l[index_l] = gainEst_l / (1 - repartitionMatch_l)
				for index_n_1_l from 0 <= index_n_1_l < index_l:
					gainEstN_1_l[index_n_1_l] = gainEstN_1_l[index_n_1_l] / repartitionMatch_l
					probaN_1_l[index_n_1_l] = probaN_1_l[index_n_1_l] * probaMatch_l
			# compute first Rank proba and gain
			proba_l = proba_l * probaMatch_l
			gainEst_l = gainEst_l / repartitionMatch_l

		nbPlayers_l = float(self.__engine.getNbPlayers())
		# Proba and gain third rank
		if (self.__thirdRankRate > 0) :
			for index_n_2_A_l from 0 <= index_n_2_A_l < size_l:
				bet_n_2_A_l = self.__combin[index_n_2_A_l]
				result_n_2_A_l = self.getResult(bet_n_2_A_l)
				probaMatch_n_2_A_l =  1/grille_l.getGame(index_n_2_A_l).getCotes(result_n_2_A_l)
				repartitionMatch_n_2_A_l = grille_l.getGame(index_n_2_A_l).getRepartition(result_n_2_A_l)

				for index_n_2_B_l from index_n_2_A_l + 1 <= index_n_2_B_l < size_l:
					proba_tmp_l = proba_l * (1 - probaMatch_n_2_A_l) / probaMatch_n_2_A_l
					gainEst_tmp_l = gainEst_l * repartitionMatch_n_2_A_l / (1 - repartitionMatch_n_2_A_l) 
					bet_n_2_B_l = self.__combin[index_n_2_B_l]
					result_n_2_B_l = self.getResult(bet_n_2_B_l)
					probaMatch_n_2_B_l = 1/grille_l.getGame(index_n_2_B_l).getCotes(result_n_2_B_l)
					repartitionMatch_n_2_B_l = grille_l.getGame(index_n_2_B_l).getRepartition(result_n_2_B_l)
					proba_tmp_l = proba_tmp_l * (1 - probaMatch_n_2_B_l) / probaMatch_n_2_B_l
					gainEst_tmp_l = gainEst_tmp_l * repartitionMatch_n_2_B_l / (1 - repartitionMatch_n_2_B_l) 
					gainEstN_2_l[index_n_2_A_l][index_n_2_B_l] = gainEst_tmp_l
					self.__proba_n_2 = self.__proba_n_2 + proba_tmp_l
					self.__gainEst_n_2 = self.__gainEst_n_2 + gainEst_tmp_l


		self.__proba = proba_l
		if (self.__scndRankRate > 0) :
			sommeInvGagnants_n_1 = 0
			sommeInvGagnants_n_1_max_l = 0
			sommeInvGagnants_n_2 = 0
			sommeInvGagnants_n_2_max_l = 0
			for index_n_1_l from 0 <= index_n_1_l < size_l:
				self.__proba_n_1 = self.__proba_n_1 + probaN_1_l[index_n_1_l]
				sommeInvGagnants_n_1 = sommeInvGagnants_n_1 + 1/gainEstN_1_l[index_n_1_l]
				sommeInvGagnants_n_1_max_l = max(sommeInvGagnants_n_1_max_l, 1/gainEstN_1_l[index_n_1_l])
				if (nbPlayers_l > 0):
					sommeInvGagnants_n_1_max_l = min(sommeInvGagnants_n_1_max_l,nbPlayers_l)
					sommeInvGagnants_n_1 = min(sommeInvGagnants_n_1,nbPlayers_l)
				if self.__thirdRankRate > 0 :
					for index_n_2_l from 0 <= index_n_2_l < size_l:
						if (gainEstN_2_l[index_n_1_l][index_n_2_l] != 0) :
							sommeInvGagnants_n_2 = sommeInvGagnants_n_2 + 1/gainEstN_2_l[index_n_1_l][index_n_2_l]
							sommeInvGagnants_n_2_max_l = max(sommeInvGagnants_n_2_max_l, 1/gainEstN_2_l[index_n_1_l][index_n_2_l])
						if (nbPlayers_l > 0):
							sommeInvGagnants_n_2_max_l = min(sommeInvGagnants_n_2_max_l,nbPlayers_l)
							sommeInvGagnants_n_2 = min(sommeInvGagnants_n_2,nbPlayers_l)
			gainEst_n_1_min_l = 1 / (sommeInvGagnants_n_1_max_l * size_l)
			gainEst_n_1_l = 1 / sommeInvGagnants_n_1
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
			else :
				self.__gainEst_n_1_min = gainEst_n_1_min_l
				self.__gainEst_n_1 = gainEst_n_1_l
			if (nbPlayers_l > 0) :
				self.__gainEst_n_1 = min(self.__gainEst_n_1,nbPlayers_l)
				self.__gainEst_n_1_min = min(self.__gainEst_n_1_min,nbPlayers_l)
				self.__gainEst_n_2 = min(self.__gainEst_n_2,nbPlayers_l)
				esperance2ndMin_l = self.__gainEst_n_1_min * self.__proba_n_1
				self.__esperance_n_1_min = esperance2ndMin_l
				esperance2nd_l = self.__gainEst_n_1 * self.__proba_n_1
				self.__esperance_n_1 = esperance2nd_l
				esperance3rd_l = self.__gainEst_n_2 * self.__proba_n_2
				self.__esperance_n_2 = esperance3rd_l

		# Maximize gain with jackpot_l value
		jackpot_l = self.__engine.getJackpot()
		if (size_l == 7) : # loto 7
			nbgagnants_l = 1000000/gainEst_l + 27 
			if (jackpot_l >0) : 
				self.__gainEst = min(1000000/nbgagnants_l, jackpot_l)
			else :
				self.__gainEst = 1000000/nbgagnants_l
		else :
			nbgagnants_l = int((nbPlayers_l) / gainEst_l)  + 1
			if (jackpot_l >0) : 
				self.__gainEst = jackpot_l / nbgagnants_l
			else :
				self.__gainEst = gainEst_l

		#  
		self.__esperance = self.__gainEst * self.__proba 
				
