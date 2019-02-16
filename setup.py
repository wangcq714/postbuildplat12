from cx_Freeze import setup, Executable


import os.path

os.environ['TCL_LIBRARY'] = r'C:\Progra~1\Python36\tcl\tcl8.6'
os.environ['TK_LIBRARY'] = r'C:\Progra~1\Python36\tcl\tk8.6'

# Dependencies are automatically detected, but it might need
# fine tuning.
buildOptions = dict(packages = [], excludes = ["PyQt5", "numpy"])

import sys
base = 'Win32GUI' if sys.platform=='win32' else None

includes = []
include_files = [r"C:\Progra~1\Python36\Lib\site-packages\numpy", 
				         r"C:\Progra~1\Python36\DLLs\tcl86t.dll",
                 r"D:\share\postbuildtool\postbuildplat12\config.ini",
                 r"D:\share\postbuildtool\postbuildplat12\image",
                 r"C:\Progra~1\Python36\DLLs\tk86t.dll"]

executables = [
    Executable('D:\\share\\postbuildtool\\postbuildplat12\\main.py', base=base, targetName = 'main.exe')
]

setup(name='postbuild',
      version = '1.0',
      author = "kanwairen",
      description = 'tool',
      # options = dict(build_exe = buildOptions),
      executables = executables,
      # options={"build_exe": {"includes": includes, "include_files": include_files, "excludes": ["PyQt5", "numpy", "notebook"], "optimize":2, "compressed":1}})
      options={"build_exe": dict(includes = includes, include_files = include_files, excludes = ["PyQt5", "numpy", "notebook"], optimize = 2)})
