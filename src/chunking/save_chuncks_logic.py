import csv
import os


def create_folder(dir: str):
    """
    function to create a directory
    @dir: can be specify to save into a directory
    """
    # set directory path
    folder_path = dir
    # creating the directory and verifying if it exists to avoid conflict
    os.makedirs(folder_path, exist_ok=True)


def save_chuncks(chuncks, dir: str = "data/chuncks"):
    """
    function that creates a dir, and store chuncks
    """
    # creating directory
    create_folder(dir)
    # csv file name
    csv_file_name = "chucks.csv"
    # directory to store the file
    csv_path = f"{dir}/{csv_file_name}"
    # validates if the csv file exists
    file_exists = os.path.exists(csv_path)
    # opening the csv file append mode
    with open(csv_path, "a", newline="") as f:
        writer = csv.writer(f)
        # validating if csv file is empty to add header csv file
        if not file_exists or os.stat(csv_path).st_size == 0:
            writer.writerow(["id", "content"])
        # writing the chuncks into csv rows
        for i, chunck in enumerate(chuncks):
            writer.writerow([i, chunck.pageContent])
