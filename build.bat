@echo off
echo Building QT version
pyinstaller -n tcb++ -w -F -i assets/tcb-col.ico main.py
echo Building console version
pyinstaller -n console -F -i assets/tcb-bl.ico console.py
pause