# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['D:/Python/PyCharm/YTD_bootstrap/main.py'],
    pathex=[],
    binaries=[],
    datas=[('D:/Python/PyCharm/YTD_bootstrap/images', 'images/'), ('D:/Python/PyCharm/YTD_bootstrap/images/YouTube.ico', '.')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='Elegant YouTube Downloader',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['D:\\Python\\PyCharm\\YTD_bootstrap\\images\\YouTube.ico'],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='Elegant YouTube Downloader',
)
