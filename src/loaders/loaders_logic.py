from .pdf_loader_logic import PDFLoader
from src.commons.logging_messages import LOGG_MESSAGES
from src.commons.models.response_logic import ResponseLogic
from src.commons.enums.type_message import TypeMessage
from src.commons.files_logic import FileManager


class Loading:
    def __init__(self, dir_path: str, file_name: str) -> None:
        """
        Load document into a langchain LOADER document

        Parameters
        ----------
        dir_path : str
            Directory path
        file_name : str
            The file name with its extension
        """
        self.file_name = file_name
        self.dir_path = dir_path

    def file_loader(self) -> ResponseLogic:
        """
        Load document into a langchain LOADER document

        Returns
        -------
        ResponseLogic
            An instance of ResponseLogic containing details about the upload operation.
        """
        file_manager = FileManager()
        # get file extension and removes .
        file_ext = file_manager.file_extension(self.dir_path)[1:]
        # pass directory path to disponible loader files
        loader_files = self._loader_files()
        response_logic: ResponseLogic

        # if file_ext is into loader document method then
        if file_ext in loader_files:
            try:
                # get file method respect to its file extension
                loader_response = loader_files[file_ext](self.dir_path)
                # defining the log message output
                message = LOGG_MESSAGES["LOADER_DOCUMENT_ADDED"].format(
                    file_name=self.file_name
                )
                # return response
                response_logic = ResponseLogic(
                    response=loader_response,
                    type_message=TypeMessage.INFO,
                    message=message,
                )
            except (ValueError, KeyError) as e:
                # catching the exception error
                message = LOGG_MESSAGES["LOADER_ERROR_LOADING"].format(error=e)
                # return a default ResponseLogic
                response_logic = ResponseLogic(
                    message=message,
                    type_message=TypeMessage.ERROR,
                    response=None,
                )
        else:
            # unsopported file extension
            message = LOGG_MESSAGES["LOADER_UNKNOWN_FILE"].format(
                file_name=self.file_name, ext=file_ext
            )
            # return response
            response_logic = ResponseLogic(
                message=message, type_message=TypeMessage.WARNING, response=None
            )

        return response_logic

    def _loader_files(self):
        """
        Method that loads all the available langchain loaders with its own logic

        Returns
        -------
        dict[str, (dir_path: Any) -> list[LoaderModel]]
            a dict with extension and a method with its own logic.
        """
        # ['pdf', 'csv', 'xlsx', 'xls', 'docx', 'txt']
        documents = {"pdf": lambda dir_path: PDFLoader(dir_path)}
        return documents
