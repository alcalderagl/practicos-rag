import os
import json
import csv
import logging
from pathlib import Path
from src.commons.logging_messages import LOGG_MESSAGES
from src.commons.models.response_logic import ResponseLogic
from src.commons.enums.type_message import TypeMessage

logging.basicConfig(level=logging.INFO)


class FileManager:

    def __init__(self) -> None:
        pass

    def exists_file(self, file_path: str) -> bool:
        """
        Validates if the file exists into a directory

        Parameters
        ----------
        file_path : str
            Location of document folder

        Returns
        -------
        bool
            It exists ?
        """
        return os.path.exists(file_path)

    def create_folder(self, dir_path: str) -> None:
        """
        Create a local folder

        Parameters
        ----------
        dir_path : str
            The directory location to create a folder
        """
        os.makedirs(dir_path, exist_ok=True)

    def save_document(self, file_path: str, document: bytes) -> None:
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

    def save_json_file(self, dir_path: str, file_name: str, data: any) -> None:
        """
        Saves the given data as a JSON file in the specified directory.

        Parameters
        ----------
        dir_path : str
            The path of the directory where the JSON file will be saved.
            If the directory does not exist, it will be created.

        file_name : str
            The name of the JSON file to be created, including its extension (e.g., "file.json").

        data : any
            The data to be saved. This must be JSON-serializable.
        """
        # create folder
        self.create_folder(dir_path=dir_path)
        file_path: str = self.generate_file_path(dir_path=dir_path, file_name=file_name)
        # Save the data in a JSON file
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

    def save_csv_file(
        self, dir_path: str, file_name: str, data: list[any], headers: list[str] = []
    ) -> None:
        """
        Saves the given data as a CSV file in the specified directory.

        This function ensures the target directory exists, then creates a CSV file
        with the given name and writes the provided data to it. Optionally, headers
        can be included as the first row of the CSV file.

        Parameters
        ----------
        dir_path : str
            The path to the directory where the CSV file will be saved.
            If the directory does not exist, it will be created.
        file_name : str
            The name of the CSV file to be created, including the ".csv" extension.
        data : list[any]
            A list of data rows to be written to the CSV file. Each row should be
            a list or other iterable that matches the length of the headers, if provided.
        headers : list[str], optional
            A list of column headers to include as the first row in the CSV file.
            Defaults to an empty list, which means no headers will be included.
        """
        # # create folder
        self.create_folder(dir_path=dir_path)
        file_path: str = self.generate_file_path(dir_path=dir_path, file_name=file_name)
        # #self._exist_csv(file_path=file_path, headers=headers)
        # with open(file_path, "a", newline="", encoding="utf-8") as f:
        #     reader = csv.DictReader(f)
        #     reader = list(reader)
        #     if len(reader) > 0:
        #         writer = csv.DictWriter(f, fieldnames=headers)
        #         writer.writerows(data)
        #     else:
        #         writer = csv.DictWriter(f, fieldnames=headers)
        #         writer.writeheader()
        #         writer.writerows(data)
        # Check if the file already exists
        file_exists = os.path.isfile(file_path)

        # Open the file in append mode if it exists, or write mode if it doesn't
        with open(
            file_path, "a" if file_exists else "w", newline="", encoding="utf-8"
        ) as f:
            writer = csv.DictWriter(f, fieldnames=headers)

            # Write the header only if the file is being created
            if not file_exists:
                writer.writeheader()

            # Write the new rows
            writer.writerows(data)

    def read_csv(self, dir_path: str, file_name: str) -> list[any]:
        """
        Reads a CSV file from the specified directory and loads its content into a list of rows.

        Parameters
        ----------
        dir_path : str
            The path to the directory containing the CSV file.
        file_name : str
            The name of the CSV file to read, including the ".csv" extension.
        """

        items: list[str] = []
        file_path: str = self.generate_file_path(dir_path=dir_path, file_name=file_name)
        with open(file_path, "r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            items = list(reader)
        return items

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

    def get_file_name(self, file: str) -> str:
        """
        Gets file without extension

        Parameters
        ----------
        file : str
            The file name with its extension

        Returns
        -------
        str
            The file name
        """
        file_name = os.path.splitext(file)[0]
        return file_name

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
        self.create_folder(dir_path=dir_path)
        file_path: str = self.generate_file_path(dir_path=dir_path, file_name=file_name)
        # validate if file_path exists
        file_already_exist = self.exists_file(file_path=file_path)
        response_logic: ResponseLogic
        if file_already_exist:
            # if file already exists
            message = LOGG_MESSAGES["LOADER_FILE_ALREADY_EXIST"].format(
                file_name=file_name
            )
            response_logic = ResponseLogic(
                message=message, type_message=TypeMessage.WARNING, response=None
            )
        else:
            # other wise store the document
            self.save_document(file_path=file_path, document=document)
            response_logic = ResponseLogic(
                message=LOGG_MESSAGES["LOADER_STORE_FILE"],
                type_message=TypeMessage.INFO,
                response=file_path,
            )

        return response_logic
