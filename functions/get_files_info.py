import os

def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        if type(directory) is not str or not os.path.isdir(directory):
            return f"Error: \"{directory}\" is not a directory"
        work_dir = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(work_dir, directory))
        if os.path.commonpath([work_dir, target_dir]) != work_dir:
            return f"Error: Cannot list \"{directory}\" as it is outside the permitted working directory"
        return f"Success: \"{directory}\" is within the working directory"
    except Exception as e:
        return f"Error: {e}"    
    