@echo off
echo ======================================
echo       INSTALL DEPENDENCIES
echo ======================================
echo.
echo Installing required Python packages...

REM 保存当前目录并切换到项目根目录
pushd %~dp0\..\..
pip install -r requirements.txt
popd

echo.
echo Installation complete!
pause 