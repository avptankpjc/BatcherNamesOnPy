
import sys
import os

import tkinter as tk
from view.batcherview import BatcherView
from tkinterdnd2 import TkinterDnD


#sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))


def runapp():
    root = TkinterDnD.Tk()
    app = BatcherView(root)
    root.mainloop()
    


if __name__ == "__main__":
    runapp()
    
    
    
