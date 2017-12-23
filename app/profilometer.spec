# -*- mode: python -*-
import os
import site
import sys

block_cipher = None
sys.modules['FixTk'] = None

site_packages_dir = site.getsitepackages()[1]
qml_dir = os.path.join(site_packages_dir, 'PyQt5', 'Qt', 'qml')
qt_dir  = os.path.join(site_packages_dir, 'PyQt5', 'Qt', 'bin')
scipy_path = os.path.join(site_packages_dir, 'scipy')

added_files = [
    (os.path.join('ui', '*.qml'), 'ui'),
    (os.path.join(qml_dir, 'Qt'), 'Qt'),
    (os.path.join(qml_dir, 'QtCharts'), 'QtCharts'),
	(os.path.join(qml_dir, 'QtDataVisualization'), 'QtDataVisualization'),
    (os.path.join(qml_dir, 'QtQuick'), 'QtQuick'),
    (os.path.join(qml_dir, 'QtQuick.2'), 'QtQuick.2'),
    (os.path.join(qt_dir, 'Qt5Charts.dll'), ''),
	(os.path.join(qt_dir, 'Qt5DataVisualization.dll'), ''),
    (os.path.join(qt_dir, 'Qt5Quick.dll'), ''),
    (os.path.join(qt_dir, 'Qt5QuickControls2.dll'), ''),
    (os.path.join(qt_dir, 'Qt5QuickTemplates2.dll'), ''),
    (os.path.join(qt_dir, 'Qt5QuickWidgets.dll'), ''),
    (os.path.join('dlls', '*.dll'), ''),
	(os.path.join(scipy_path, 'extra-dll', '*.dll'), ''),
	#(os.path.join(scipy_path, '_lib', 'messagestream.cp36-win_amd64.pyd'), 'scipy._lib.messagestream.pyd'),
]

a = Analysis(['profilometer.py'],
    #pathex=['C:\\Users\\Sebastian\\Documents\\repo\\profilometer\\app'],
    pathex=['C:\\Users\\Sebastian\\Miniconda3\\envs\\py36-nomkl\\Lib\\site-packages\\PyQt5\\Qt\\bin'],
    binaries=[],
    datas=added_files,
    hiddenimports=['simplejson'],
    hookspath=[],
    runtime_hooks=[],
    excludes=['FixTk', 'tcl', 'tk', '_tkinter', 'tkinter', 'Tkinter'],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher)

pyz = PYZ(a.pure, a.zipped_data,
    cipher=block_cipher)

exe = EXE(pyz,
    a.scripts,
    exclude_binaries=True,
    name='profilometer',
    debug=False,
    strip=False,
    upx=True,
    console=False)

coll = COLLECT(exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    name='app')
