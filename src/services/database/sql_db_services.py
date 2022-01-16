import sqlite3
import pandas as pd


class MyFlatTable():
    def __init__(self, dbname='stocks.db'):
        self.dbname = dbname
        self.conn = sqlite3.connect('data/{}'.format(self.dbname))
        self.conn.close()

    def connect(self):
        self.conn = sqlite3.connect('data/{}'.format(self.dbname))
        return self.conn

    def create_table_for_company(self, company_name: str = None, fields: list = None):
        create_query_str = '''CREATE TABLE IF NOT EXISTS {table_name} {fields_names}'''.format(
            table_name=company_name, fields_names=tuple(fields))

        with self.connect() as f:
            cur = f.cursor()
            cur.execute(create_query_str)

    def delete_table_for_company(self, company_name: str = None):
        delete_query_str = '''DROP TABLE IF EXISTS {table_name}'''.format(
            table_name=company_name)

        with self.connect() as f:
            cur = f.cursor()
            cur.execute(delete_query_str)

    def read(self, query):
        df = pd.Dataframe({})
        if len(query):
            with self.connect() as f:
                df = pd.read_sql_query(query, f)
        return df

    def write_from_dataframe(self, df=None, table_name=None):
        if df and table_name:
            with self.connect() as f:
                cur = f.cursor()
                df.to_sql(table_name, f, if_exists='append', index=False)
