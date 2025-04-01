
import sys
import os

import tkinter as tk
from view.batcherview import BatcherView


#sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))


def runapp():
    root = tk.Tk()
    app = BatcherView(root)
    root.mainloop()
    


if __name__ == "__main__":
    runapp()
    
    
    
