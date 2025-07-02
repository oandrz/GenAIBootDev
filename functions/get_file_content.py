import os

from google.genai import types


def get_file_content(working_directory, file_path):
    abs_working_dir = os.path.abspath(working_directory)
    target_file = os.path.abspath(os.path.join(working_directory, file_path))
    if not target_file.startswith(abs_working_dir):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(target_file):
        return f'Error: "{file_path}" is not a file'
    try:
        with open(target_file, 'r') as file:
            content = file.read()
            if len(content) > 10000:
                content = content[:10000] + f'\n[...File "{file_path}" truncated at 10000 characters]'
            return content
    except Exception as e:
        return f"Error reading file: {e}"

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="retrieve file content from the specified file path, constrained to the working directory.",
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
        },
    ),
)
