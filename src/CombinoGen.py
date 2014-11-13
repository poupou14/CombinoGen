#!/usr/bin/python 
import string, sys
from CombinoSource import CombinoSource
from CombinoEngine import CombinoEngine


def main():
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
	returnRate_l = mySource.getReturnRate()
	firstRankRate_l = mySource.getFirstRankRate()
	scndRankRate_l = mySource.getScndRankRate()
	thirdRankRate_l = mySource.getThirdRankRate()
	totalRate_l = returnRate_l * firstRankRate_l
	if thirdRankRate_l != -1 :
		totalRate2nd_l = returnRate_l * scndRankRate_l
		totalRate3rd_l = returnRate_l * thirdRankRate_l
		print "Min Esp : %f" % espMin_l
		print "sourceFile_l : %s" % sourceFile_l
		print "outputFile_l : %s" % outputFile_l
		myBets = CombinoEngine(myGrille, totalRate_l, espMin_l, f1, totalRate2nd_l, totalRate3rd_l)
	elif scndRankRate_l != -1 :
		totalRate2nd_l = returnRate_l * scndRankRate_l
		myBets = CombinoEngine(myGrille, totalRate_l, espMin_l, f1, totalRate2nd_l)
	else :
		myBets = CombinoEngine(myGrille, totalRate_l, espMin_l, f1)
	myBets.generateCombinoBets()
	print "Fichier genere :", outputFile_l
	f1.write(str(myBets))
#	myBets.printFile(outputFile_l)
	
main()
