#    <BatcherNameOnPy, App to Rename for Batch/Lotes.>
#    Copyright (C) <2025> <AvpTankPowerJC>
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program. If not, see <http://www.gnu.org/licenses/>.


import sys
import os

import tkinter as tk
from tkinter import ttk
from tkinterdnd2 import TkinterDnD

from arc.view.batcherview import BatcherView



#sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))


def runapp():
    
    root = TkinterDnD.Tk()
    
    icon_filename = "A01_2_Logo_Icon_BatcherName.ico"
    icon_relative_path = "assets/img/icon_logo/A01_2_Logo_Icon_BatcherName.ico"
    
    if getattr(sys, "frozen", False):
        base_dir = os.path.dirname(sys.executable)
        icon_path = os.path.join(base_dir, icon_filename)
    else:
        #Mode Develop
        base_dir = os.path.dirname(os.path.abspath(__file__))  
        icon_path = os.path.join(base_dir, icon_relative_path)
    
    if os.path.exists(icon_path):
        try:
            root.iconbitmap(icon_path)
        except Exception as e:
            print(f"Failed to load icon: {e}")
    else:
        print(f"Warning: Icon not found at {icon_path}")

    status_frame = tk.Frame(root, bd=1, relief=tk.SUNKEN)
    status_frame.pack(side=tk.BOTTOM, fill=tk.X)
    
    version_label = tk.Label(status_frame, text="[1.2.0]", anchor="e")
    version_label.pack(fill=tk.X)
    
    #Start App
    app = BatcherView(root)
    root.mainloop()
    


if __name__ == "__main__":
    runapp()
    
    
    
