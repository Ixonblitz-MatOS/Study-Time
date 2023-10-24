@echo off
set PYINSTALLER_NOT_INSTALLED="pyinstaller : The term 'pyinstaller' is not recognized as the name of a cmdlet, function, script file, or operable program. Check the "
set PYINSTALLER_INSTALLED="usage: pyinstaller [-h] [-v] [-D] [-F] [--specpath DIR] [-n NAME] [--contents-directory CONTENTS_DIRECTORY] [--add-data SOURCE:DEST]"

echo "Checking if pyinstaller is installed..."
"check if PYINSTALLER_NOT_INSTALLED or PYINSTALLER_INSTALLED is in the output of pyinstaller"
if "pyinstaller" == "PYINSTALLER_NOT_INSTALLED" (
    echo "pyinstaller is not installed. Installing pyinstaller..."
    pip install pyinstaller
    echo "pyinstaller installed."
    pyinstaller --onefile main.py
) else (
    echo "pyinstaller is installed."
    pyinstaller --onefile main.py
)
