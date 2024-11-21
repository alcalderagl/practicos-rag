import os
from pathlib import Path
from src.commons.logging_messages import LOGG_MESSAGES
from src.commons.models.response_logic import ResponseLogic
from src.commons.enums.type_message import TypeMessage


def existsFile(file_path: str) -> bool:
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


def createFolder(dir_path: str) -> str:
    """
    Create a local folder

    Parameters
    ----------
    dir_path : str
        The directory location to create a folder
    """
    os.makedirs(dir_path, exist_ok=True)


def save_document(file_path: str, document: bytes):
    """
    Write into the file path the binary document

    Parameters
    ----------
    dir_path : str
        The directory location to save the document

    document: bytes
        document binary
    """
    with open(file_path, "wb") as file:
        file.write(document)


def file_extension(filename: str) -> str:
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
    file = Path(filename)
    return file.suffix


def generate_file_path(dir_path: str, filename: str) -> str:
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


def upload_file(dir_path: str, document: bytes, filename: str) -> ResponseLogic:
    """
    Upload a document to an specify directory

    Parameters
    ----------
    dir_path : str
        Directory path
    document : bytes
        bynary document to store locally
    filename : str
        The file name with its extension

    Returns
    -------
    ResponseLogic
        An instance of ResponseLogic containing details about the upload operation.
    """
    # create folder
    createFolder(dir_path)
    file_path: str = generate_file_path(dir_path, filename)
    # validate if file_path exists
    file_already_exist = existsFile(file_path)
    response = None
    if file_already_exist:
        # if file already exists
        message = LOGG_MESSAGES["LOADER_FILE_ALREADY_EXIST"].format(filename=filename)
        response = ResponseLogic(
            message=message, typeMessage=TypeMessage.WARNING, response=None
        )
    else:
        # other wise store the document
        save_document(file_path, document)
        response = ResponseLogic(
            message=LOGG_MESSAGES["LOADER_STORE_FILE"],
            typeMessage=TypeMessage.INFO,
            response=file_path,
        )

    return response
