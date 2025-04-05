


import sys, os
from cx_Freeze import setup, Executable

#python_install_dir = sys.base_prefix
#tcl_dll = os.path.join(python_install_dir, "DLLs", "tcl86t.dll")
#tk_dll = os.path.join(python_install_dir, "DLLs", "tk86t.dll")


#For add Icon
#executables = [Executable("tu_script.py", base=base, icon="icono.ico")]

build_exe_options = {
    "packages":["tkinter", "os"],
    "excludes":[],
     "include_files": [
        ("assets/img/icon_logo/A00_1_Logo_BatcherName_256.ico")
    ]
    #"include_files":[
    #    (tcl_dll, "tcl86t.dll"),
    #    (tk_dll, "tk86t.dll"),
    #],
    #"include_msvcr": True 
}

base = None
if sys.platform == "win32":
    base = "Win32GUI"


setup(
    name="BatcherNameApp",
    version="1.1.2",
    description="Applications for rename files by batch",
    author="Avptankpowerjc",
    options={"build_exe":build_exe_options},
    executables=[Executable("apprun.py", base=base, icon="assets/img/icon_logo/A00_1_Logo_BatcherName_256.ico") ]
)




