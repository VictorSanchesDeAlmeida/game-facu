# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ['src\\main.py'],
    pathex=['D:\\Projects\\game-facu'],
    binaries=[],
    datas=[
        ('assets\\Demon.png', 'assets'),
        ('assets\\Player.png', 'assets'),
        ('assets\\grass_block.png', 'assets'),
        ('assets\\rocky_block.png', 'assets'),
        ('src\\sprite\\Demon.json', 'src\\sprite'),
        ('src\\sprite\\Player.json', 'src\\sprite'),
    ],
    hiddenimports=['pygame', 'json', 'math', 'random', 'os', 'sys'],
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
    name='DemonHunter',
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
