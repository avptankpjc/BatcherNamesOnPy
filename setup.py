


import sys
from cx_Freeze import setup, Executable


#For add Icon
#executables = [Executable("tu_script.py", base=base, icon="icono.ico")]
build_exe_options = {
    "packages":["tkinter", "os"],
    "excludes":[]
}

base = None
if sys.platform == "win32":
    base = "Win32GUI"


setup(
    name="BatcherNameApp",
    verion="1.0.0",
    description="Applications for rename files by batch",
    author="Avptankpowerjc",
    options={"build_exe":build_exe_options},
    executable=[Executable("codec_total_app.py", base=base) ]

)



