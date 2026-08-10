from PyInstaller.utils.hooks import collect_data_files, collect_dynamic_libs


datas = collect_data_files("pypdfium2")
binaries = collect_dynamic_libs("pypdfium2")
