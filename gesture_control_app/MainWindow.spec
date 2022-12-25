# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    [
        'MainWindow.py',
        'PySide/FloatingWindow.py',
        'PySide/GestureFloatingWindow.py',
        'PySide/HelpWindow.py',
        'PySide/ModelFloatingWindow.py',
        'PySide/MyKeyboard.py',
        'PySide/MyTabWidget.py',
        'PySide/SystemConfigWindow.py',
        'PySide/UserConfigWindow.py',
        'PySide/WarningFloatingWindow.py',
        'PySide/utils/KeyboardMap.py',
        'PySide/utils/MyLoading.py',
        'PySide/utils/MyMessageBox.py',
        'PySide/utils/PropertiesHandler.py',
        'PySide/utils/ScreenUtil.py',
        'PySide/utils/ThreadUtils.py',
        'GestureAlgorithm/camera.py',
        'GestureAlgorithm/Action/BaseAction.py',
        'GestureAlgorithm/Action/EyeGaze.py',
        'GestureAlgorithm/Action/FaceDetection.py',
        'GestureAlgorithm/Action/MouseMoving.py',
        'GestureAlgorithm/Action/ScrollScreen.py',
        'GestureAlgorithm/Action/StringAction.py',
        'GestureAlgorithm/Action/VirtualKeyboard.py',
    ],
    pathex=[],
    binaries=[],
    datas=[
        ('PySide/resources/images', 'PySide/resources/images'),
        ('PySide/resources/qss', 'PySide/resources/qss'),
        ('models', 'models')
    ],
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
    name=u'手势控制',
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
    icon='PySide/resources/images/favicon.ico',
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='MainWindow',
)
