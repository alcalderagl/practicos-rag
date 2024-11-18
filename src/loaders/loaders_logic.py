from src.commons.logging_messages import LOGG_MESSAGES
from .pdf_loader_logic import PDFLoader
from src.commons.models.loaders.loader_response import FileModel, LoaderResponse
from src.commons.enums.type_message import TypeMessage
from src.commons.files_logic import file_extension


def file_loader(dir_path: str, file_name: str):
    """
    Load document into PDFLoader langchain library

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
    # get file extension and removes .
    file_ext = file_extension(dir_path)[1:]
    # pass directory path to disponible loader files
    loader_files = _loader_files()
    response = None
    if file_ext in loader_files:
        # if file_ext is allowed then
        try:
            # get file method respect to its file extension
            loader_response = loader_files[file_ext](dir_path)
            file_resp = FileModel(fileExt=file_ext, response=loader_response)
            message = LOGG_MESSAGES["LOADER_DOCUMENT_ADDED"].format(filename=file_name)
            response = LoaderResponse(
                message=message, response=file_resp, typeMessage=TypeMessage.INFO
            )
        except (ValueError, KeyError) as e:
            # catching the exception error
            message = LOGG_MESSAGES["LOADER_ERROR_LOADING"].format(error=e)
            response = LoaderResponse(
                message=message,
                typeMessage=TypeMessage.ERROR,
                response=FileModel(fileExt="", response=[]),
            )
    else:
        # unsopported file extension
        message = LOGG_MESSAGES["LOADER_UNKNOWN_FILE"].format(
            filename=file_name, ext=file_ext
        )
        response = LoaderResponse(
            message=message, typeMessage=TypeMessage.WARNING, response=None
        )

    return response


def _loader_files():
    # ['pdf', 'csv', 'xlsx', 'xls', 'docx', 'txt']
    documents = {"pdf": lambda dir_path: PDFLoader(dir_path)}
    return documents
