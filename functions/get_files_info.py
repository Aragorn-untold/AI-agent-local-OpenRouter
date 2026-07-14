import os

def get_files_info(working_directory: str, directory: str = ".") -> str:
    if directory == ".":
        res_dir = "current"
    else:
        res_dir = f"\'{directory}\'"
    ret_str = f"Result for {res_dir} directory\n"    
    try:
        if type(directory) is not str: # or not os.path.isdir(directory):
            return ret_str + f"  Error: \"{directory}\" is not a directory"
        work_dir = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(work_dir, directory))
        if os.path.commonpath([work_dir, target_dir]) != work_dir:
            return ret_str + f"  Error: Cannot list \"{directory}\" as it is outside the permitted working directory"
        # return f"Success: \"{directory}\" is within the working directory"
        dir_con = os.listdir(target_dir)
        for file in dir_con:
            name = file
            file_size = os.path.getsize(os.path.join(target_dir, file))
            isdir_check = os.path.isdir(os.path.join(target_dir, file))
            ret_str += f"- {name}: file_size={file_size} bytes, is_dir={isdir_check}\n"
        return ret_str.strip("\n")
    except Exception as e:
        return ret_str + f"  Error: {e}"  
      
    