import os


def existsFile(file: str):
    return os.path.exists(file)


def createFolder(dir_path: str):
    """
    function to create a directory
    @dir: can be specify to save into a directory
    """
    # creating the directory and verifying if it exists to avoid conflict
    os.makedirs(dir_path, exist_ok=True)


def save_document(file_path: str, document: any):
    with open(file_path, "wb") as file:
        file.write(document)


def file_extension(filename: str):
    return os.path.splitext(filename)[1][1:].lower()


def generate_file_path(dir_path: str, filename: str):
    return os.path.join(dir_path, filename)
