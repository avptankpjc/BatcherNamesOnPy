

import os
import re

class BatcherModel:
    
    @staticmethod
    def rename_files(path_list, new_nameformat,
                     prefix,suffix,
                     separator,mode,
                     enumerated_prefix,
                     suffix_mode
                     ):
        rename_files = []
        global_prefix_counter = 1
        
             
        for index, item_path in enumerate(path_list):
            
            directory, old_name = os.path.split(item_path)
       
            is_folder = os.path.isdir(item_path)
            
            if is_folder:
                extension = ""
                base_name = old_name
            else:
                base_name, extension = os.path.splitext(old_name)
                
            
            new_name = BatcherModel.rename_advance(
                base_name, new_nameformat,
                prefix, suffix, separator,
                mode, enumerated_prefix,
                suffix_mode,global_prefix_counter
            )
            
            #Concat only is file
            new_name_full = new_name + extension
            new_path = os.path.join(directory, new_name_full)

            candidate = new_path
            counter = 1
            
            while os.path.exists(candidate):
                new_name_attemp = f"{new_name}_{counter:03d}" + extension
                candidate = os.path.join(directory, 
                                         new_name_attemp)
                counter += 1
            
            new_path = candidate
             
            try:
                
                os.rename(item_path, new_path)
                rename_files.append((item_path, new_path))
                
            except Exception as e:
                raise Exception(f"Could not rename {old_name}: {e}")

            global_prefix_counter += 1
            
        return rename_files
    
    
    @staticmethod
    def rename_advance(base_name, new_nameformat,
                       prefix, suffix,
                       separator, mode,
                       enumerated_prefix,
                       suffix_mode,
                       enumeration_number):
        
        if separator == "none" or separator not in base_name:
            parts = []
            
            if prefix:
                prex = f"{prefix}{enumeration_number:02d}" if enumerated_prefix else prefix
                parts.append(prex)
                            
            parts.append(new_nameformat if new_nameformat else base_name) 

            if suffix:
                parts.append(suffix)
                
            return "_".join(parts)
        
        
        if mode == "replace_after":
            
            prefix_part, remainder = base_name.split(separator, 1)
            m = re.match(r'^(.*)(' + re.escape(separator) + r'\d+)$', remainder)
            
            if m:
                core_part = m.group(1)
                orig_suffix = m.group(2)
                
            else:
                core_part = remainder
                orig_suffix = ""
                
            prex_n = f"{prefix}{enumeration_number:02d}" if prefix and enumerated_prefix else (prefix if prefix else prefix_part)
            new_prefix = (prex_n)
            
            new_core = new_nameformat if new_nameformat else core_part 
           
            if suffix:
                new_suffix = suffix if suffix.startswith(separator) else separator + suffix
            else:
                new_suffix = "" if suffix_mode == "delete" else orig_suffix
              
            return new_prefix + separator + new_core + new_suffix
        
                
        elif mode == "replace_before":
            parts = base_name.rsplit(separator, 1)
            
            if len(parts) == 2:
                left_part, right_part = parts
                orig_suffix = separator + right_part
                
            else:
                left_part = base_name
                orig_suffix = ""
            new_text = new_nameformat if new_nameformat else (
                f"{prefix}{enumeration_number:02d}" 
                if (prefix and enumerated_prefix) 
                else (prefix if prefix else left_part )
            )
            
            if suffix:
                new_suffix = suffix if suffix.startswith(separator) else separator + suffix
            else:
                new_suffix = "" if suffix_mode == "delete" else orig_suffix
                
            return new_text + new_suffix
        
        
        else:
            #Mode "None"
            parts = []
            if prefix:
                prex_e = f"{prefix}{enumeration_number:02d}" if enumerated_prefix else prefix
                parts.append(prex_e)
                         
            parts.append(new_nameformat if new_nameformat else base_name)
            
            if suffix:
                parts.append(suffix)
            return "_".join(parts)
        
        
        
            
            
            
            
            