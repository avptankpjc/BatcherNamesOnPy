

import os
import re

class BatcherModel:
    
    @staticmethod
    def rename_files(path_list, new_nameformat,
                     prefix,suffix,
                     separator,mode,
                     enumerated_prefix,
                     suffix_mode,
                     offset_enabled=False,
                     offset_value=0,
                     offset_partial=False,
                     enum_offset=1,
                     enum_offset_enabled=False
                     ):
        
        rename_files = []
        
        global_prefix_counter = enum_offset if enumerated_prefix and enum_offset_enabled else 1
        
             
        for  item_path in path_list:
            
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
                suffix_mode, global_prefix_counter,
                offset_enabled=offset_enabled,
                offset_value=offset_value,
                offset_partial=offset_partial
            )
            
            #Concat only if it's a file
            new_name_full = new_name + extension
            new_path = os.path.join(directory, 
                                    new_name_full)

            #Avoid the Conflit with the new Name, if is the same at the current
            if os.path.normpath(item_path) == os.path.normpath(new_path):
                rename_files.append((item_path, new_path))
                global_prefix_counter += 1
                continue
            
            
            #Ensure no name conflicts
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
    def get_prefix(prefix, enumerated_prefix, enumeration_number):
        return f"{prefix}{enumeration_number:02d}" if prefix and enumerated_prefix else prefix
    
    @staticmethod
    def rename_advance(base_name, new_nameformat,
                       prefix, suffix,
                       separator, mode,
                       enumerated_prefix,
                       suffix_mode,
                       enumeration_number,
                       offset_enabled=False,
                       offset_value=0,
                       offset_partial=False
                       ):
        
        def clean_join(parts):
            return separator.join([p for p in parts if p.strip(separator)])
    
        #Offset Advance
        if offset_enabled and separator in base_name:
            parts = base_name.split(separator)
            offset = offset_value
            
            #Ensure the offset is within range
            if offset < 0 or offset >= len(parts): 
               return base_name

            if mode == "replace_before":
                 
                if offset_partial:
                    #Replace partial: only in position
                    parts[offset] = new_nameformat if new_nameformat is not None else parts[offset]
                else:
                    #Replace total: Since the position set
                    clean_name = new_nameformat.strip(separator) if new_nameformat else ""
                    parts = [clean_name] + parts[offset:]
                             
             
            
            elif mode == "replace_after":
                if offset_partial:
                    parts[offset] = new_nameformat if new_nameformat is not None else parts[offset]
                    
                else:
                    clean_name = new_nameformat.strip(separator) if new_nameformat else ""
                    parts = parts[:offset+1] + [clean_name]
                             
            else:
                if offset_partial:
                    parts[offset] = new_nameformat if new_nameformat is not None else parts[offset]
                    
                else:
                    clean_name = new_nameformat.strip(separator) if new_nameformat else ""
                    parts = parts[:offset] + [clean_name] + parts[offset+1:]

            
            new_name = clean_join(parts)
                
            #Add Prefix
            prex = BatcherModel.get_prefix(prefix, 
                                           enumerated_prefix,
                                           enumeration_number)
            
            if prex:
                new_name = prex + separator + new_name 
                
            #Add Suffix
            if suffix:
                new_name = new_name + (separator + suffix if not suffix.startswith(separator) else suffix)

            new_name = re.sub(rf"{re.escape(separator)}+", separator, new_name)
            
            return new_name
            
            
               
        #---------------------
        #------------ Mode Normal Without Offset -------------
        #---------------------
        
        if separator == "none" or separator not in base_name:
            parts = []
            
            if prefix:
                parts.append(BatcherModel.get_prefix(prefix, enumerated_prefix, enumeration_number))
                            
            parts.append(new_nameformat if new_nameformat else base_name) 

            if suffix:
                parts.append(suffix)
                
            return "_".join(parts)
        
        #Handle replace after mode
        if mode == "replace_after":
            
            prefix_part, remainder = base_name.split(separator, 1)
            m = re.match(r'^(.*)(' + re.escape(separator) + r'\d+)$', remainder)
            
            if m:
                core_part = m.group(1)
                orig_suffix = m.group(2)
                
            else:
                core_part = remainder
                orig_suffix = ""
                
         
            new_prefix = BatcherModel.get_prefix(prefix, enumerated_prefix, enumeration_number) if prefix else prefix_part
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
                
                
         
            #Modify the base name and apply the prefix/suffix
            new_text = new_nameformat if new_nameformat else left_part
            
            
            prex = BatcherModel.get_prefix(prefix, enumerated_prefix, enumeration_number)
            
            if prex:
                new_text = prex + separator + new_text
            
            
            if suffix:
                new_suffix = suffix if suffix.startswith(separator) else separator + suffix
            else:
                new_suffix = "" if suffix_mode == "delete" else orig_suffix
                
            return new_text + new_suffix
        
        
        else:
            #Mode "None"
            parts = []
            if prefix:
                parts.append(BatcherModel.get_prefix(prefix, enumerated_prefix, enumeration_number))
            parts.append(new_nameformat if new_nameformat else base_name)
            
            if suffix:
                parts.append(suffix)
            return "_".join(parts)
        
        
        
            
            
            
            
            