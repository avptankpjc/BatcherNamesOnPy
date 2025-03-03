


import os, sys, re
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk


class BatcherNameApp:

    def __init__(self, root):

        self.root = root
        self.root.title("Batcher Names for Rename in Batch")
        self.root.geometry("800x600")

        #Variables basic
        self.selected_files = []
        self.new_name = tk.StringVar()
        self.prefix = tk.StringVar()
        self.suffix = tk.StringVar()

        #Variables for Advanced Settings
        self.separator_var = tk.StringVar(value="none")
        self.custom_separator = tk.StringVar()
        
        #Mode renamed: "none" (default), common options or "custom"
        self.mode_var = tk.StringVar(value="none")
        
        #Checkbox for enumated prefix
        self.enumerated_prefix_var = tk.BooleanVar()

        #Radiobutton for suffix handling: "keep" (default) or "delete"
        self.suffix_mode = tk.StringVar(value="keep")

        #History and control
        self.file_data = {}
        self.check_vars = []
        
        #Mapping of Treeview path in the file
        self.item_to_file = {}

        #Counter global for prefix enumerated
        self.global_prefix_counter = 1

        #Area - Canvas and Scrollbar for main layout
        self.canvas = tk.Canvas(self.root)

        self.scrollbar = ttk.Scrollbar(
            self.root, orient="vertical", 
            command=self.canvas.yview
        )
        
        self.scrollbar_frame = tk.Frame(self.canvas)
        self.scrollbar_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")) 
        )

        self.canvas.create_window(
            (0,0), 
            window=self.scrollbar_frame, anchor="nw")
        
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self.create_widgets()

    def create_widgets(self):

        main_frame = tk.Frame(self.scrollbar_frame)
        main_frame.pack(padx=50, pady=25, expand=True)

        global_check_frame = tk.Frame(main_frame)
        global_check_frame.pack(pady=5, anchor="w")

        self.select_all_var = tk.BooleanVar(value=True)
        
        tk.Checkbutton(global_check_frame,
                       text="Select All",
                       variable=self.select_all_var,
                       command=self.toggle_all).pack(side="left", padx=5)


 

       

        #Panel Top: Select All (Button) and Select Files(BTN)
    
        
        tk.Button(main_frame,
                  text="Select Files",
                  command=self.select_files,
                   background="#75A9A2").pack(pady=10, anchor="center")

        #Treeview of selected files
        tk.Label(main_frame,
                 text="Files Selected:").pack(pady=10)
        
        #Button Clear Files
        tk.Button(main_frame,
                  text="Clear Files",
                  command=self.clear_list,
                  background="#FFADC9").pack(side="top", anchor="ne", pady=10)

        tree_frame = tk.Frame(main_frame)
        tree_frame.pack(pady=5, fill="x")

        
        self.tree = ttk.Treeview(tree_frame,
                                 columns=("Select",
                                          "Original",
                                          "New Name",
                                          "Status"),
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

        self.tree.pack(side="left", 
                       fill="both", 
                       expand=True)
        
        tree_scrollbar = ttk.Scrollbar(tree_frame,
                                       orient="vertical",
                                       command=self.tree.yview)
        
        self.tree.configure(yscrollcommand=tree_scrollbar)


        tk.Label(main_frame, 
            text="History Changes: ").pack(pady=5)
        
        #Treeview Historical Changes

        history_frame = tk.Frame(main_frame)
        history_frame.pack(pady=5, fill="x")

      
        #Button Clear
        tk.Button(history_frame,
            text="Clear History",
            command=self.clear_history,
            background="#FFADC9").pack(side="top", anchor="ne", padx=5, pady=12)

        self.history_tree = ttk.Treeview(
                        history_frame,
                        columns=("Original",
                                 "New Name",
                                 "Status"),
                                 show="headings",
                                 height=6                 
                        )
        
        self.history_tree.heading("Original",text="Original")
        self.history_tree.heading("New Name", text="New Name")
        self.history_tree.heading("Status", text="Status")

        self.history_tree.column("Original", width=200)
        self.history_tree.column("New Name", width=200)
        self.history_tree.column("Status", width=100)

        self.history_tree.pack(side="left", fill="both", expand=True)

        history_scrollbar = ttk.Scrollbar(history_frame, 
                                          orient="vertical",
                                          command=self.history_tree.yview
                                          )
        history_scrollbar.pack(side="right", fill="y")

        self.history_tree.configure(yscrollcommand=history_scrollbar.set)


        pan_ops_frame = tk.Frame(main_frame)
        pan_ops_frame.pack(anchor="e", fill="x")

        tk.Button(pan_ops_frame, 
                  text="Reset All Fields", 
                  command=self.reset_all, background="#ED6A5A").pack(side="left", padx=5, pady=10)


        #rename_frame_01 = tk.Frame(main_frame)
        #rename_frame_01.pack(anchor="e", fill="x")

        #Buttons Main Actions
        tk.Button(pan_ops_frame,
                  text="Rename Files",
                  command=self.rename_files, background="#6F8AEB").pack(side="right", pady=10)  
              
        #Fields Basic Inputs
        tk.Label(main_frame, text="New Name: ").pack(pady=5)
        tk.Entry(main_frame, 
                 textvariable=self.new_name, 
                 width=20).pack(pady=5)

        tk.Label(main_frame, text="Prefix:").pack(pady=5)
        tk.Entry(main_frame, 
                 textvariable=self.prefix,
                 width=15).pack(pady=5)
        
        tk.Label(main_frame, text="Suffix:").pack(pady=5)
        tk.Entry(main_frame,
                 textvariable=self.suffix,
                 width=15
                 ).pack(pady=5)
        
        
        
       
        
        #----------- Sep Advance ------------------
        tk.Label(main_frame,
                 text="=============== Advance Options ===============").pack(pady=5)

        #Options advance - Select Separator
        tk.Label(main_frame, text="Select Separator").pack(pady=5)
        for sep, label in [("none", "None"), 
                           ("_", "_"),
                           (".","."),
                           (",",","),
                           (";",";"),
                           ("custom","Custom")]:
            tk.Radiobutton(main_frame, 
                           text=label,
                           variable=self.separator_var,
                           value=sep
                           ).pack(anchor="w")
        
            
        tk.Label(main_frame, text="Enter Separator: ").pack(anchor="w")
        
        tk.Entry(main_frame,
                 textvariable=self.custom_separator,
                 width=5).pack(pady=5, anchor="w")


        #Options Adnvae - Select Mode Renamed
        tk.Label(main_frame, text="Rename Mode:").pack(pady=10)
        for mode_val, mode_label in [
                                ("none","None"),
                                ("replace_after", "Replace After(Keep before text)"),
                                ("replace_before", "Replace Before(Keep after text)")
                                ]:
            tk.Radiobutton(main_frame,
                           text=mode_label,
                           variable=self.mode_var,
                           value=mode_val).pack(anchor="w")
        

        #Options Advance - Handle of Suffix
        tk.Label(main_frame, text="Suffix Handling").pack(pady=10)
        tk.Checkbutton(main_frame,
                       text="Enumerated Prefix",
                       variable=self.enumerated_prefix_var
                       ).pack(pady=10, anchor="w")
        
        tk.Radiobutton(main_frame, 
                       text="Keep Suffix", 
                       variable=self.suffix_mode, 
                       value="Keep").pack(anchor="w")
        
        tk.Radiobutton(main_frame,
                       text="Delete Suffix",
                       variable=self.suffix_mode,
                       value="Delete").pack(anchor="w")

        self.tree.bind("<ButtonRelease-1>", self.toggle_checkbox)



    
    def reset_all(self):
        self.new_name.set("")
        self.prefix.set("")
        self.suffix.set("")
        self.separator_var.set("none")
        self.custom_separator.set("")
        self.mode_var.set("none")
        self.suffix_mode.set("keep")
        self.enumerated_prefix_var.set(False)
        self.select_all_var.set(True)
    
    def select_files(self):
        files = filedialog.askopenfilenames(
            title="Select Files",
            filetypes=(
                ("All Files", "*.*"),
                ("Text Files", "*.txt" )
            )
        )
        if files:
            new_files = [file for file in files if file not in self.selected_files]
            self.selected_files.extend(new_files)

            for file in new_files:
                org_name = os.path.basename(file)
                item_id = self.tree.insert("", "end", 
                                           values=["✓",
                                                   org_name,
                                                   "",
                                                   "Pending"])
                self.item_to_file[item_id] = file 

    
    def toggle_checkbox(self, event):
        region = self.tree.identify_region(event.x, event.y)
        if region == "cell":
            item_id = self.tree.identify_row(event.y)
            current_values = self.tree.item(item_id, "values")
            if len(current_values) < 4:
                return
            new_state = "✗" if current_values[0] == "✓" else "✓"
            self.tree.item(item_id, 
                           values=[new_state] + list(current_values[1:]))

        

    def toggle_all(self):
        new_state = "✓" if self.select_all_var.get()  else "✗"
        for item_id in self.tree.get_children():
            current_values = self.tree.item(item_id, "values")
            if len(current_values) < 4:
                continue
            self.tree.item(item_id, 
                           values=[new_state] + list(current_values[1:]))

    
    def clear_list(self):
        self.tree.delete(*self.tree.get_children())
        self.selected_files.clear()
        self.item_to_file.clear()
        

    def clear_history(self):
        self.history_tree.delete(*self.history_tree.get_children())
        self.file_data.clear()
        self.global_prefix_counter = 1

    def _on_mousewheel(self, event):
        if event.widget.winfo_class() == "Treeview":
            return
        self.canvas.yview_scroll(int(-1 *(event.delta / 100)), "units")


    def rename_advance(self, original,
                       new_name_val,
                       prefix_val,
                       suffix_val,
                       enumerated_prefix,
                       enumeration_number):
        
        base, ext = os.path.splitext(original)

        sep = self.separator_var.get()

        if sep == "custom":
            sep = self.custom_separator.get()

        if sep == "none" or sep not in base:
            new_parts = []

            if prefix_val:
                new_parts.append(f"{prefix_val}{enumeration_number:02d}" if enumerated_prefix else prefix_val)
            new_parts.append(new_name_val if new_name_val else base)

            if suffix_val:
                new_parts.append(suffix_val)
            return "_".join(new_parts) + ext
        
        mode = self.mode_var.get()

        if mode == "replace_after":
            #Separte in 2 parts the first apartion of separator
            prefix_part, remainder = base.split(sep, 1)

            # Try to extract numeric suffix in the end (p.ej. _001)
            m = re.match(r'^(.*)(' + re.escape(sep) + r'\d+)$', remainder)

            if m:
                core_part = m.group(1)
                orig_suffix = m.group(2)

            else:
                core_part = remainder
                orig_suffix = ""

            #New Prefix
            new_prefix = (f"{prefix_val}{enumeration_number:02d}"
                          if prefix_val and enumerated_prefix else (prefix_val if prefix_val else prefix_part))

            #New Core
            new_core = new_name_val if new_name_val else core_part

            #New Suffix
            if suffix_val:
                new_suffix = suffix_val if suffix_val.startswith(sep) else sep + suffix_val
            else:
                new_suffix = orig_suffix if self.suffix_mode.get() == "keep" else ""
            
            res_str = new_prefix + sep + new_core + new_suffix  + ext
            
            return res_str
        
        elif mode == "replace_before":

            parts = base.rsplit(sep, 1)
            if len(parts) == 2:
                left_part, right_part = parts

                if right_part.isdigit():
                    orig_suffix = sep + right_part
                else:
                    orig_suffix = ""

            else:
                left_part = base
                orig_suffix = ""

            new_text = new_name_val if new_name_val else (f"{prefix_val}{enumeration_number:02d}"
                                                          if prefix_val and enumerated_prefix else (prefix_val if prefix_val else left_part))
            
            if suffix_val:
                new_suffix = suffix_val if suffix_val.startswith(sep) else sep + suffix_val
            else:
                new_suffix = orig_suffix if self.suffix_mode.get() == "keep" else ""
            
            res_str2 = new_text + new_suffix + ext
            return res_str2
        
        else:
            #Mode "none" join the field in order
            new_parts = []
            if prefix_val:
                new_parts.append(f"{prefix_val}{enumeration_number:02d}"
                                 if enumerated_prefix else prefix_val)
                
            new_parts.append(new_name_val if new_name_val else base)

            if suffix_val:
                new_parts.append(suffix_val)

            return "_".join(new_parts) + ext


    def rename_files(self):
        new_name_val = self.new_name.get().strip().replace(" ", "_")
        prefix_val = self.prefix.get().strip().replace(" ", "_")
        suffix_val = self.suffix.get().strip().replace(" ", "_")

        if not self.selected_files:
            messagebox.showwarning("Warning", "No File Selected !!!!")
            return
        
        if not new_name_val and not prefix_val and not suffix_val:
            messagebox.showwarning("Warning", "You must enter a new name, prefix or suffix")
            return
        
        selected_items = [item_id for item_id in self.tree.get_children() 
                          if self.tree.item(item_id, "values")[0] == "✓"]

        if not selected_items:
            messagebox.showinfo("Info", "No changes made because no file was selected !!!")
            return
        
        new_files = []
        rename_items = []

        for item_id in selected_items:
            file_path = self.item_to_file.get(item_id)

            if not file_path:
                continue
            org_name = os.path.basename(file_path)
            dir_name = os.path.dirname(file_path)

            #-------------------
            #Part of Advance Options
            if self.separator_var.get() != "none" or self.mode_var.get() != "none":
                if self.enumerated_prefix_var.get():
                    enum_num = self.global_prefix_counter
                    self.global_prefix_counter += 1
                
                else:
                    enum_num = 0
                update_name = self.rename_advance(
                    original=org_name,
                    new_name_val=new_name_val,
                    prefix_val=prefix_val,
                    suffix_val=suffix_val,
                    enumerated_prefix=self.enumerated_prefix_var.get(),
                    enumeration_number=enum_num
                )
            else:
                base, ext = os.path.splitext(org_name)
                if self.suffix_mode.get() == "delete":
                    base = base.split("_", 1)[1]

                new_base = new_name_val if new_name_val else base
                
                if prefix_val:
                    if self.enumerated_prefix_var.get():
                        new_base = f"{prefix_val}{self.global_prefix_counter:02d}_{new_base}"
                        self.global_prefix_counter += 1
                    else:
                        new_base = f"{prefix_val}_{new_base}"
                if suffix_val:
                    new_base = f"{new_base}_{suffix_val}"
                update_name = new_base + ext

            base_new, ext_new = os.path.splitext(update_name)

            if os.path.exists(os.path.join(dir_name, update_name)) or update_name in new_files:
                counter = 1
                candidate = f"{base_new}_{counter:03d}{ext_new}"
                
                while os.path.exists(os.path.join(dir_name, candidate)) or candidate in new_files:
                    counter += 1
                    candidate = f"{base_new}_{counter:03d}{ext_new}"
                update_name = candidate

            new_path = os.path.join(dir_name, update_name)

            try:
                os.rename(file_path, new_path)
            except Exception as e:
                messagebox.showwarning("Error", 
                                       f"Could not rename {org_name}: {e}")
                continue

            new_files.append(new_path)
            self.history_tree.insert("", "end", values=(
                                        org_name,
                                         update_name,
                                         "Renamed" ))
            self.tree.item(item_id, 
                           values=["✓", org_name, update_name, "Renamed"])

            rename_items.append(item_id)
            
            if file_path in self.selected_files:
                self.selected_files.remove(file_path)
            del self.item_to_file[item_id]

        for item_id in rename_items:
            self.tree.delete(item_id)

        messagebox.showinfo("Succes", "Files renamed successfully")




def runapp():
    root = tk.Tk()
    
    icon_filename = "A00_1_Logo_BatcherName_256.ico"
    uri_local = "assets/img/icon_logo/A00_1_Logo_BatcherName_256.ico"

    if getattr(sys, 'frozen', False):
        base_dir = os.path.dirname(sys.executable)
        icon_path = os.path.join(base_dir, icon_filename)
    
    else:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        icon_path = os.path.join(base_dir, uri_local )
    
    if os.path.exists(icon_path):
        try:
            root.iconbitmap(icon_path)
        except Exception as e:
            print(f"Failed to load icon: {e}")
    else:
        print(f"Wargning: Not Found Icon in {icon_path}")

    status_frame = tk.Frame(root, bd=1, relief=tk.SUNKEN)
    status_frame.pack(side=tk.BOTTOM, fill=tk.X)
    version_label = tk.Label(status_frame, text="[v1.1.0]", anchor="e")
    version_label.pack(fill=tk.X)

    app = BatcherNameApp(root)

    root.mainloop()


if __name__ == "__main__":
    runapp()
    