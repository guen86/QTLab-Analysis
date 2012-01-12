:: qtlabgui.bat
:: Runs QTlab GUI part on Windows
::
:: QTlab needs some programs to exist in the system PATH. They can be
:: defined globally in "configuration_panel => system => advanced =>
:: system_variables", or on the commandline just before execution of
:: QTlab.

SET PATH=%CD%\..\qtlab\3rd_party\gtk\bin;%CD%\..\qtlab\3rd_party\gtk\lib;%PATH%
SET GTK_BASEPATH=%CD%\..\qtlab\3rd_party\gtk

SET PATH=%CD%\..\qtlab\3rd_party\gnuplot\bin;%PATH%

SET PATH=%CD%\..\qtlab\3rd_party\Console2\;%PATH%

SET QT_API=pyqt

:: Check for version of python
IF EXIST c:\python27\python.exe (
    SET PYTHON_PATH=c:\python27
    GOTO mark1
)
IF EXIST c:\python26\python.exe (
    SET PYTHON_PATH=c:\python26
    GOTO mark1
)
:mark1
:: Run QTlab
:: check if version < 0.11
IF EXIST "%PYTHON_PATH%\scripts\ipython.py" (
::    start Console -w "QTLab Analysis" -r "/k %PYTHON_PATH%\python.exe %PYTHON_PATH%\scripts\ipython.py -q4thread -p sh source/analysisclient.py"
    GOTO EOF
)
:: check if version >= 0.11
IF EXIST "%PYTHON_PATH%\scripts\ipython-script.py" (
    start Console -w "QTLab Analysis" -r "/k %PYTHON_PATH%\python.exe %PYTHON_PATH%\scripts\ipython-script.py --gui=qt -i source/analysisclient.py"
::    start %PYTHON_PATH%\python.exe source/analysisclient.py"
    GOTO EOF
)

echo Failed to run qtlab.bat
pause
:EOF
