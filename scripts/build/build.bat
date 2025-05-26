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
echo 3. 检查资源文件...
if not exist "ivmanager\resources\assets\icon.png" (
    echo 错误: 缺少图标文件!
    echo 请确保 ivmanager\resources\assets\icon.png 文件存在
    pause
    exit /b 1
)

if not exist "ivmanager\resources\templates\输液单.xlsx" (
    echo 错误: 缺少模板文件!
    echo 请确保 ivmanager\resources\templates\输液单.xlsx 文件存在
    pause
    exit /b 1
)

if not exist "ivmanager\resources\config\suggestions.json" (
    echo 错误: 缺少配置文件!
    echo 请确保 ivmanager\resources\config\suggestions.json 文件存在
    pause
    exit /b 1
)

REM 构建应用
echo 4. 构建应用...
REM 清理之前的构建
if exist "build" rd /s /q "build" 2>nul
if exist "dist" rd /s /q "dist" 2>nul

REM 直接使用PyInstaller命令行参数构建
echo 正在运行PyInstaller...
python -m PyInstaller ^
  --name="输液单管理系统" ^
  --windowed ^
  --clean ^
  --icon="ivmanager\resources\assets\icon.png" ^
  --add-data="ivmanager\resources\assets\icon.png;ivmanager\resources\assets" ^
  --add-data="ivmanager\resources\templates\输液单.xlsx;ivmanager\resources\templates" ^
  --add-data="ivmanager\resources\config\suggestions.json;ivmanager\resources\config" ^
  --hidden-import=win32gui ^
  --hidden-import=win32con ^
  --hidden-import=win32process ^
  --hidden-import=psutil ^
  "ivmanager\run.py"

echo 5. 复制资源文件到dist目录...
mkdir "dist\ivmanager\resources\assets" 2>nul
mkdir "dist\ivmanager\resources\templates" 2>nul
mkdir "dist\ivmanager\resources\config" 2>nul

copy "ivmanager\resources\assets\icon.png" "dist\ivmanager\resources\assets\" /y
copy "ivmanager\resources\templates\输液单.xlsx" "dist\ivmanager\resources\templates\" /y
copy "ivmanager\resources\config\suggestions.json" "dist\ivmanager\resources\config\" /y

REM 创建启动批处理文件
echo 6. 创建启动器...
(
echo @echo off
echo chcp 65001 ^>nul
echo cd /d %%~dp0
echo start 输液单管理系统.exe
echo exit
) > "dist\启动输液管理系统.bat"

echo 7. 创建说明文件...
(
echo 输液单管理系统
echo ================
echo.
echo 使用方法:
echo 1. 双击"启动输液管理系统.bat"以运行程序
echo 2. 或直接运行"输液单管理系统.exe"
echo.
echo 注意: 请勿删除resources目录，其中包含程序所需的必要资源文件。
) > "dist\README.txt"

popd

echo.
echo 构建完成! 应用程序文件已准备好，位于dist目录中。
echo.
pause 