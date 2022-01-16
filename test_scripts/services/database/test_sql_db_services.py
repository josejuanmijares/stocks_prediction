import unittest
import sqlite3
from src.services.database.sql_db_services import MyFlatTable
import warnings


class TestMyFlatTable(unittest.TestCase):
    def setUp(self, **kwargs):
        warnings.simplefilter('ignore', ResourceWarning)
        warnings.filterwarnings(
            "ignore", message=r"\[W008\]", category=UserWarning)
        self.obj = MyFlatTable('test_table.db')

    def test_MFT_int(self):
        """
        Test that it can initialize
        """
        self.assertTrue(isinstance(self.obj.conn, sqlite3.Connection))

    def test_MFT_connect(self):
        x = self.obj.connect()
        self.assertTrue(isinstance(x, sqlite3.Connection))
        x.close()

    def test_MFT_create_table_for_company(self):
        self.obj.create_table_for_company(
            company_name='AAP',
            fields=['field1', 'field2'])

        with self.obj.connect() as f:
            cur = f.cursor()
            cur.execute('select * from AAP')
            names = list(map(lambda x: x[0], cur.description))

            self.assertTrue(len(names) == 2)

    def test_MFT_delete_table_for_company(self):
        self.obj.create_table_for_company(
            company_name='AAP',
            fields=['field1', 'field2'])
        self.obj.delete_table_for_company(company_name='AAP')

        with self.obj.connect() as f:
            cur = f.cursor()
            res = cur.execute(
                '''SELECT count(*) FROM sqlite_master WHERE type="table" AND name="AAP";''')
            x = list(res)
            self.assertTrue(x[0][0] == 0)


if __name__ == '__main__':
    unittest.main()
