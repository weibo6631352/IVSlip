@echo off
rem 设置UTF-8编码
chcp 65001 >nul

echo ======================================
echo         构建输液单管理系统
echo ======================================
echo.
echo 第一步: 检查运行实例...

REM 保存当前目录并切换到项目根目录
pushd %~dp0\..\..

REM 结束可能正在运行的应用实例
echo 查找并关闭正在运行的实例...
taskkill /f /im 输液单管理系统.exe 2>nul
if exist "%APPDATA%\IVManagementSystem\app.lock" del /f /q "%APPDATA%\IVManagementSystem\app.lock" 2>nul

echo 第二步: 安装依赖...
python -m pip install -r requirements.txt

echo 第三步: 安装PyInstaller...
python -m pip install PyInstaller

echo 第四步: 复制资源文件...
REM 确保资源目录存在
if not exist "ivmanager\resources\assets" mkdir "ivmanager\resources\assets"
if not exist "ivmanager\resources\templates" mkdir "ivmanager\resources\templates"
if not exist "ivmanager\resources\config" mkdir "ivmanager\resources\config"

REM 如果有src目录，从src和data目录复制资源
if exist "src\assets\icon.png" copy "src\assets\icon.png" "ivmanager\resources\assets\icon.png" 2>nul
if exist "data\templates\输液单.xlsx" copy "data\templates\输液单.xlsx" "ivmanager\resources\templates\输液单.xlsx" 2>nul
if exist "src\config\suggestions.json" copy "src\config\suggestions.json" "ivmanager\resources\config\suggestions.json" 2>nul

echo 第五步: 构建应用...
REM 清理之前的构建
if exist "build" rd /s /q "build" 2>nul
if exist "dist\输液单管理系统.exe" del /f "dist\输液单管理系统.exe" 2>nul

REM 直接使用PyInstaller命令行参数构建，不使用spec文件
python -m PyInstaller --name="输液单管理系统" ^
  --windowed ^
  --icon="ivmanager\resources\assets\icon.png" ^
  --add-data="ivmanager\resources\assets\icon.png;ivmanager\resources\assets" ^
  --add-data="ivmanager\resources\templates\输液单.xlsx;ivmanager\resources\templates" ^
  --add-data="ivmanager\resources\config\suggestions.json;ivmanager\resources\config" ^
  --hidden-import=win32gui ^
  --hidden-import=win32con ^
  --hidden-import=win32process ^
  --hidden-import=psutil ^
  "ivmanager\run.py"

echo 第六步: 创建启动器...
REM 创建启动批处理文件
(
echo @echo off
echo chcp 65001 ^>nul
echo cd /d %%~dp0
echo start 输液单管理系统.exe
echo exit
) > "dist\temp.bat"

REM 使用PowerShell转换编码并替换文件
powershell -Command "Get-Content 'dist\temp.bat' | Set-Content -Encoding UTF8 'dist\启动输液管理系统.bat'"
del "dist\temp.bat" 2>nul

popd

echo.
echo 构建完成! 应用程序文件已准备好，位于dist目录中。
echo.
pause 