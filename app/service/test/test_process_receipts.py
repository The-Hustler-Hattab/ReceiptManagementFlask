import datetime
from unittest import TestCase

from app.model.db.receipts_alchemy import Receipt
from app.service.process_receipts import AzureFormRecognizer


class TestAzureFormRecognizer(TestCase):
    def test_analyze_invoice(self):
        with open("static/2024-03-31-11-18-53_$26.04.pdf", "rb") as data:
            receipts = AzureFormRecognizer.analyze_invoice(data)
            print(f"File analyzed successfully: {receipts} ")


    def test_construct_file_name(self):
        receipt = Receipt.empty()
        receipt.purchased_at = datetime.datetime.now()
        receipt.total= 26.04
        receipt.vendor = "Home Depot"
        file_name = AzureFormRecognizer.construct_file_name(receipt)
        print(f"File name constructed successfully: {file_name} ")