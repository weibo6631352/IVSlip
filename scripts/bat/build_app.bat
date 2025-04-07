@echo off
chcp 65001 >nul
echo ======================================
echo         BUILD APPLICATION
echo ======================================
echo.
echo Step 1: Checking running instances...

REM 保存当前目录并切换到项目根目录
pushd %~dp0\..\..

REM 结束可能正在运行的应用实例
echo Finding and closing running instances...
taskkill /f /im 输液单管理系统.exe 2>nul
if exist "%APPDATA%\IVManagementSystem\app.lock" del /f /q "%APPDATA%\IVManagementSystem\app.lock" 2>nul

echo Step 2: Installing PyInstaller...
python -m pip install pyinstaller

echo Step 3: Building application...
REM 清理之前的构建
if exist "build" rd /s /q "build" 2>nul
if exist "dist\输液单管理系统.exe" del /f "dist\输液单管理系统.exe" 2>nul

REM 使用修改后的spec文件进行构建
python -m PyInstaller scripts/build.spec

echo Step 4: Organizing resources...

REM 确保原始的src和data目录已被复制
if not exist dist\resources mkdir dist\resources

REM 创建正确的资源目录结构
echo Creating resource directories...
mkdir dist\resources\templates 2>nul
mkdir dist\resources\config 2>nul
mkdir dist\resources\assets 2>nul

REM 复制资源文件到新的结构中
echo Copying template files...
copy /y "data\templates\输液单.xlsx" "dist\resources\templates\" 2>nul

echo Copying config files...
copy /y "src\config\suggestions.json" "dist\resources\config\" 2>nul

echo Copying asset files...
copy /y "src\assets\icon.png" "dist\resources\assets\" 2>nul

REM 如果需要，删除旧的目录结构
if exist dist\src rd /s /q dist\src 2>nul
if exist dist\data rd /s /q dist\data 2>nul

REM 创建启动批处理文件 - 使用UTF-8编码
echo Creating launcher...

REM 使用临时文件确保UTF-8编码
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
echo Build completed! Application files are ready in the dist directory.
echo All resources organized into dist\resources folder.
pause 