# -*- mode: python ; coding: utf-8 -*-
import os
import sys

# 使用硬编码的相对路径
script_dir = os.path.dirname(os.path.abspath("scripts/build.spec"))
root_dir = os.path.dirname(script_dir)
sys.path.append(root_dir)

block_cipher = None

a = Analysis(
    [os.path.join(root_dir, 'app.py')],
    pathex=[root_dir],
    binaries=[],
    datas=[
        # 将所有资源文件放在resources目录下
        (os.path.join(root_dir, 'src/assets/icon.png'), 'resources/assets'),
        (os.path.join(root_dir, 'data/templates/输液单.xlsx'), 'resources/templates'),
        (os.path.join(root_dir, 'src/config/suggestions.json'), 'resources/config'),
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
    icon=os.path.abspath(os.path.join(root_dir, 'src/assets/icon.png')),
) 