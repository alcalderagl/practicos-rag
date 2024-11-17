import os


def existsFile(file_path: str):
    """
    Validates if the file exists into a directory

    Parameters
    ----------
    file_path : str
        Location of document folder

    Returns
    -------
    bool
        It exist ?
    """
    return os.path.exists(file_path)


def createFolder(dir_path: str):
    """
    Create a local folder

    Parameters
    ----------
    dir_path : str
        The directory location to create a folder
    """
    os.makedirs(dir_path, exist_ok=True)


def save_document(file_path: str, document: any):
    with open(file_path, "wb") as file:
        file.write(document)


def file_extension(filename: str):
    """
    Gets file extension by file name

    Parameters
    ----------
    filename : str
        The file name with its extension

    Returns
    -------
    str
        The file extension
    """
    return os.path.splitext(filename)[1][1:].lower()


def generate_file_path(dir_path: str, filename: str):
    """
    Build a path with directory path and file name

    Parameters
    ----------
    dir_path : str
        Directory path
    filename : str
        The file name with its extension

    Returns
    -------
    str
        the file extension
    """
    return os.path.join(dir_path, filename)
