import os
import shutil
import urllib.request as request
import zipfile
from mlProject import logger
from mlProject.utils.common import get_size
from mlProject.entity.config_entity import DataIngestionConfig
from pathlib import Path



class DataIngestion:
    def __init__(self, config: DataIngestionConfig):
        self.config = config

    

    def download_file(self):
        source_path = Path(self.config.source_URL)
        local_file_path = Path(self.config.local_data_file)

        if source_path.exists():
            local_file_path.parent.mkdir(parents=True, exist_ok=True)
            if local_file_path.resolve() != source_path.resolve():
                shutil.copy2(source_path, local_file_path)
                logger.info(
                    f"Copied local source file from {source_path} to {local_file_path}"
                )
            else:
                logger.info(f"Local source file already exists at {local_file_path}")
            return

        if not os.path.exists(local_file_path):
            filename, headers = request.urlretrieve(
                url=self.config.source_URL,
                filename=self.config.local_data_file
            )
            logger.info(f"{filename} downloaded with following info: \n{headers}")
        else:
            logger.info(f"File already exists of size: {get_size(local_file_path)}")

        if local_file_path.suffix == ".zip" and not zipfile.is_zipfile(local_file_path):
            raise ValueError(
                f"Downloaded file is not a valid zip file: {self.config.local_data_file}"
            )

    def extract_zip_file(self):
        """
        Extracts the zip file into the data directory if the source is a zip.
        If the source is already a CSV file, no extraction is needed.
        """
        local_file_path = Path(self.config.local_data_file)
        unzip_path = Path(self.config.unzip_dir)
        os.makedirs(unzip_path, exist_ok=True)

        if local_file_path.suffix.lower() == ".zip":
            with zipfile.ZipFile(local_file_path, 'r') as zip_ref:
                zip_ref.extractall(unzip_path)
        else:
            logger.info(f"No extraction needed for non-zip file: {local_file_path}")