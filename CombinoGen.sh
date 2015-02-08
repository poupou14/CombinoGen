# En cas général les "#" servent à faire des commentaires comme ici
echo Lancement scrap de FrancePari
date > ./date1.txt
python ./src/CombinoGen.py $@
date > ./date2.txt
 
