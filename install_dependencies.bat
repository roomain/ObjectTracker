@echo off
REM Chercher Python dans les emplacements courants
echo Recherche de Python...

REM Vérifier le répertoire Python par défaut dans Windows
if exist "C:\Python311\python.exe" (
    set PYTHON_PATH=C:\Python311\python.exe
    echo Python trouvé: C:\Python311
) else if exist "C:\Python310\python.exe" (
    set PYTHON_PATH=C:\Python310\python.exe
    echo Python trouvé: C:\Python310
) else if exist "C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python311\python.exe" (
    set PYTHON_PATH=C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python311\python.exe
    echo Python trouvé: AppData
) else (
    echo.
    echo ✗ Python n'a pas pu être trouvé automatiquement
    echo.
    echo SOLUTION:
    echo 1. Vérifiez que Python est installé
    echo 2. Ouvrez Invite de commandes en tant qu'admin
    echo 3. Exécutez: python -m pip install -r requirements.txt
    echo.
    echo Ou spécifiez le chemin complet:
    echo "C:\Python311\python.exe" -m pip install -r requirements.txt
    echo.
    pause
    exit /b 1
)

REM Installer les dépendances
echo.
echo Installation des dépendances...
"%PYTHON_PATH%" -m pip install -r requirements.txt

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ✓ Installation réussie!
    echo.
    echo Vous pouvez maintenant lancer l'application avec:
    echo "%PYTHON_PATH%" main.py
) else (
    echo.
    echo ✗ Erreur lors de l'installation
    echo Vérifiez votre connexion internet et réessayez
)

pause
