import os

from google.genai import types


def write_file(working_directory, file_path, content):
    abs_working_dir = os.path.abspath(working_directory)
    target_file = os.path.abspath(os.path.join(working_directory, file_path))
    if not target_file.startswith(abs_working_dir):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    try:
        with open(target_file, 'w') as file:
            file.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error: writing file: {e}"

schema_write_file_content = types.FunctionDeclaration(
    name="write_file",
    description="writes content to a file at the specified path, constrained to the working directory. If the file does not exist, it will be created.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file from which to retrieve content, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write to the file. If the file already exists, it will be overwritten.",
            ),
        },
    ),
)