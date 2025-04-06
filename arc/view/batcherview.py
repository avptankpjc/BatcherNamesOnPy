
import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from arc.viewmod.batcherviewmodel import BatcherViewModel


class BatcherView:
    
    def __init__(self, root):
        
        #super().__init__(root)
        
        self.root = root
        self.root.title("Batcher Renamer")
        self.root.geometry("800x600")
        
        
       
        
        #Area - Canvas/Scrollbar for layout
        self.canvas = tk.Canvas(self.root)
        self.scrollbar = ttk.Scrollbar(self.root, 
                                       orient="vertical",
                                       command=self.canvas.yview)
        
        self.scrollbar_frame = tk.Frame(self.canvas)
        self.scrollbar_frame.bind("<Configure>",
                                  lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))        
        
        self.canvas.create_window((0,0),
                                  window=self.scrollbar_frame, anchor="nw")
        
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.canvas.bind_all("<MouseWheel>", 
                             self._on_mousewheel)
        
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        
        self.list_seps = [("none", "None"),
                          ("_", "_"),
                          (".", "."),
                          (",",","),
                          (";",";"),
                          ("custom","Custom")]
        
        self.list_modes = [("none", "None"),
                           ("replace_after", "Replace After (Keep before text)"),
                           ("replace_before", "Replace Before (Keep after text)")
                           
                           ]
        
        self.vm = BatcherViewModel(self.root)
        self.vm.set_view(self)
        
        self.create_widgets()
        
        self.vm.register_tree(self.tree)
      
        
    def create_widgets(self):
        
        main_frame = tk.Frame(self.scrollbar_frame)
        main_frame.pack(padx=50, pady=50, fill="both", expand=True)

        global_check_frame = tk.Frame(main_frame)
        global_check_frame.pack(pady=5, anchor="w")
        
        self.select_all_var = tk.BooleanVar(value=True)

        tk.Checkbutton(global_check_frame, 
                       text="Select All",
                       variable=self.select_all_var,
                       command=self.vm.toggle_all).pack(side="left", padx=5)
        

        tk.Button(main_frame, 
                  text="Select Files", 
                  command=self.select_files,
                  background="#75A9A2").pack(side="top", pady=5, anchor="center")
        
        tk.Button(main_frame,
                  text="Select Folders",
                  command=self.select_folders,
                  background="#75a9f2").pack( pady=5, anchor="ne")
        
        
        btn_tree_frameTop = tk.Frame(main_frame)
        btn_tree_frameTop.pack(pady=5, fill="both")
        
        tk.Button(btn_tree_frameTop,
                  text="Clear All Files",
                  command=self.clear_file_tree,
                  background="#FFADC9").pack(side="left",pady=10, anchor="nw")
        
       
        tree_frame = tk.Frame(main_frame)
        tree_frame.pack(pady=5, fill="x")
        
        self.tree = ttk.Treeview(tree_frame, 
                                 columns=("Select", "Original", "New Name", "Status"),
                                 show="headings",
                                 height=8)
        
        self.tree.heading("Select", text="Select")
        self.tree.heading("Original", text="Original")
        self.tree.heading("New Name", text="New Name")
        self.tree.heading("Status", text="Status")
        
        self.tree.column("Select", width=50)
        self.tree.column("Original", width=200)
        self.tree.column("New Name", width=200)
        self.tree.column("Status", width=100)
        
        self.tree.pack(side="left", fill="both", expand=True)
        tree_scrollbar = ttk.Scrollbar(tree_frame,
                                       orient="vertical",
                                       command=self.tree.yview)
        
        tree_scrollbar.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=tree_scrollbar.set)
        
        tk.Button(main_frame,
                  text="Clear Item",
                  command=self.delete_select_item,
                  background="#F000FD").pack( side="right",pady=5, anchor="ne")
        
        
        #Area History
        tk.Label(main_frame, text="History Changes").pack(pady=15)
        
        history_frame = tk.Frame(main_frame)
        history_frame.pack(pady=5, fill="x")
        
        tk.Button(history_frame, text="Clear History",
                  command=self.clear_history, background="#FFADC9").pack(side="top", anchor="nw", padx=5, pady=12)
        
        self.history_tree = ttk.Treeview(history_frame, 
                                         columns=("Original", "New Name", "Status"),
                                         show="headings",
                                         height=6)
        
        self.history_tree.heading("Original", text="Original")
        self.history_tree.heading("New Name", text="New Name")
        self.history_tree.heading("Status", text="Status")
        
        self.history_tree.column("Original", width=200)
        self.history_tree.column("New Name", width=200)
        self.history_tree.column("Status", width=100)
        
        self.history_tree.pack(side="left", fill="both", expand=True)
        
        history_scrollbar = ttk.Scrollbar(history_frame, 
                                          orient="vertical",
                                          command=self.history_tree.yview)
        
        history_scrollbar.pack(side="right", fill="y")
       
        self.history_tree.configure(yscrollcommand=history_scrollbar.set)
        
        pan_ops_frame = tk.Frame(main_frame)
        pan_ops_frame.pack(pady=5, fill="x")
        
        tk.Button(pan_ops_frame, text="Reset All Field",
                  command=self.vm.reset_fields, 
                  background="#ED6A5A").pack(side="left",  pady=5)
        
        
        tk.Button(pan_ops_frame, text="Rename Files", 
                 command=self.vm.rename_files,
                 background="#396693").pack(side="right", pady=5)
        
        #Fields Inputs Operations Prefix/Suffix
        tk.Label(main_frame, text="New Name: ").pack(pady=5)
        tk.Entry(main_frame, textvariable=self.vm.new_name, width=100).pack(pady=5)
        tk.Label(main_frame, text="Prefix: ").pack(pady=5)
        tk.Entry(main_frame, textvariable=self.vm.prefix, width=50).pack(pady=5)
        tk.Label(main_frame, text="Suffix: ").pack(pady=5)
        tk.Entry(main_frame, textvariable=self.vm.suffix, width=50).pack(pady=5)

        #--------------------------
        #// Advance Options //
        tk.Label(main_frame, text="================ Advance Options ================").pack(pady=6)
        tk.Label(main_frame, text="Select Separator").pack(pady=5)
        
        for sep, label in self.list_seps:
            tk.Radiobutton(main_frame, text=label, variable=self.vm.separator_var, value=sep ).pack(anchor="w")
        
        tk.Label(main_frame, text="Enter Separator: ").pack(anchor="w")
        tk.Entry(main_frame, textvariable=self.vm.custom_separator, width=5).pack(pady=5, anchor="w")
        
        tk.Label(main_frame, text="Rename Mode").pack(pady=10)
        
        for mode_val, mode_label in self.list_modes:
            tk.Radiobutton(main_frame, text=mode_label, variable=self.vm.mode_var, value=mode_val).pack(anchor="w")
        
        tk.Label(main_frame, text="Suffix Handling").pack(pady=10)
        tk.Checkbutton(main_frame, text="Enumerated Prefix", variable=self.vm.enumerated_prefix_var).pack(pady=10)
        
        
        tk.Radiobutton(main_frame, text="None (Neutral)",variable=self.vm.suffix_mode,  value="none").pack(anchor="w")
        tk.Radiobutton(main_frame, text="Keep Suffix",   variable=self.vm.suffix_mode,  value="keep").pack(anchor="w")
        tk.Radiobutton(main_frame, text="Delete Suffix", variable=self.vm.suffix_mode, value="delete").pack(anchor="w")
        
        self.tree.bind("<ButtonRelease-1>",
                       self.vm.toggle_checkbox)
        
    def _on_mousewheel(self, event):
        if event.widget.winfo_class() == "Treeview":
            return
        self.canvas.yview_scroll(int(-1 * (event.delta / 100)), "units")


    def select_files(self):
        self.vm.select_files()
            
    def select_folders(self):
        self.vm.select_folders()
        

    def select_onefoldes(self):
        self.vm.select_onefolder()
        
    def delete_select_item(self):
        self.vm.delete_selected_item()

    def clear_file_tree(self):
        self.tree.delete(*self.tree.get_children())
        self.vm.selected_files.clear()
        self.vm.item_to_file.clear()
        
        
    def clear_history(self):
        self.history_tree.delete(*self.history_tree.get_children())
        self.vm.file_data.clear()
        self.vm.global_prefix_counter = 1
        
        
    def show_warning(self, msg):
        messagebox.showwarning("Warning", msg)
        
    def show_info(self, msg):
        messagebox.showinfo("Info", msg)
        
    

