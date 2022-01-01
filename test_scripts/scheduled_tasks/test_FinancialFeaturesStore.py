import unittest
import finnhub
from app.scheduled_tasks.FinancialFeatureStore import HighFrequencyFinancials
import warnings


class TestFinancialFeaturesStore(unittest.TestCase):
    def setUp(self, **kwargs):
        warnings.simplefilter('ignore', ResourceWarning)
        warnings.filterwarnings(
            "ignore", message=r"\[W008\]", category=UserWarning)
        self.conn = HighFrequencyFinancials(company='AAP')

    def test_HFF_int(self):
        """
        Test that it can initialize
        """
        self.assertTrue(isinstance(self.conn.fh_client, finnhub.Client))

    def test_get_fundamental_company_data(self):

        raw_dict = {}
        raw_dict, _ = self.conn.get_fundamental_company_data()

        self.assertTrue(len(raw_dict) != 0)
        self.assertTrue("time_to_ipo" in raw_dict)

    def test_get_company_news(self):

        raw_list_dict = None
        raw_list_dict, _ = self.conn.get_company_news()
        self.assertTrue(isinstance(raw_list_dict, list))

    def test_get_market_news(self):

        raw_list_dict = []
        raw_list_dict, _ = self.conn.get_market_news()
        self.assertTrue(isinstance(raw_list_dict, list))


if __name__ == '__main__':
    unittest.main()
