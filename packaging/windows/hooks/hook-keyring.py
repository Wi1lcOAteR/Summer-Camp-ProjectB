from PyInstaller.utils.hooks import collect_data_files, collect_submodules


hiddenimports = [
    "keyring.backends.Windows",
    "keyring.backends.chainer",
    *collect_submodules("keyring.backends"),
]
datas = collect_data_files("keyring")
