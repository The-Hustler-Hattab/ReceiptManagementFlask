from datetime import datetime
from typing import IO

from werkzeug.datastructures import FileStorage

from app.model.db.sherief_sale_master_table_alchemy import SherifSales, SherifSale
from app.service.azure_blob import AzureBlobStorage, BlobType
from app.util.data_manipulation import DataManipulation
from app.util.date_util import DateUtil
from app.util.pdf_util import PdfUtil


class SheriffSaleService:

    @staticmethod
    def process_master_pdf(pdf_file: FileStorage,sale_date: str) -> str:
        file_name: str = DateUtil.prepend_timestamp_to_filename(pdf_file.filename.lower())
        file_data: bytes | IO[bytes] = pdf_file.read()
        file_hash = DataManipulation.compute_hash(file_data)
        file_path=f'{sale_date}/{file_name}'
        sherif_sale_date: datetime = DateUtil.convert_string_to_date(sale_date)
        pdf_page_count = PdfUtil.get_pdf_page_count(file_data)
        # Upload the file to Azure Blob Storage
        AzureBlobStorage.upload_file(file_data, file_name, BlobType.SHERIF_SALE_BLOB)
        sherif_sales : SherifSales = SherifSales(file_name=file_name, file_path=file_path, file_hash=file_hash,
                                                 pages_size=pdf_page_count
                                                 ,sherif_sale_date=sherif_sale_date)
        # Save the sherif sale to the database
        SherifSale.save_sherif_sale_to_db(sherif_sales)

        return "Sherif Sale Master PDF processed successfully"


