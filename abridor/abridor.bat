@echo off
echo driverstation:
powershell -Command "Start-Process '.\DriverStation.exe' -Verb runAs"
echo keyboard:
start /min python3 ".\KeyboardToNetworkTables.py"