from unittest import TestCase

from app.service.sherief_sale_service import SheriffSaleService


class TestSheriffSaleService(TestCase):
    def test_enrich_zillow_data_web_scrapper(self):
        SheriffSaleService.enrich_zillow_data_web_scrapper()
        # self.fail()

    def test_enrich_amount_in_dispute_web_scrapper(self):
        SheriffSaleService.enrich_amount_in_dispute_web_scrapper()
