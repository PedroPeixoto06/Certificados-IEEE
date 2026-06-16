# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ['src/app_gui.py'],
    pathex=['src'],
    binaries=[],
    # O PyInstaller agora vai puxar as pastas inteiras, garantindo que a logo vai junto com os assets
    datas=[('assets', 'assets'), ('data', 'data')],
    hiddenimports=['main'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='app_gui',
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
)