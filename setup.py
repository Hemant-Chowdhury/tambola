import cx_Freeze
import sys

base = None

if sys.platform == 'win32':
    base = "Win32GUI"

executables = [cx_Freeze.Executable("__main__.py", base=base)]

cx_Freeze.setup(
    name="tambola",
    options={"build_exe": {"packages": ["tkinter"], "include_files": []}},
    version="0.01",
    description="tambola game",
    executables=executables
)
