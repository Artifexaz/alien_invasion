# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['alien_invasion.py'],
             pathex=['alien.py', 'bullet.py', 'button.py', 'display.py', 'game_function.py', 'game_stats.py', 'scoreboard.py', 'settings.py', 'ship.py', 'C:\\Users\\绿色调感\\Python'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=['numpy'],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='alien_invasion',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False , icon='x.ico')
