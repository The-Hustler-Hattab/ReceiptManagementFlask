import datetime
import traceback
from typing import IO, Dict, Tuple

from azure.ai.formrecognizer import DocumentAnalysisClient, CurrencyValue
from azure.core.credentials import AzureKeyCredential
from openai.lib import azure

from app import app, Constants
from app.model.db.receipts_alchemy import Receipt, Receipts
from app.service.azure_blob import AzureBlobStorage
from app.util.data_manipulation import DataManipulation

endpoint = app.config.get(Constants.AZURE_FORM_RECOGNIZER_ENDPOINT)
key = app.config.get(Constants.AZURE_FORM_RECOGNIZER_KEY)


class AzureFormRecognizer:

    @staticmethod
    def process_receipts(document_file: bytes | IO[bytes], company_name: str, customer_name: str, created_by: str,
                         spend_type:str) -> Tuple[Dict[str, str], int]:
        try:
            # anaylize pdf to process the receipt
            receipt: Receipt = AzureFormRecognizer.analyze_invoice(document_file)
            receipt.company_name = company_name
            receipt.customer_name = customer_name
            receipt.created_by = created_by
            receipt.spend_type = spend_type
            # upload the pdf to azure blob storage
            pdf_file_name = AzureFormRecognizer.construct_file_name(receipt)
            print(f"pdf file name: {pdf_file_name}")
            AzureBlobStorage.upload_file(document_file, pdf_file_name)
            receipt.file_path = pdf_file_name
            # save the receipt to the database
            Receipts.save_receipt_to_db(receipt)
            return {'message': 'PDF file received and processed successfully'}, 200
        except Exception as e:
            print(e)
            raise e
            # return {'message': f'An error occurred while processing the PDF file: {e}'}, 500

    @staticmethod
    def process_receipts_ai_assisted(document_file: bytes | IO[bytes]) -> Tuple[Dict[str, str], int]:
        try:
            # anaylize pdf to process the receipt
            receipt: Receipt = AzureFormRecognizer.analyze_invoice(document_file)
            return {'message': 'PDF file received and processed successfully',
                    'document_details': receipt.to_dict()}, 200
        except Exception as e:
            print(e)
            raise e
            # return {'message': f'An error occurred while processing the PDF file: {e}'}, 500

    @staticmethod
    def store_receipt_ai_assisted(document_file: bytes | IO[bytes],receipt: Receipt) -> Tuple[Dict[str, str], int]:
        try:
            # anaylize pdf to process the receipt
            pdf_file_name = AzureFormRecognizer.construct_file_name(receipt)
            print(f"pdf file name: {pdf_file_name}")
            AzureBlobStorage.upload_file(document_file, pdf_file_name)
            receipt.file_path = pdf_file_name
            # save the receipt to the database
            Receipts.save_receipt_to_db(receipt)
            return {'message': 'PDF file received and processed successfully'}, 200
        except Exception as e:
            print(e)
            traceback.print_exc()

            return {'message': f'An error occurred while processing the PDF file: {e}'}, 500

    @staticmethod
    def construct_file_name(receipt: Receipt) -> str:
        pdf_date = receipt.purchased_at.strftime("%Y_%m_%d-%H_%M_%S")
        pdf_year = receipt.purchased_at.strftime("%Y")
        pdf_month = receipt.purchased_at.strftime("%m")
        pdf_vendor = receipt.vendor.replace(" ", "_").strip()
        pdf_total_cost = f"${receipt.total}"
        return f"{pdf_year}/{pdf_vendor}/{pdf_month}/{pdf_date}-{pdf_total_cost}.pdf"

    @staticmethod
    def analyze_invoice(document_file: bytes | IO[bytes]) -> Receipt:
        receipt = Receipt.empty()
        receipt.created_at = datetime.datetime.now()
        receipt.sha256 = DataManipulation.compute_hash(document_file)
        document_analysis_client = DocumentAnalysisClient(
            endpoint=endpoint, credential=AzureKeyCredential(key)
        )

        poller = document_analysis_client.begin_analyze_document(
            "prebuilt-invoice", document_file
        )
        invoices = poller.result()
        for idx, invoice in enumerate(invoices.documents):
            print("--------Recognizing invoice #{}--------".format(idx + 1))
            vendor_name = invoice.fields.get("VendorName")
            if vendor_name:
                vendor_name = vendor_name.value.replace("\n","").replace("\t","")
                print(
                    "Vendor Name: {} ".format(
                        vendor_name
                    )
                )
                vendor_name= DataManipulation.convert_keywords(vendor_name, DataManipulation.mappings)
                receipt.vendor = str(vendor_name).replace("®","")
            vendor_address = invoice.fields.get("VendorAddress")
            if vendor_address:
                vendor_address = AzureFormRecognizer.get_address(vendor_address)
                print(f"Vendor Address: {vendor_address}")
                if vendor_address.startswith(", "):
                    vendor_address = vendor_address[2:]
                receipt.vendor_address = str(vendor_address)

            customer_name = invoice.fields.get("CustomerName")
            if customer_name:
                print(
                    "Customer Name: {} has confidence: {}".format(
                        customer_name.value, customer_name.confidence
                    )
                )

                receipt.customer_name = str(customer_name.value)

            invoice_id = invoice.fields.get("InvoiceId")
            if invoice_id:
                print(
                    "Invoice Id: {} has confidence: {}".format(
                        invoice_id.value, invoice_id.confidence
                    )
                )

                receipt.invoice_id = str(invoice_id.value)
            invoice_date = invoice.fields.get("InvoiceDate")
            if invoice_date:
                print(
                    "Invoice Date: {} has confidence: {}".format(
                        invoice_date.value, invoice_date.confidence
                    )
                )

                receipt.purchased_at = invoice_date.value
                print(f"Purchased At: {type(invoice_date.value)}")
            invoice_total = invoice.fields.get("InvoiceTotal")
            if invoice_total:
                print(
                    "Invoice Total: {} has confidence: {}, type {}".format(
                        invoice_total.value, invoice_total.confidence, type(invoice_total.value)
                    )
                )
                value: CurrencyValue = invoice_total.value
                receipt.total = float(value.amount)
            subtotal = invoice.fields.get("SubTotal")
            if subtotal:
                print(
                    "Subtotal: {} has confidence: {}".format(
                        subtotal.value, subtotal.confidence
                    )
                )

                receipt.sub_total = float(subtotal.value.amount)
            total_tax = invoice.fields.get("TotalTax")
            if total_tax:
                print(
                    "Total Tax: {} has confidence: {}".format(
                        total_tax.value, total_tax.confidence
                    )
                )

                receipt.tax = float(total_tax.value.amount)

            print("----------------------------------------")
            return receipt

    @staticmethod
    def get_address(address) -> str:
        vendor_address = ""
        if address.value.street_address:
            street_address = address.value.street_address
            vendor_address += street_address
        if address.value.city:
            city = address.value.city
            vendor_address += ", "
            vendor_address += city
        if address.value.state:
            state = address.value.state
            vendor_address += ", "
            vendor_address += state
        if address.value.postal_code:
            postal_code = address.value.postal_code
            vendor_address += ", "
            vendor_address += postal_code
        return vendor_address


