


import tkinter as tk
import os, re, sys
from tkinter import ttk, filedialog, messagebox
from tkinterdnd2 import TkinterDnD, DND_FILES

from arc.model.batchermodel import BatcherModel
from arc.utils.logger_conf import logger


class BatcherViewModel:
    
    def __init__(self, root):
        
        self.root = root
        self.view = None
        
        self.selected_files = []
        
        self.last_selected_folder = self.load_last_selected_folder()
        
        #Variables Inputs
        self.new_name = tk.StringVar()
        self.prefix = tk.StringVar()
        self.suffix = tk.StringVar()
        
        #Part - Advance Config
        self.separator_var = tk.StringVar(value="none")
        self.custom_separator = tk.StringVar()
        
        #Mode rename: "none"(default)
        self.mode_var = tk.StringVar(value="none")   
        self.enumerated_prefix_var = tk.BooleanVar()   
        self.suffix_mode = tk.StringVar(value="none")
        
        #Historial - control
        self.file_data = {}
        self.check_vars = []
        
        #Maping Treewview
        self.item_to_file = {}
        
        self.global_prefix_counter = 1
        
        
        
    def set_view(self, view):
        self.view = view
        
     
    def register_tree(self, tree):
        tree.drop_target_register(DND_FILES)
        tree.dnd_bind("<<Drop>>", self.on_drop)
    
    
    def save_last_selected_folder(self):
        """Save the last folder selected"""
        try:
            
            logger.info("Initialize Save Files")
            
            with open("last_selected_folder.txt","w") as file:
                file.write(self.last_selected_folder)
        
        except Exception as e:
            print(f"Error saving last folder: {e}")
            
    def load_last_selected_folder(self):
        """Load the last Folder Selected"""
        try:
            
            if os.path.exists("last_selected_folder.txt"):
                with open("last_selected_folder.txt", "r") as file:
                    folder =  file.read().strip()
                    if os.path.isdir(folder):
                        return folder
                    
        except Exception as e:
            print(f"Error loading the last folder: {e}")
            
        return os.getcwd()
    
    
    def select_files(self):
        initial_dir = self.last_selected_folder
        
        # Primero, intentar seleccionar archivos
        files = filedialog.askopenfilenames(
            title="Select Files",
            filetypes=(("All Files", "*.*"), ("Text Files", "*.txt")),
            initialdir=initial_dir
        )
        
        if files:
            self._add_files_and_folders(files)
            self.last_selected_folder = os.path.dirname(files[0])
            self.save_last_selected_folder()
            
    def select_onefolder(self):
        folder = filedialog.askdirectory(title="Select Folders")
        
        if folder:
            self._add_files_and_folders([folder])
        
    
           
    def select_folders(self):
        
        initial_dir = self.last_selected_folder
        
        # Usar el cuadro de diálogo para seleccionar una carpeta
        folder = filedialog.askdirectory(title="Select Folders", initialdir=initial_dir)
        
        if folder:
            # Verificar si la carpeta no está ya en la lista de archivos seleccionados
            if folder not in self.selected_files:
                self.selected_files.append(folder)
                
                name = os.path.basename(folder)
                dis_text = f"[Folder] {name}"
                val_lis = ["✓", dis_text, "", "Pending"]
                
                #self._add_files_and_folders([folder])
                item_id = self.view.tree.insert("","end", values=val_lis)
                self.item_to_file[item_id] = folder
                # Mostrar la carpeta seleccionada en el árbol
                
                self.last_selected_folder = initial_dir
                self.save_last_selected_folder()
                
    
    def toggle_checkbox(self, event):
        region = self.view.tree.identify_region(event.x, event.y)
        
        if region == "cell":
            item_id = self.view.tree.identify_row(event.y)
            current_values = self.view.tree.item(item_id, "values")
            if len(current_values) < 4:
                return
            new_state = "✗" if current_values[0] == "✓" else "✓"
            self.view.tree.item(item_id, values=[new_state] + list(current_values[1:]))

    
    def toggle_all(self):
        new_state = "✓" if self.view.select_all_var.get() else "✗"
        for item_id in self.view.tree.get_children():
            current_values = self.view.tree.item(item_id, "values")
            if len(current_values) < 4:
                continue
            self.view.tree.item(item_id, values=[new_state] + list(current_values[1:]))
         
    
    def rename_files(self):
        new_name_val = self.new_name.get().strip().replace(" ", "_")
        prefix_val = self.prefix.get().strip().replace(" ", "_")
        suffix_val = self.suffix.get().strip().replace(" ", "_")
        
        if not self.selected_files:
            self.view.show_warning("No File Selected!!!")
            return
        
        if not new_name_val and not prefix_val and not suffix_val:
            self.view.show_warning("You Must Enter a name, prefix or suffix")
            return
        
        try:
            
            rename_items = []
            items_to_remove = []
            
            #To Filter the files to be mark "OK✓" before renaming.
            for item_id in self.view.tree.get_children():
                current_values = self.view.tree.item(item_id, "values")
                if current_values[0] == "✓":
                    file_path = self.item_to_file.get(item_id)
                    if file_path:
                        rename_items.append(file_path)
                        items_to_remove.append(item_id)
                        
            
            if not rename_items:
                self.view.show_warning("No Files selected for renaming, please mark files!!!")
                return 
            
            #Rename Files
            rename_pairs = BatcherModel.rename_files(
                rename_items,
                new_name_val,
                prefix_val,
                suffix_val,
                self.separator_var.get(),
                self.mode_var.get(),
                self.enumerated_prefix_var.get(),
                self.suffix_mode.get()
            )
            
            for old_path, new_path in rename_pairs:
                old_name = os.path.basename(old_path)
                new_name = os.path.basename(new_path)
                
                self.view.history_tree.insert("", "end", values=(old_name, new_name, "Renamed"))
            self.view.show_info(f"Renamed {len(rename_pairs)} items successfully!!")
            
            #--self.view.clear_file_tree() replace - this line delete all 
            #Check if exists elements peding to renaming in the Tree
            for item_id in items_to_remove:
                self.view.tree.delete(item_id)
                if item_id in self.item_to_file:
                    del self.item_to_file[item_id]
            
        except Exception as e:
            self.view.show_warning(f"Error: {e}")
        
        
    def on_drop(self, event):
        paths = self.root.tk.splitlist(event.data)
        clean_paths = []
        
        for p in paths:
            if os.path.exists(p):
                clean_paths.append(p)
                
        self._add_files_and_folders(clean_paths)
        
    def _add_files_and_folders(self, path_list):
        
        #Normalizer paths
        normalized_lis = [os.path.abspath(p) for p in path_list]
        current_files_set = set(map(os.path.abspath, self.selected_files))
        
        #new_files = [f for f in path_list if f not in self.selected_files]
        new_files = [f for f in normalized_lis if f not in current_files_set]
        self.selected_files.extend(new_files)
           
        for file in new_files:
            name = os.path.basename(file)
            display_type = "[Folder]" if os.path.isdir(file) else "[File]"
            
            dis_text = f"{display_type} {name}"
            val_lis = ["✓", dis_text, "", "Pending"]
            
            if self.view and hasattr(self.view, 'tree'):
                item_id = self.view.tree.insert("","end",values=val_lis)
                self.item_to_file[item_id] = file
         
    
    def delete_selected_item(self):
        selected_items = self.view.tree.selection()
        
        if not selected_items:
            self.view.show_warning("No Item Selected to remove.")
            return
        
        for item_id in selected_items:
            file_path = self.item_to_file.get(item_id)

            if file_path and file_path in self.selected_files:
                self.selected_files.remove(file_path)
                
            if item_id in self.item_to_file:
                del self.item_to_file[item_id]
        
            self.view.tree.delete(item_id)
            
        
    def reset_fields(self):
        
        self.new_name.set("")     
        self.prefix.set("")
        self.suffix.set("")
        self.separator_var.set("none")
        self.custom_separator.set("")
        self.mode_var.set("none")
        self.suffix_mode.set("none")
        self.enumerated_prefix_var.set(False)
            
        
        
