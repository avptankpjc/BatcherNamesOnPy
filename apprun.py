
import sys
import os

import tkinter as tk
from tkinter import ttk
from tkinterdnd2 import TkinterDnD

from view.batcherview import BatcherView



#sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))


def runapp():
    
    root = TkinterDnD.Tk()
    
    icon_filename = "A00_2_Logo_BatcherName.ico"
    icon_relative_path = ""
    
    if getattr(sys, "frozen", False):
        base_dir = os.path.dirname(sys.executable)
        
    else:
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
    
    
    
