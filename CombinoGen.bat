REM En cas général les "#" servent à faire des commentaires comme ici
echo Lancement scrap de PronoSoft
set PATH=%PATH%;"D:\Program Files"\geckodriver
python ./src/CombinoGen.py %1 %2 %3 %4 %5 %6
 
