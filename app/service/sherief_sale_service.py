import io
import json
from datetime import datetime
from io import BytesIO
from typing import IO, Tuple, Dict

from werkzeug.datastructures import FileStorage

from app.model.db.sherief_sale_child_table_alchemy import SherifSaleChild, SherifSalesChild
from app.model.db.sherief_sale_master_table_alchemy import SherifSales, SherifSale
from app.model.db.sherif_sale_properties_alchemy import Property, PropertySherifSale
from app.model.generic.sheriff_sale_detail_model import SheriffSaleDetailModel
from app.service.azure_blob import AzureBlobStorage, BlobType
from app.service.queue_service import QueueService
from app.service.sherief_sale_ai_service import AzureCustomModel
# from app.service.web_scraper import WebScrapper
# from app.service.selenium_web_scraper_service import ZillowScraper

from app.util.data_manipulation import DataManipulation
from app.util.date_util import DateUtil
from app.util.pdf_util import PdfUtil

import pandas as pd
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
            try:
                child_id = SherifSaleChild.save_sherif_sale_to_db(sherif_sales_child_model)
                sherif_sales_child_model.id = child_id
                # push the important details to the queue
                sherif_sales_details: SheriffSaleDetailModel = SheriffSaleDetailModel(file_path=sherif_sales.file_path,
                                                                                      sheriff_sale_child_id=child_id)
                try:
                    property_list: list[Property] = AzureCustomModel.extract_sherif_sale_details(sherif_sales_details)

                except Exception as e:
                    print(f"Error extracting sherif sale details: {e}")
                    if "Invalid request" in str(e):
                        continue
                    else:
                        raise e

                PropertySherifSale.save_all_sherif_sales_to_db(property_list)
                # QueueService.push_message(sherif_sales_details.to_json())
            except Exception as e:
                error_message = str(e)
                print(f"[+] Error while saving sherif sale child: {error_message}")
                if sherif_sales.file_hash in error_message:
                    print("[+] The exception contains the specific string, handling it accordingly.")
                    SherifSaleChild.update_sheriff_sale_date_by_file_hash(sherif_sales.file_hash,
                                                                          sherif_sales.SHERIFF_SALE_DATE)
                else:
                    print("[-] The exception does not contain the specific string, handling it differently.")
                    raise e

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
            if property.property_address is None:
                continue
            address = property.property_address.replace(" ", "-")
            zillow_link = f"https://www.zillow.com/homes/{address}_rb/"
            property.zillow_link = zillow_link
            new_property_list.append(property)
        PropertySherifSale.save_all_sherif_sales_to_db(new_property_list)

        return {"message": "enriched data successfully"}, 200

    # @staticmethod
    # def enrich_zillow_data():
    #     property_list: list['PropertySherifSale'] = PropertySherifSale.get_all_where_zillow_data_is_missing("1")
    #     print(f"property list: {property_list}")
    #     # new_property_list: list[Property] = []
    #     for property in property_list:
    #         zillow_model = ZillowScraper.get_zillow_property_data(property.zillow_link)
    #         property.add_zillow_data(zillow_model)
    #         PropertySherifSale.save_sherif_sale_to_db(property)
    #         # PropertySherifSale.save_all_sherif_sales_to_db(new_property_list)
    #
    #     return {"message": "enriched data successfully"}, 200

    # @staticmethod
    # def enrich_zillow_data_web_scrapper():
    #     property_list: list['PropertySherifSale'] = PropertySherifSale.get_all_where_zillow_data_is_missing("1",
    #                                                                                                         "Real Estate Sale - Mortgage Foreclosure")
    #     print(f"property list: {property_list}")
    #     for i, property in enumerate(property_list):
    #         # Handle the first item differently
    #         if i == 0:
    #             print("Handling the first property differently")
    #             # Custom logic for the first property
    #             WebScrapper.start_browser(property.zillow_link)
    #             zillow = WebScrapper.start_web_scraping_routine()
    #             property.add_zillow_data(zillow)
    #             # Maybe a different way to save the first property
    #             PropertySherifSale.save_sherif_sale_to_db(property)
    #         else:
    #             # Regular handling for the rest of the properties
    #             zillow_model = WebScrapper.continue_web_scraping_routine(property.zillow_link)
    #             property.add_zillow_data(zillow_model)
    #             PropertySherifSale.save_sherif_sale_to_db(property)
    #
    #     return {"message": "enriched data successfully"}, 200
    #
    # @staticmethod
    # def enrich_amount_in_dispute_web_scrapper():
    #     property_list: list['PropertySherifSale'] = PropertySherifSale.get_all_where_ammount_in_dispute_is_missing(
    #         "Real Estate Sale - Mortgage Foreclosure")
    #     print(f"property list: {property_list}")
    #     for property in property_list:
    #         if property.case_number is None or property.case_number == "":
    #             continue
    #         amount_in_dispute = WebScrapper.get_amount_in_dispute(property.case_number)
    #         property.amount_in_dispute = amount_in_dispute
    #         # Maybe a different way to save the first property
    #         PropertySherifSale.save_sherif_sale_to_db(property)
    #
    #     return {"message": "enriched data successfully"}, 200

    @staticmethod
    def get_sheriff_sale_data_between_two_dates(start_date: datetime, end_date: datetime) -> Tuple[Dict[str, str], int]:
        sheriff_sale_data: list = SherifSale.get_sherif_sales_between_dates(start_date, end_date)
        # Serialize each instance to a dictionary
        sherif_sales_list = [sherif_sale.to_dict() for sherif_sale in sheriff_sale_data]

        return {"message": "pulled data successfully", "sheriff_data": sherif_sales_list}, 200




    @staticmethod
    def export_properties_to_excel(sherif_sale_id: int) -> BytesIO:
        """
        Exports properties associated with the given SherifSale ID to an Excel file in memory,
        making the 'zillow_link' column clickable.

        :param sherif_sale_id: The ID of the SherifSale.
        :return: A BytesIO object containing the Excel file data.
        """
        try:
            # Get properties
            properties = SherifSale.get_properties_by_sherif_sale_id(sherif_sale_id)

            if not properties:
                print(f"No properties found for SherifSale ID {sherif_sale_id}")
                return BytesIO()  # Return an empty BytesIO object

            # Convert to list of dictionaries
            properties_list = [property.to_dict() for property in properties]

            # Create DataFrame
            df = pd.DataFrame(properties_list)

            # Create a BytesIO buffer
            output = BytesIO()

            # Use XlsxWriter as the engine
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                df.to_excel(writer, index=False, sheet_name='Properties')

                # Access the workbook and worksheet objects
                workbook = writer.book
                worksheet = writer.sheets['Properties']

                # Create a format for hyperlinks
                hyperlink_format = workbook.add_format({'font_color': 'blue', 'underline': True})

                # Get the column index of 'zillow_link'
                zillow_link_col_idx = df.columns.get_loc('zillow_link')

                # Iterate over the DataFrame rows and write hyperlinks
                for row_num, link in enumerate(df['zillow_link'], start=1):  # start=1 to skip header row
                    if pd.notnull(link):
                        # Write the hyperlink
                        worksheet.write_url(row_num, zillow_link_col_idx, link, hyperlink_format, string=link)
                    else:
                        # If no link, write an empty string or leave as is
                        worksheet.write(row_num, zillow_link_col_idx, '', workbook.add_format())

            # Seek to the beginning of the stream
            output.seek(0)

            print("Excel file has been created successfully in memory.")
            return output
        except Exception as e:
            print(f"[-] An error occurred: {e}")
            raise e