from unittest import TestCase

from app.model.receipts_alchemy import Receipts


class TestReceipts(TestCase):



    def test_delete_by_file_path(self):
        Receipts.delete_by_file_path("test")
