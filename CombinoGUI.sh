# En cas général les "#" servent à faire des commentaires comme ici
export PATH=$PATH:/home/poupou/Program/geckodriver-v0.27.0/
echo Lancement de CombinoGUI !
cd $COMBINO
date > ./date1.txt
python2 ./src/CombinoGUI.py
date > ./date2.txt
cd -
