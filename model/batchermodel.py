

import os
import re

class BatcherModel:
    
    @staticmethod
    def rename_files(file_list, 
                     new_nameformat,
                     prefix,
                     suffix,
                     separator,
                     mode,
                     enumerated_prefix,
                     suffix_mode
                     ):
        rename_files = []
        global_prefix_counter = 1
        
             
        for index, file_path in enumerate(file_list):
            
            directory, old_name = os.path.split(file_path)
            extension = os.path.splitext(old_name)[1]
            base_name = os.path.splitext(old_name)[0]
            
            new_name = BatcherModel.rename_advance(base_name, new_nameformat,
                                                   prefix, suffix, separator,
                                                   mode, enumerated_prefix,
                                                   suffix_mode, global_prefix_counter)
            
            
            new_path = os.path.join(directory, new_name)
            
            try:
                
            
                os.rename(file_path, new_path)
                rename_files.append(new_path)
                
            except Exception as e:
                raise Exception(f"Could not rename {old_name}: {e}")
            
        return rename_files
    
    
    @staticmethod
    def rename_advance(base_name, new_name,
                       prefix, suffix,
                       separator, mode,
                       enumerated_prefix,
                       suffix_mode,
                       enumeration_number):
        
        if separator == "none":
            separator = "_"
            
        if enumerated_prefix:
            new_name = f"{prefix}_{enumeration_number:02d}_{new_name}"
        
        else:
            new_name = f"{prefix}_{new_name}"
            
        
        if suffix_mode == "delete":
            new_name = f"{new_name}"     
        else:
            new_name = f"{new_name}_{suffix}"
            
            
        return new_name
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            