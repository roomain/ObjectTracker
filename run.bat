@echo off
REM Script pour lancer l'application ObjectTracker
echo Démarrage de ObjectTracker...

REM Chercher Python
if exist "C:\Python311\python.exe" (
    set PYTHON_PATH=C:\Python311\python.exe
) else if exist "C:\Python310\python.exe" (
    set PYTHON_PATH=C:\Python310\python.exe
) else if exist "C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python311\python.exe" (
    set PYTHON_PATH=C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python311\python.exe
) else (
    echo ✗ Python n'a pas pu être trouvé
    echo Installez d'abord les dépendances avec: install_dependencies.bat
    pause
    exit /b 1
)

REM Lancer l'application
"%PYTHON_PATH%" main.py

pause
