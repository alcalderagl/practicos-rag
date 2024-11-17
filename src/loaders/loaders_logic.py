from src.commons.logging_messages import LOGG_MESSAGES
from .pdf_loader_logic import PDFLoader
from src.commons.models.response_logic import ResponseLogic
from src.commons.enums.type_message import TypeMessage
from src.commons.files_logic import (
    createFolder,
    existsFile,
    save_document,
    generate_file_path,
    file_extension,
)


def upload_document(dir_path: str, document: any, filename: str):
    createFolder(dir_path)
    file_path = generate_file_path(dir_path, filename)
    file_already_exist = existsFile(file_path)
    if file_already_exist:
        message = LOGG_MESSAGES["LOADER_FILE_ALREADY_EXIST"].format(filename=filename)
        response = ResponseLogic(
            message=message, typeMessage=TypeMessage.WARNING, response=[]
        )
        return response
    else:
        save_document(file_path, document)
        response = _load_document(filename, file_path)
        return response


def _load_document(filename: str, file_path: str):
    file_ext = file_extension(filename)
    documents = _document_loaders(file_path)
    if file_ext in documents:
        try:
            loader_response = documents[file_ext]
            result_loader = {"file_ext": file_ext, "response": loader_response}
            message = LOGG_MESSAGES["LOADER_DOCUMENT_ADDED"].format(filename=filename)
            response = ResponseLogic(
                message=message, response=result_loader, typeMessage=TypeMessage.INFO
            )
            return response
        except (ValueError, KeyError) as e:
            # catching the exception error
            message = LOGG_MESSAGES["LOADER_ERROR_LOADING"].format(error=e)
            response = ResponseLogic(
                message=message, typeMessage=TypeMessage.ERROR, response=[]
            )
            return response
    else:
        message = LOGG_MESSAGES["LOADER_UNKNOWN_FILE"].format(
            filename=filename, ext=file_ext
        )
        response = ResponseLogic(
            message=message, typeMessage=TypeMessage.WARNING, response=[]
        )
        return response


def _document_loaders(path):
    # ['pdf', 'csv', 'xlsx', 'xls', 'docx', 'txt']
    documents = {
        #'csv': lambda path: (),
        "pdf": PDFLoader(path)
        #'txt': lambda path: (),
    }
    return documents
