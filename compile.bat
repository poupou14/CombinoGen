del  src\*.c
rmdir src\build
cd src
pyside-uic -o ui_mainwin.py mainwin.ui
CALL "c:\Program Files (x86)\Microsoft Visual Studio 9.0\VC\bin\"vcvarsx86_amd64.bat
python setup.py build_ext --inplace
cd ..
