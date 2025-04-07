@echo off
echo ======================================
echo        ENVIRONMENT CHECK
echo ======================================
echo.
echo Checking Python environment and dependencies...

REM 保存当前目录并切换到项目根目录
pushd %~dp0\..\..
python scripts\check_system.py
popd

echo.
pause 