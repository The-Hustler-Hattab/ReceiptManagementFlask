from datetime import datetime
from typing import List, Dict, Union, Tuple

from azure.storage.blob import BlobServiceClient, ContainerClient, StorageStreamDownloader
from flask import jsonify, Response
from io import BytesIO
import zipfile

from app import app, Constants
from app.model.db.receipts_alchemy import Receipts
from app.util.data_manipulation import DataManipulation
from enum import Enum


class BlobType(Enum):
    SHERIF_SALE_BLOB = 'SHERIF_SALE_BLOB'
    RECEIPT_BLOB = 'RECEIPT_BLOB'


class AzureBlobStorage:
    blob_connection_string = app.config.get(Constants.BLOB_CONNECTION_STRING)
    blob_container_name = app.config.get(Constants.BLOB_CONTAINER_NAME)
    blob_service_client: BlobServiceClient = BlobServiceClient.from_connection_string(blob_connection_string)
    container_client: ContainerClient = blob_service_client.get_container_client(blob_container_name)

    @staticmethod
    def upload_file(data: bytes, blob_name: str, blob_type: BlobType) -> None:
        if blob_type == BlobType.SHERIF_SALE_BLOB:
            container_name = app.config.get(Constants.BLOB_CONTAINER_SHERIF_SALE)
            container_client: ContainerClient = AzureBlobStorage.blob_service_client.get_container_client(container_name)
            container_client.upload_blob(name=blob_name, data=data)
            print(f"File '{blob_name}' uploaded to Azure sherif Blob Storage.")
        else:
            AzureBlobStorage.container_client.upload_blob(name=blob_name, data=data)
            print(f"File '{blob_name}' uploaded to Azure receipt Blob Storage.")

    @staticmethod
    def download_file(blob_name: str) -> StorageStreamDownloader:
        # with open(local_file_path, "wb") as download_file:
        return AzureBlobStorage.container_client.download_blob(blob=blob_name)

    @staticmethod
    def delete_file(blob_name: str) -> tuple[Response, int]:
        try:
            AzureBlobStorage.container_client.delete_blob(blob=blob_name)
            Receipts.delete_by_file_path(blob_name)
            print(f"File '{blob_name}' deleted from Azure Blob Storage.")
            return jsonify({'message': f'File "{blob_name}" deleted successfully'}), 200
        except Exception as e:

            error_msg = f"Failed to delete file '{blob_name}': {e}"
            print(error_msg)
            return jsonify({'message': error_msg}), 500

    @staticmethod
    def list_files() -> List[Dict[str, Union[Dict[str, str], List[Dict[str, Dict[str, str]]]]]]:
        blob_list = AzureBlobStorage.container_client.list_blobs()
        file_structure = []

        for blob in blob_list:
            parts = blob.name.split('/')
            current_level = file_structure

            for part in parts[:-1]:
                found = False
                for item in current_level:
                    if item['data']['name'] == part:
                        current_level = item['children']
                        found = True
                        break

                if not found:
                    new_folder = {
                        "data": {
                            "name": part,
                            "type": "Folder"
                        },
                        "children": []
                    }
                    current_level.append(new_folder)
                    current_level = new_folder['children']

            if parts[-1]:
                current_level.append({
                    "data": {
                        "name": parts[-1],
                        "type": "File",
                        "path": blob.name
                    }
                })

        return file_structure

    @staticmethod
    def download_files_as_zip(files: List[str]) -> bytes:
        zip_buffer = BytesIO()

        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            for file_name in files:
                blob_stream_downloader = AzureBlobStorage.download_file(file_name)
                file_content = blob_stream_downloader.readall()
                zip_file.writestr(file_name, file_content)

        zip_buffer.seek(0)
        return zip_buffer.getvalue()

    @staticmethod
    def get_files_between_dates(start_date: datetime, end_date: datetime) -> bytes:
        files: list[str] = Receipts.fetch_between_files(start_date, end_date)
        print("Files: ", files)
        zip_file = AzureBlobStorage.download_files_as_zip(files)
        return zip_file

    @staticmethod
    def update_files_hash_in_table() -> tuple[Response, int]:
        receipts: list[Receipts] = Receipts.get_all()
        for receipt in receipts:
            file_path: str = receipt.file_path
            if file_path is not None or file_path != "":
                file: StorageStreamDownloader = AzureBlobStorage.download_file(file_path)
                file_hash = DataManipulation.compute_hash(file.readall())
                Receipts.update_hash(file_path, file_hash)

        return jsonify({'message': "Files hash updated successfully"}), 200
