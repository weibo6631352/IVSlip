@echo off
rem 设置UTF-8编码，确保正确显示中文
chcp 65001 >nul
title 输液单管理系统

REM 检查是否有命令行参数
if "%1"=="run" goto START_APP_DIRECT

:MAIN_MENU
cls
echo ========================================
echo    输液单管理系统 - 主菜单
echo ========================================
echo.
echo  1. 启动应用程序
echo  2. 安装依赖
echo  3. 构建应用
echo  4. 退出
echo.
echo ========================================
echo  提示: 在PowerShell中请使用 .\start.bat 或 .\start.bat run
echo  在命令提示符中使用 start.bat 或 start.bat run
echo ========================================
echo.

choice /c 1234 /n /m "选择选项 (1-4): "

if errorlevel 4 goto EXIT_PROGRAM
if errorlevel 3 goto BUILD_APP
if errorlevel 2 goto INSTALL_DEPS
if errorlevel 1 goto START_APP

:START_APP_DIRECT
echo.
echo 正在启动输液单管理系统...
echo.
python ivmanager/run.py
exit /b

:START_APP
cls
echo.
echo 正在启动应用程序...
echo.
python ivmanager/run.py
echo.
echo 按任意键返回菜单...
pause >nul
goto MAIN_MENU

:INSTALL_DEPS
cls
echo.
echo 安装依赖...
echo.
python -m pip install -r requirements.txt
echo.
echo 按任意键返回菜单...
pause >nul
goto MAIN_MENU

:BUILD_APP
cls
echo.
echo 构建应用程序...
echo.
call .\scripts\build\build.bat
echo.
echo 按任意键返回菜单...
pause >nul
goto MAIN_MENU

:EXIT_PROGRAM
cls
echo.
echo 正在退出程序...
echo 感谢使用输液单管理系统!
echo.
timeout /t 2 >nul
exit /b 