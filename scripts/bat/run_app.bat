@echo off
echo ======================================
echo          START APPLICATION
echo ======================================
echo.
echo Starting IV Management System...

REM 保存当前目录并切换到项目根目录
pushd %~dp0\..\..
start pythonw app.py
popd

echo.
echo Application started successfully.
echo Please check the system tray for the application icon.
timeout /t 3 > nul 