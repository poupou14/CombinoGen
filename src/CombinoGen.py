#!/usr/bin/python 
import string, sys
import threading
from CombinoSource import CombinoSource
from CombinoEngine import CombinoEngine
from CombinoEngine import GenBetCounter


def main():
	
	lock_l = threading.Lock()
	nbGenBets_l = GenBetCounter()
	
	if len(sys.argv) == 2 :
		if sys.argv[1] == "-h" :
			print "user help :"
			print "$ CombinoGen.sh -s <source_data_file> -o <output_file> [-e <esperance_min>]"
			exit()
		else :
			annee = int(sys.argv[1])
	elif len(sys.argv) == 5 :
		print "5 params"
		sourceFile_l = sys.argv[2]
		outputFile_l = sys.argv[4]
		espMin_l = 0
	elif len(sys.argv) == 7 :
		print "7 params"
		sourceFile_l = sys.argv[2]
		outputFile_l = sys.argv[4]
		espMin_l = float(sys.argv[6])
	else :
		print "user help :"
		print "$ CombinoGen.sh -s <source_data_file> -o <output_file>"
		exit()

	print "Lecture fichier Source"
	mySource = CombinoSource(sourceFile_l)
	myGrille = mySource.getGrille()

	print "Calcul Proba et Esperances des grilles"
	f1=open(outputFile_l, 'w+')
	f1.write("Game;Proba-Rg1;Esp-Rg1;Estim-Rg1;Proba-Rg2;Esp-Rg2;Estim-Rg2;Proba-Rg3;Esp-Rg3;Estim-Rg3;Esp-tot\n")
	strBet1_l = ""
	strBetN_l = ""
	strBet2_l = ""
	returnRate_l = mySource.getReturnRate()
	firstRankRate_l = mySource.getFirstRankRate()
	scndRankRate_l = mySource.getScndRankRate()
	thirdRankRate_l = mySource.getThirdRankRate()
	jackpot_l = mySource.getJackpot()
	nbPlayers_l = mySource.getNbPlayers()
	totalRate_l = returnRate_l * firstRankRate_l
	if thirdRankRate_l != -1 :
		totalRate2nd_l = returnRate_l * scndRankRate_l
		totalRate3rd_l = returnRate_l * thirdRankRate_l
		print "Min Esp : %f" % espMin_l
		print "1st rank rate Esp : %f" % firstRankRate_l
		print "2nd rank rate Esp : %f" % scndRankRate_l
		print "3rd rank rate Esp : %f" % thirdRankRate_l
		print "sourceFile_l : %s" % sourceFile_l
		print "outputFile_l : %s" % outputFile_l
		print "Jackpot : %f Euros" % jackpot_l
		print "Nb Players Esp : %f" % nbPlayers_l
		myBet1 = CombinoEngine(myGrille, 0, lock_l, nbGenBets_l, strBet1_l, totalRate_l, espMin_l, f1, jackpot_l, nbPlayers_l, totalRate2nd_l, totalRate3rd_l)
		myBetN = CombinoEngine(myGrille, 1, lock_l, nbGenBets_l, strBetN_l, totalRate_l, espMin_l, f1, jackpot_l, nbPlayers_l, totalRate2nd_l, totalRate3rd_l)
		myBet2 = CombinoEngine(myGrille, 2, lock_l, nbGenBets_l, strBet2_l, totalRate_l, espMin_l, f1, jackpot_l, nbPlayers_l, totalRate2nd_l, totalRate3rd_l)
	elif scndRankRate_l != -1 :
		totalRate2nd_l = returnRate_l * scndRankRate_l
		print "1st rank rate Esp : %f" % firstRankRate_l
		print "2nd rank rate Esp : %f" % scndRankRate_l
		print "Jackpot : %f Euros" % jackpot_l
		print "Nb Players Esp : %f" % nbPlayers_l
		myBet1 = CombinoEngine(myGrille, 0, lock_l, nbGenBets_l, strBet1_l, totalRate_l, espMin_l, f1, jackpot_l, nbPlayers_l, totalRate2nd_l)
		myBetN = CombinoEngine(myGrille, 1, lock_l, nbGenBets_l, strBetN_l, totalRate_l, espMin_l, f1, jackpot_l, nbPlayers_l, totalRate2nd_l)
		myBet2 = CombinoEngine(myGrille, 2, lock_l, nbGenBets_l, strBet2_l, totalRate_l, espMin_l, f1, jackpot_l, nbPlayers_l, totalRate2nd_l)
	else :
		print "1st rank rate Esp : %f" % firstRankRate_l
		print "Jackpot : %f Euros" % jackpot_l
		print "Nb Players Esp : %f" % nbPlayers_l
		myBet1 = CombinoEngine(myGrille, 0, lock_l, nbGenBets_l, strBet1_l, totalRate_l, espMin_l, f1, jackpot_l, nbPlayers_l)
		myBetN = CombinoEngine(myGrille, 1, lock_l, nbGenBets_l, strBetN_l, totalRate_l, espMin_l, f1, jackpot_l, nbPlayers_l)
		myBet2 = CombinoEngine(myGrille, 2, lock_l, nbGenBets_l, strBet2_l, totalRate_l, espMin_l, f1, jackpot_l, nbPlayers_l)
	myBet1.start()
	myBetN.start()
	myBet2.start()
	myBet1.join()
	myBetN.join()
	myBet2.join()
	print "Fichier genere :", outputFile_l
	f1.write(strBet1_l)
	f1.write(strBetN_l)
	f1.write(strBet2_l)
#	myBets.printFile(outputFile_l)
	
main()
