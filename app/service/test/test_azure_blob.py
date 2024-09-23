from unittest import TestCase

from app.service.azure_blob import AzureBlobStorage, BlobType


class TestAzureBlobStorage(TestCase):
    def test_upload_file(self):
        with open("static/2024-03-31-11-18-53_$26.04.pdf", "rb") as data:
            AzureBlobStorage.upload_file(data, "2023/10/2024-03-31-11-18-53_$26.04.pdf", BlobType.RECEIPT_BLOB)
            print("File uploaded successfully")

    def test_download_file(self):
        download_file_blob = AzureBlobStorage.download_file("2023/10/2024-03-31-11-18-53_$26.04.pdf",BlobType.RECEIPT_BLOB)
        with open("static/downloaded_file.pdf", "wb") as download_file:
            download_file.write(download_file_blob.readall())
            print("File downloaded successfully")

    def test_list_files(self):
        files = AzureBlobStorage.list_files()
        print(files)
