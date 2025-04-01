


import tkinter as tk
import os, re, sys
from tkinter import ttk, filedialog
from model.batchermodel import BatcherModel


class BatcherViewModel:
    
    def __init__(self, root):
        
        #self.file_list = []
        #self.new_nameformat = tk.StringVar()
        #self.status_message = tk.StringVar(value="Ready");
        self.root = root
        self.view = None
        
        self.selected_files = []
        
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
        
        
    def select_files(self):
        files = filedialog.askopenfilenames(
           title="Select Files",
           filetypes=(("All Files", "*.*"),
                      ("Text Files", "*.txt"))
        )
        
        if files:
            new_files = [f for f in files if f not in self.selected_files ]
            self.selected_files.extend(new_files)
            for file in new_files:
                org_name = os.path.basename(file)
                item_id = self.view.tree.insert("",
                                           "end", values=["✓", org_name, "", "Pending"] )
                self.item_to_file[item_id] = file
                
    
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
           
    def rename_advance(self, original, new_name_val, 
                       prefix_val, suffix_val,
                       enumerated_prefix,
                       enumeration_number
                       ):
        
        base, ext = os.path.splitext(original)
        sep = self.separator_var.get()
        
        if sep == "custom":
            sep = self.custom_separator.get()
            
        if sep == "none" or sep not in base:
            new_parts = []
            if prefix_val:
                new_parts.append(f"{prefix_val}{enumeration_number:02d}"
                                 if enumerated_prefix else prefix_val)
                
            new_parts.append(new_name_val if new_name_val else base)
            if suffix_val:
                new_parts.append(suffix_val)
                
            return "_".join(new_parts) + ext
        
        mode = self.mode_var.get()
        
        if mode == "replace_after":
            prefix_part, remainder = base.split(sep, 1)
            m = re.match(r'^(.*)(' + re.escape(sep) + r'\d+)$', remainder)

            if m:
                core_part = m.group(1)
                orig_suffix = m.group(2)
                
            else:
                core_part = remainder
                orig_suffix = ""
                
            new_prefix = (f"{prefix_val}{enumeration_number:02d}"
                          if prefix_val and enumerated_prefix 
                          else (prefix_val if prefix_val else prefix_part))
            
            new_core = new_name_val if new_name_val else core_part
            
            if suffix_val:
                new_suffix = suffix_val if suffix_val.startswith(sep) else sep + suffix_val 
            else:
                if self.suffix_mode.get() == "delete":
                    new_suffix = ""
                else:
                    new_suffix = orig_suffix
                    
            return new_prefix + sep + new_core + new_suffix + ext 
        
        elif mode == "replace_before":
            parts = base.rsplit(sep, 1)
            if len(parts) == 2:
                left_part, right_part = parts
                orig_suffix = sep + right_part
                
            else:
                left_part = base
                orig_suffix = ""
                
            new_text = new_name_val if new_name_val else (f"{prefix_val}{enumeration_number:02d}"
                                                          if prefix_val and enumerated_prefix else (prefix_val if prefix_val else left_part))
            
            if suffix_val:
                new_suffix = suffix_val if suffix_val.startswith(sep) else sep + suffix_val
            
            else:
                if self.suffix_mode.get() == "delete":
                    new_suffix = ""
                    
                else:
                    new_suffix = orig_suffix
                    
            return new_text + new_suffix + ext
        
        else:
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
            self.view.show_warning("Not File Selected !!!")
            return
        
        if not new_name_val and not prefix_val and not suffix_val:
            self.view.show_warning("You must enter a new name, prefix or suffix")
            return
        
        selected_items = [item_id for item_id in self.view.tree.get_children() if self.view.tree.item(item_id, "values")[0] == "✓"]
        
        if not selected_items:
            self.view.show_info("No Changes made because no file was selected. !!!")
            return
        
        new_files = []
        rename_items = []
        
        for item_id in selected_items:
            file_path = self.item_to_file.get(item_id)
            if not file_path:
                continue
            org_name = os.path.basename(file_path)
            dir_name = os.path.dirname(file_path)
            
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
                self.view.show_warning(f"Could not rename {org_name}: {e}")
                continue
            
            new_files.append(new_path)
            self.view.history_tree.insert("", "end", values=(org_name, update_name, "Renamed"))
            self.view.tree.item(item_id, values=["✓", org_name, update_name, "Renamed"])
            rename_items.append(item_id)
            if file_path in self.selected_files:
                self.selected_files.remove(file_path)
                
            del self.item_to_file[item_id]
            
        for item_id in rename_items:
            self.view.tree.delete(item_id)
            
        self.view.show_info("!! Files renamed successfully !!")
            
            
    def reset_fields(self):
        
        self.new_name.set("")     
        self.prefix.set("")
        self.suffix.set("")
        self.separator_var.set("none")
        self.custom_separator.set("")
        self.mode_var.set("none")
        self.suffix_mode.set("none")
        self.enumerated_prefix_var.set(False)
            
        
        
