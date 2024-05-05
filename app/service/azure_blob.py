from typing import List, Dict, Union

from azure.storage.blob import BlobServiceClient, ContainerClient, StorageStreamDownloader
from flask import jsonify, Response

from app import app, Constants
from app.model.receipts_alchemy import Receipts


class AzureBlobStorage:
    blob_connection_string = app.config.get(Constants.BLOB_CONNECTION_STRING)
    blob_container_name = app.config.get(Constants.BLOB_CONTAINER_NAME)
    blob_service_client: BlobServiceClient = BlobServiceClient.from_connection_string(blob_connection_string)
    container_client: ContainerClient = blob_service_client.get_container_client(blob_container_name)

    @staticmethod
    def upload_file(data: bytes, blob_name: str) -> None:
        # with open(local_file_path, "rb") as data:
        AzureBlobStorage.container_client.upload_blob(name=blob_name, data=data)
        print(f"File '{blob_name}' uploaded to Azure Blob Storage.")

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

            error_msg= f"Failed to delete file '{blob_name}': {e}"
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
                        "type": "File" ,
                        "path": blob.name
                    }
                })

        return file_structure
