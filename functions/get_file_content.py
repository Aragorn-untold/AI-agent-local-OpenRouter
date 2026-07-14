import os
from config import MAX_CHARS


def get_file_content(working_directory: str, file_path: str) -> str:
    path = os.path.join(working_directory, file_path)
    try:
        if type(file_path) is not str or not os.path.isfile(path):
            return f"Error: File not found or is not a regular file: \"{file_path}\""
        work_dir = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(work_dir, file_path))
        if os.path.commonpath([work_dir, target_dir]) != work_dir:
            return f"Error: Cannot read \"{file_path}\" as it is outside the permitted working directory"
        
        # file_content = open(file_path).read(MAX_CHARS)
        with open(path) as file:
            file_content = file.read(MAX_CHARS)
            if file.read(1):
                file_content += f"[...File \"{file_path}\" truncated at {MAX_CHARS} characters]"
        return file_content
    except Exception as e:
        return f"Error: {e}"

    