import unittest
import pandas as pd
from main import scrape_falabella

class TestScraping(unittest.TestCase):

    def test_scrape_returns_dataframe(self):
        url_base = 'https://www.falabella.com.co/falabella-co/category/cat1361001/Computadores-Portatiles'
        df = scrape_falabella(url_base, num_pages=10)
        self.assertIsInstance(df, pd.DataFrame)

    def test_dataframe_not_empty(self):
        url_base = 'https://www.falabella.com.co/falabella-co/category/cat1361001/Computadores-Portatiles'
        df = scrape_falabella(url_base, num_pages=10)
        self.assertTrue(len(df) > 0)