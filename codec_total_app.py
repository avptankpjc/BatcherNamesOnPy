


import os, sys

"""
if sys.platform == "win32" and hasattr(os, "add_dll_directory"):
    dll_dir = os.path.join(sys.base_prefix, "DLLs")
    if os.path.isdir(dll_dir):
        os.add_dll_directory(dll_dir)
    else:
        print(f"Warning: DLL directory not found: {dll_dir}")
"""

import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk

icon_path = "assets/img/icon_logo/A00_1_Logo_BatcherName_256.ico"



class BatcherNameApp:

    def __init__(self, root):

        self.root = root
        self.root.title("Batcher Names for Rename in Batch")
        self.root.geometry("800x600")

        #Varibables
        self.selected_files = []
        self.new_name =  tk.StringVar()
        self.prefix = tk.StringVar()
        self.suffix = tk.StringVar()

        #Presistence temp in memory
        #Store the Original Names like keys and new names like values
        self.file_data = {}

        #Variables for control checkboxes(optcional)
        self.check_vars = []

        #Area - Create Canvas, Scrollbar
        self.canvas = tk.Canvas(self.root)
        self.scrollbar = ttk.Scrollbar(self.root, 
                                       orient="vertical",
                                       command=self.canvas.yview)
        
        self.scrollbar_frame = tk.Frame(self.canvas)

        self.scrollbar_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        #Configure Canvas
        self.canvas.create_window((0,0), 
                                  window=self.scrollbar_frame,
                                  anchor="nw")
        self.canvas.configure(
                        yscrollcommand=self.scrollbar.set
                        )

        #Enabled Event MouseWheel
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

        #Packging Canvas and Scrollbar
        self.canvas.pack(
                    side="left", 
                    fill="both", 
                    expand=True
        )
        
        self.scrollbar.pack(side="right", fill="y")


        self.create_widgets()

    
    def create_widgets(self):

        main_frame = tk.Frame(self.scrollbar_frame)
        main_frame.pack(padx=10, pady=10, expand=True)

        global_check_frame = tk.Frame(main_frame)
        global_check_frame.pack(pady=5)

        self.select_all_var = tk.BooleanVar(value=True)
        tk.Checkbutton(global_check_frame, text="Select All", variable=self.select_all_var, command=self.toggle_all).pack(side="left", padx=5)
        


        #Tag for Select Files
        tk.Label(main_frame, text="Files Selected:").pack(pady=10)

        # ---- Frames - TreeView 01
        tree_frame = tk.Frame(main_frame)
        tree_frame.pack(pady=5, fill="x")

        self.tree = ttk.Treeview(
            tree_frame,
            columns=("Select", "Original", "New Name", "Status" ),
            show="headings",
            height=8
        )

        self.tree.heading("Select", text="Select")
        self.tree.heading("Original", text="Original")
        self.tree.heading("New Name", text="New Name")
        self.tree.heading("Status", text="Status")

        self.tree.column("Select", width=50)
        self.tree.column("Original", width=200)
        self.tree.column("New Name", width=200)
        self.tree.column("Status", width=100)

        self.tree.pack(side="left", fill="both", expand=True)

        #Scrollbar independietn for the 1er Treeview
        tree_scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        tree_scrollbar.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=tree_scrollbar.set)

        

        #Area Historial Changes
        tk.Label(main_frame,
                 text="History Changes:").pack(pady=5)


        # --- Frames 2 - History
        history_frame = tk.Frame(main_frame)
        history_frame.pack(pady=5, fill="x")

        self.history_tree = ttk.Treeview(
            history_frame,
            columns=("Original", "New Name", "Status"),
            show="headings",
            height=6
        )

        self.history_tree.heading("Original", text="Original")
        self.history_tree.heading("New Name", text="New Name")
        self.history_tree.heading("Status", text="Status")

        self.history_tree.column("Original", width=200)
        self.history_tree.column("New Name", width=200)
        self.history_tree.column("Status", width=100)

        self.history_tree.pack(side="left", fill="both", expand=True)

        #--- History Scrollbar
        history_scrollbar = ttk.Scrollbar(
            history_frame, 
            orient="vertical", 
            command=self.history_tree.yview)
        history_scrollbar.pack(side="right", fill="y")
        self.history_tree.configure(yscrollcommand=history_scrollbar.set)

        #Buttons Part 01
        #Button for "Select Files"
        tk.Button(main_frame, text="Select Files", command=self.select_files).pack(pady=10)

        #Inputs Part 01
        #Input - New Name
        tk.Label(main_frame, text="New Name:").pack(pady=5)
        tk.Entry(main_frame, textvariable=self.new_name, width=30).pack(pady=5)
        
        #Input - Prefix
        tk.Label(main_frame, text="Prefix:").pack(pady=5)
        tk.Entry(main_frame, textvariable=self.prefix, width=20).pack(pady=5)
          
        #Input - Suffix
        tk.Label(main_frame, text="Suffix:").pack(pady=5)
        tk.Entry(main_frame, textvariable=self.suffix, width=20).pack(pady=5)


        tk.Button(main_frame, text="Rename", command=self.rename_files).pack(pady=10)
        tk.Button(main_frame, text="Clear Files", command=self.clear_list).pack(pady=10)
        tk.Button(main_frame, text="Clear History", command=self.clear_history).pack(pady=10)

        #Bind event click to link checkbox state
        self.tree.bind("<ButtonRelease-1>", self.toggle_checkbox) 


    def select_files(self):

        files = filedialog.askopenfilenames(
            title="Select Files",
            filetypes=(
                ("All Files", "*.*"),
                ("Text Files", "*.txt")
            )
        )

        if files:
            new_files = [file for file in files if file not in self.selected_files]
            self.selected_files.extend(new_files)

            for file in new_files:
                org_name = os.path.basename(file)
                self.check_vars.append(True)
                self.tree.insert("", "end", values=["✓", org_name, "", "Pending"])
                self.tree.tag_configure("pending", foreground="orange")

            
    def toggle_checkbox(self, event):

        region = self.tree.identify_region(event.x, event.y)

        if region == "cell":
            column = self.tree.identify_column(event.x)

            if column == "#1":
                item_id = self.tree.identify_row(event.y)
                current_values = self.tree.item(item_id, "values")

                if len(current_values) < 4:
                    return
                
                current_state = current_values[0]
                new_state = "✗" if current_state == "✓" else "✓"
                self.tree.item(item_id, values=[new_state] + list(current_values[1:]))


    def toggle_all(self):
        new_state = "✓" if self.select_all_var.get() else "✗"
        for item_id in self.tree.get_children():
            current_values = self.tree.item(item_id, "values")
            if len(current_values) < 4:
                continue
            self.tree.item(item_id, 
                           values=[new_state] + list(current_values[1:]))


    def deselect_all(self):
        for item_id in self.tree.get_children():
            current_values = self.tree.item(item_id, 
                                            "values")
            if len(current_values) < 4:
                continue
            self.tree.item(item_id, values=["✗"] + list(current_values[1:]))


    def rename_files(self):
        new_name = self.new_name.get().strip().replace(" ", "_")
        prefix = self.prefix.get().strip().replace(" ", "_")
        suffix = self.suffix.get().strip().replace(" ", "_")

        if not self.selected_files:
            messagebox.showwarning("Warning", "No Files Selected!!!")
            return
        
        if not new_name and not prefix and not suffix:
            messagebox.showwarning("Warning", "You must enter a new name, prefix or suffix")
            return
        
        try:
            next_number = 1
            #Make copy current items
            tree_items = list(self.tree.get_children())
            #Store Tuples(index, item_id)
            rename_items = []

            total_files = len(self.selected_files)

            for i in range(total_files):

                if i >= len(tree_items):
                    continue

                item_id = tree_items[i]
                current_values = self.tree.item(item_id, "values")

                if len(current_values ) < 4:
                    continue

                if current_values[0] != "✓":
                    continue

                file_path = self.selected_files[i]
                org_name = os.path.basename(file_path)
                
                dir_name = os.path.dirname(file_path)
                name, ext = os.path.splitext(org_name)

                base_name = new_name if new_name else name 
                update_name = base_name
                
                if prefix:
                    update_name = f"{prefix}_{update_name}"

                if suffix:
                    update_name = f"{update_name}_{suffix}"

                #Check the Files name withour theirs numbers
                candidate = f"{update_name}{ext}"

                if os.path.exists(os.path.join(dir_name, candidate)):
                    next_number = 1

                    while os.path.exists(os.path.join(dir_name, f"{update_name}_{next_number:03d}{ext}")):
                        next_number += 1   
                    candidate = f"{update_name}_{next_number:03d}{ext}"
                
                update_name = candidate

                new_path = os.path.join(dir_name, update_name)

                #Rename the File
                os.rename(file_path, new_path)

                #Update the Path in the List of Files
                self.selected_files[i] = new_path

                #Update the history in the memory
                self.file_data[org_name] = update_name

                exists = False
                for row in self.history_tree.get_children():
                    values = self.history_tree.item(row, "values")

                    if len(values) >= 2 and org_name == values[0] and update_name == values[1]:
                        exists = True
                        break

                if not exists:
                    self.history_tree.insert("", "end", values=[org_name, update_name, "Renamed"])

                #Update the state the Main Treeview
                self.tree.item(item_id, values=["✓", org_name, update_name, "Renamed"])

                #Store the information about the item renamed
                rename_items.append((i, item_id))

            if not rename_items:
                messagebox.showinfo("Info", "No changes made becasue no file were selected!!")
                return

            #Delete the items was renamed it in descent sorted for not affect any index.
            for idx, item_id in sorted(rename_items, key=lambda x: x[0], reverse=True):
                self.tree.delete(item_id)
                del self.selected_files[idx]

            messagebox.showinfo("Succes", "Files renamed successfully!!!!")


        except Exception as e:
            messagebox.showerror("Error", f"An error ocurred: {e}")


    def clear_list(self):
        self.tree.delete(*self.tree.get_children())
        self.check_vars.clear()
        self.selected_files.clear()

    def clear_history(self):
        self.history_tree.delete(*self.history_tree.get_children())
        self.file_data.clear()

    def _on_mousewheel(self, event):
        if event.widget.winfo_class() == "Treeview":
            return
        self.canvas.yview_scroll(int(-1 * (event.delta / 100)), "units")

if __name__ == "__main__":
    root = tk.Tk()
    
    if getattr(sys, 'frozen', False):
        # Si está congelado con cx_Freeze, usamos la carpeta del ejecutable
        base_dir = os.path.dirname(sys.executable)
    else:
        base_dir = os.path.dirname(os.path.abspath(__file__))

    icon_path = os.path.join(base_dir, "A00_1_Logo_BatcherName_256.ico")
    #print("Icon path:", icon_path)  # Para verificar la ruta

    if os.path.exists(icon_path):
        try:
            root.iconbitmap(icon_path)
        except Exception as e:
            print(f"Error al asignar el icono: {e}")
    else:
        print(f"Advertencia: No se encontró el icono en {icon_path}")

    app = BatcherNameApp(root) 
    root.mainloop()



