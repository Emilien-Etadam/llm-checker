@echo off
REM ===================================================================
REM LLM Checker - Script de Build Automatique pour Windows
REM ===================================================================
REM Ce script automatise la création du fichier .exe
REM Double-cliquez sur ce fichier pour lancer le build

echo.
echo ========================================
echo  LLM Checker - Build Script
echo ========================================
echo.

REM Vérifier que Python est installé
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERREUR] Python n'est pas installé ou pas dans le PATH
    echo.
    echo Veuillez installer Python depuis: https://www.python.org/downloads/
    echo N'oubliez pas de cocher "Add Python to PATH" lors de l'installation
    echo.
    pause
    exit /b 1
)

echo [OK] Python est installé
echo.

REM Vérifier que pip est installé
pip --version >nul 2>&1
if errorlevel 1 (
    echo [ERREUR] pip n'est pas installé
    echo.
    pause
    exit /b 1
)

echo [OK] pip est installé
echo.

REM Installer les dépendances
echo [ETAPE 1/4] Installation des dépendances...
pip install -r requirements.txt
if errorlevel 1 (
    echo [ERREUR] Échec de l'installation des dépendances
    pause
    exit /b 1
)
echo [OK] Dépendances installées
echo.

REM Tester l'application (optionnel - commentez si vous ne voulez pas)
echo [ETAPE 2/4] Test de l'application (5 secondes)...
echo Fermer la fenêtre qui s'ouvre pour continuer...
timeout /t 2 /nobreak >nul
start /wait python llm_checker_gui.py
echo [OK] Test terminé
echo.

REM Nettoyer les anciens builds
echo [ETAPE 3/4] Nettoyage des anciens builds...
if exist dist rmdir /s /q dist
if exist build rmdir /s /q build
echo [OK] Nettoyage terminé
echo.

REM Build avec PyInstaller
echo [ETAPE 4/4] Création du fichier .exe...
echo Cela peut prendre 1-2 minutes, patientez...
echo.
pyinstaller llm_checker.spec
if errorlevel 1 (
    echo.
    echo [ERREUR] Échec de la création du .exe
    echo.
    pause
    exit /b 1
)

echo.
echo ========================================
echo  BUILD RÉUSSI !
echo ========================================
echo.
echo Le fichier .exe a été créé dans:
echo %CD%\dist\LLM_Checker.exe
echo.
echo Taille du fichier:
dir dist\LLM_Checker.exe | find "LLM_Checker.exe"
echo.
echo Vous pouvez maintenant:
echo 1. Tester le .exe en double-cliquant dessus
echo 2. Le copier où vous voulez
echo 3. Le distribuer (aucune installation requise)
echo.

REM Ouvrir le dossier dist
echo Voulez-vous ouvrir le dossier dist?
pause
explorer dist

echo.
echo Terminé!
pause
