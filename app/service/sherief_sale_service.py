import json
from datetime import datetime
from typing import IO, Tuple, Dict

from werkzeug.datastructures import FileStorage

from app.model.db.sherief_sale_child_table_alchemy import SherifSaleChild, SherifSalesChild
from app.model.db.sherief_sale_master_table_alchemy import SherifSales, SherifSale
from app.model.db.sherif_sale_properties_alchemy import Property, PropertySherifSale
from app.service.azure_blob import AzureBlobStorage, BlobType
# from app.service.queue_service import QueueService
from app.service.sherief_sale_ai_service import AzureCustomModel
from app.util.data_manipulation import DataManipulation
from app.util.date_util import DateUtil
from app.util.pdf_util import PdfUtil


class SheriffSaleService:

    @staticmethod
    def process_master_pdf(pdf_file: FileStorage, sale_date: str) -> tuple[dict[str, str], int]:
        file_name, sherif_sales = SheriffSaleService.process_file(pdf_file, sale_date)
        # Save the sherif sale to the database
        sherif_sales_id: int = SherifSale.save_sherif_sale_to_db(sherif_sales)
        print(f"sherif sale Master PDF saved to database with id: {sherif_sales_id}")

        # Split the PDF into individual pages
        pdf_files: list[FileStorage] = PdfUtil.split_pdf_pages(pdf_file)

        for pdf in pdf_files:
            file_name_child, sherif_sales = SheriffSaleService.process_file(pdf, sale_date)
            sherif_sales_child_model: SherifSalesChild = SherifSalesChild(
                file_hash=sherif_sales.file_hash, file_path=sherif_sales.file_path,
                file_name=sherif_sales.file_name, SHERIFF_SALE_DATE=sherif_sales.SHERIFF_SALE_DATE,
                SHERIEF_SALE_MASTER_ID=sherif_sales_id
            )
            child_id = SherifSaleChild.save_sherif_sale_to_db(sherif_sales_child_model)
            sherif_sales_child_model.id = child_id
            property_list: list[Property] = AzureCustomModel.extract_sherif_sale_details(
                sherif_sales_child_model.file_path, child_id)
            PropertySherifSale.save_all_sherif_sales_to_db(property_list)

        return {'message': 'File processed successfully'}, 200

    @staticmethod
    def process_file(pdf_file: FileStorage, sale_date: str) -> tuple[str, SherifSales]:
        """
        Processes a PDF file for a sheriff sale by performing the following steps:

        1. Appends a timestamp to the file name.
        2. Reads the file data as bytes.
        3. Computes a hash of the file data.
        4. Constructs a file path using the sale date and the new file name.
        5. Converts the sale date from a string to a datetime object.
        6. Retrieves the number of pages in the PDF file.
        7. Uploads the file to Azure Blob Storage.
        8. Creates a `SherifSales` object with the relevant information.

        Args:
            pdf_file (FileStorage): The PDF file to process, typically received from an HTTP request.
            sale_date (str): The date of the sheriff sale, formatted as a string (e.g., "YYYY-MM-DD").

        Returns:
            tuple: A tuple containing:
                - file_name (str): The name of the file with the timestamp prepended.
                - sherif_sales (SherifSales): An instance of the `SherifSales` class containing the
                  processed file's metadata.

        Raises:
            ValueError: If the sale_date cannot be converted to a valid datetime object.
            AzureBlobStorageException: If the file upload to Azure Blob Storage fails.
        """
        file_name: str = DateUtil.prepend_timestamp_to_filename(pdf_file.filename.lower())
        file_data: bytes | IO[bytes] = pdf_file.read()
        file_hash = DataManipulation.compute_hash(file_data)
        file_path = f'{sale_date}/{file_name}'
        sherif_sale_date: datetime = DateUtil.convert_string_to_date(sale_date)
        pdf_page_count = PdfUtil.get_pdf_page_count(pdf_file)

        # Upload the file to Azure Blob Storage
        AzureBlobStorage.upload_file(file_data, file_path, BlobType.SHERIF_SALE_BLOB)
        print(f"file uploaded to azure blob storage: {file_path}")

        sherif_sales: SherifSales = SherifSales(
            file_name=file_name,
            file_path=file_path,
            file_hash=file_hash,
            pages_size=pdf_page_count,
            SHERIFF_SALE_DATE=sherif_sale_date
        )

        return file_name, sherif_sales

    @staticmethod
    def enrich_sherif_sale():
        property_list: list['PropertySherifSale'] = PropertySherifSale.get_all_by_tract("1")
        print(f"property list: {property_list}")
        new_property_list: list[Property] = []
        for property in property_list:
            address = property.property_address.replace(" ", "-")
            zillow_link = f"https://www.zillow.com/homes/{address}_rb/"
            property.zillow_link = zillow_link
            new_property_list.append(property)
        PropertySherifSale.save_all_sherif_sales_to_db(new_property_list)

        return {"message": "enriched data successfully"}, 200