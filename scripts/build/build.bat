@echo off
rem 设置UTF-8编码
chcp 65001 >nul

echo ======================================
echo         构建输液单管理系统
echo ======================================
echo.

REM 保存当前目录并切换到项目根目录
pushd %~dp0\..\..

REM 结束正在运行的应用
echo 1. 检查运行实例...
taskkill /f /im 输液单管理系统.exe 2>nul
if exist "%APPDATA%\IVManagementSystem\app.lock" del /f /q "%APPDATA%\IVManagementSystem\app.lock" 2>nul

REM 安装依赖
echo 2. 安装依赖...
python -m pip install -r requirements.txt
python -m pip install pyinstaller

REM 准备资源目录
echo 3. 检查资源...
if not exist "ivmanager\resources\assets" mkdir "ivmanager\resources\assets"
if not exist "ivmanager\resources\templates" mkdir "ivmanager\resources\templates"
if not exist "ivmanager\resources\config" mkdir "ivmanager\resources\config"

REM 构建应用
echo 4. 构建应用...
REM 清理之前的构建
if exist "build" rd /s /q "build" 2>nul
if exist "dist" rd /s /q "dist" 2>nul

REM 直接使用PyInstaller命令行参数构建
echo python -m PyInstaller --name="输液单管理系统" --windowed --icon="ivmanager\resources\assets\icon.png" --add-data="ivmanager\resources\assets\icon.png;ivmanager\resources\assets" --add-data="ivmanager\resources\templates\输液单.xlsx;ivmanager\resources\templates" --add-data="ivmanager\resources\config\suggestions.json;ivmanager\resources\config" --hidden-import=win32gui --hidden-import=win32con --hidden-import=win32process --hidden-import=psutil "ivmanager\run.py"
python -m PyInstaller --name="输液单管理系统" --windowed --icon="ivmanager\resources\assets\icon.png" --add-data="ivmanager\resources\assets\icon.png;ivmanager\resources\assets" --add-data="ivmanager\resources\templates\输液单.xlsx;ivmanager\resources\templates" --add-data="ivmanager\resources\config\suggestions.json;ivmanager\resources\config" --hidden-import=win32gui --hidden-import=win32con --hidden-import=win32process --hidden-import=psutil "ivmanager\run.py"

REM 创建启动批处理文件
echo 5. 创建启动器...
echo @echo off > "dist\启动输液管理系统.bat"
echo chcp 65001 ^>nul >> "dist\启动输液管理系统.bat"
echo cd /d %%~dp0 >> "dist\启动输液管理系统.bat"
echo start 输液单管理系统.exe >> "dist\启动输液管理系统.bat"
echo exit >> "dist\启动输液管理系统.bat"

popd

echo.
echo 构建完成! 应用程序文件已准备好，位于dist目录中。
echo.
pause 