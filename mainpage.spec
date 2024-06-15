# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['mainpage.py'],
    pathex=[],
    binaries=[],
    datas=[('image','image'),('DataForUse','DataForUse'),
        ('内置单词书','内置单词书'),('内置英文原版书','内置英文原版书')],
    hiddenimports=[],
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
    [],
    exclude_binaries=True,
    name='mainpage',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='D:\\leidian\\pic_qwetyuqwteyu\\oh-boy.ico'
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='我是软件！！！双击我就可以进去了！！',
)
