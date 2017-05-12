# En cas général les "#" servent à faire des commentaires comme ici
export PATH=$PATH:$HOME/Program/geckodriver/:/media/sf_Thalès/geckodriver/
echo Lancement de CombinoGUI !
date > ./date1.txt
python ./src/CombinoGUI.py
date > ./date2.txt
