from cx_Freeze import setup, Executable


import os.path

os.environ['TCL_LIBRARY'] = r'C:\Progra~1\Python36-32\tcl\tcl8.6'
os.environ['TK_LIBRARY'] = r'C:\Progra~1\Python36-32\tcl\tk8.6'

# Dependencies are automatically detected, but it might need
# fine tuning.
buildOptions = dict(packages = [], excludes = ["PyQt5", "numpy"])

import sys
base = 'Win32GUI' if sys.platform=='win32' else None

includes = []
include_files = [r"C:\Progra~1\Python36-32\Lib\site-packages\numpy", 
				         r"C:\Progra~1\Python36-32\DLLs\tcl86t.dll",
                 r"F:\PyTool\postbuildplat12\config.ini",
                 r"F:\PyTool\postbuildplat12\image",
                 r"C:\Progra~1\Python36-32\DLLs\tk86t.dll"]

executables = [
    Executable(script=r'F:\PyTool\postbuildplat12\main.py', base=base, targetName = 'Postbuild.exe', icon="image/icon6.ico")
]

setup(name='Postbuild',
      version = '1.0',
      author = "Kanwairen",
      description = 'Tool',
      # options = dict(build_exe = buildOptions),
      executables = executables,
      # options={"build_exe": {"includes": includes, "include_files": include_files, "excludes": ["PyQt5", "numpy", "notebook"], "optimize":2, "compressed":1}})
      options={"build_exe": dict(includes = includes, include_files = include_files, excludes = ["PyQt5", "numpy", "notebook"], optimize = 2)})
