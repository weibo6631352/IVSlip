# -*- mode: python ; coding: utf-8 -*-
import os
import sys

# 获取当前目录
current_dir = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
sys.path.append(current_dir)

block_cipher = None

a = Analysis(
    [os.path.join(current_dir, 'ivmanager', 'run.py')],
    pathex=[current_dir],
    binaries=[],
    datas=[
        # 资源文件
        (os.path.join(current_dir, 'ivmanager/resources/assets/icon.png'), 'ivmanager/resources/assets'),
        (os.path.join(current_dir, 'ivmanager/resources/templates/输液单.xlsx'), 'ivmanager/resources/templates'),
        (os.path.join(current_dir, 'ivmanager/resources/config/suggestions.json'), 'ivmanager/resources/config'),
    ],
    hiddenimports=['win32gui', 'win32con', 'win32process', 'psutil'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='输液单管理系统',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=os.path.join(current_dir, 'ivmanager/resources/assets/icon.png'),
) 