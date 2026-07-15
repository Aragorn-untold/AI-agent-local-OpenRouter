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
        
        path_no_file = os.path.dirname(path_to_file) # A path without file at the end (only dirs)
        os.makedirs(path_no_file, exist_ok=True) # Creates directory if the final path is missing it

        with open(path_to_file, mode="w") as file:
            file.write(content)
            
        return f"Successfully wrote to \"{file_path}\" ({len(content)} characters written)"
        
    except Exception as e:
        return f"Error: {e}"    


schema_write_file = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "Writes text content to a specified file within the working directory (overwriting if the file exists)",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the file to write, relative to the working directory",
                },
                "content": {
                    "type": "string",
                    "description": "Text content to write to the file",
                },
            },
            "required": ["file_path", "content"],
        },
    },
}
