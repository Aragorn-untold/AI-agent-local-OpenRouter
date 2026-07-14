import os


def write_file(working_directory: str, file_path: str, content: str) -> str:
    path_to_file = os.path.join(working_directory, file_path)
    try:
        if type(file_path) is not str:
            return f"Error: File not found or is not a regular file: \"{file_path}\""
        if os.path.isdir(path_to_file):
            return f"Error: Cannot write to \"{file_path}\" as it is a directory"
        work_dir = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(work_dir, file_path))
        if os.path.commonpath([work_dir, target_dir]) != work_dir:
            return f"Error: Cannot write to \"{file_path}\" as it is outside the permitted working directory"
        
        os.makedirs(file_path, exist_ok=True)

        with open(path_to_file, mode="w") as file:
            file.write(content)
            
        return f"Successfully wrote to \"{file_path}\" ({len(content)} characters written)"
        
    except Exception as e:
        return f"Error: {e}"    



