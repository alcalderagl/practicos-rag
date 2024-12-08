import os
from pathlib import Path
from src.commons.logging_messages import LOGG_MESSAGES
from src.commons.models.response_logic import ResponseLogic
from src.commons.enums.type_message import TypeMessage


class FileManager:

    def __init__(self):
        pass

    def existsFile(self, file_path: str) -> bool:
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

    def createFolder(self, dir_path: str) -> str:
        """
        Create a local folder

        Parameters
        ----------
        dir_path : str
            The directory location to create a folder
        """
        os.makedirs(dir_path, exist_ok=True)

    def save_document(self, file_path: str, document: bytes):
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

    def file_extension(self, file_name: str) -> str:
        """
        Gets file extension by file name

        Parameters
        ----------
        file_name : str
            The file name with its extension

        Returns
        -------
        str
            The file extension
        """
        file = Path(file_name)
        return file.suffix

    def generate_file_path(self, dir_path: str, file_name: str) -> str:
        """
        Build a path with directory path and file name

        Parameters
        ----------
        dir_path : str
            Directory path
        file_name : str
            The file name with its extension

        Returns
        -------
        str
            the file extension
        """
        return os.path.join(dir_path, file_name)

    def upload_file(self, document: bytes, file_name: str) -> ResponseLogic:
        """
        Upload a document to an specify directory

        Parameters
        ----------
        dir_path : str
            Directory path
        document : bytes
            bynary document to store locally
        file_name : str
            The file name with its extension

        Returns
        -------
        ResponseLogic
            An instance of ResponseLogic containing details about the upload operation.
        """
        # directory path
        dir_path: str = os.getenv("REGULATIONS_FOLDER", "data/regulations")
        # create folder
        self.createFolder(dir_path=dir_path)
        file_path: str = self.generate_file_path(dir_path=dir_path, file_name=file_name)
        # validate if file_path exists
        file_already_exist = self.existsFile(file_path=file_path)
        response = None
        if file_already_exist:
            # if file already exists
            message = LOGG_MESSAGES["LOADER_FILE_ALREADY_EXIST"].format(
                file_name=file_name
            )
            response = ResponseLogic(
                message=message, type_message=TypeMessage.WARNING, response=None
            )
        else:
            # other wise store the document
            self.save_document(file_path=file_path, document=document)
            response = ResponseLogic(
                message=LOGG_MESSAGES["LOADER_STORE_FILE"],
                type_message=TypeMessage.INFO,
                response=file_path,
            )

        return response
