# En cas général les "#" servent à faire des commentaires comme ici
export PATH=$PATH:/home/poupou/DATA/Program/GeckoDiver
echo Lancement de CombinoGUI !
cd $COMBINO
date > ./date1.txt
python ./src/CombinoGUI.py
date > ./date2.txt
cd -
