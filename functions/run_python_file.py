import os
import subprocess


def run_python_file(working_directory: str, file_path: str, args: list[str] | None = None) -> str:
    path_to_file = os.path.join(working_directory, file_path)
    try:
        if type(file_path) is not str:
            return f"Error: File not found or is not a regular file: \"{file_path}\""
        if not os.path.isfile(path_to_file):
            return f"Error: \"{file_path}\" does not exist or is not a regular file"
        if not file_path.endswith(".py"):
            return f"Error: \"{file_path}\" is not a Python file"       
        work_dir = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(work_dir, file_path))
        if os.path.commonpath([work_dir, target_dir]) != work_dir:
            return f"Error: Cannot execute \"{file_path}\" as it is outside the permitted working directory"       
        
        command = ["python", os.path.abspath(path_to_file)]
        if args != None:
            command.extend(args)
        
        sub_run = subprocess.run(command, capture_output=True, timeout=30, text=True)
        output_string = ""
        if sub_run.returncode != 0:
            output_string += f"Process exited with code {sub_run.returncode}\n"
        if sub_run.stdout == None and sub_run.stderr == None:
            output_string += "No output produced"
        else:
            output_string += f"STDOUT: {sub_run.stdout}"
            if sub_run.stderr:
                output_string += f"STDERR: {sub_run.stderr}"       
        return output_string
    except Exception as e:
        return f"Error: executing Python file {e}"
     