# En cas général les "#" servent à faire des commentaires comme ici
<<<<<<< HEAD
export PATH=$PATH:/home/poupou/DATA/Program/GeckoDiver
=======
export PATH=$PATH:$HOME/Program/geckodriver-v0.26.0/
>>>>>>> a21f3faffcfed07232b53fc96f1fd5462192e298
echo Lancement de CombinoGUI !
cd $COMBINO
date > ./date1.txt
python ./src/CombinoGUI.py
date > ./date2.txt
cd -
