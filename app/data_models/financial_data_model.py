import finnhub
from datetime import date, datetime


class BasicFinancialsMetrics:
    def __init__(self, metric_arg: dict = {}):
        self.metric = metric_arg
        self.today = date.today()

    def pre_process(self):
        # processing dates
        Ta = datetime.strptime(self.metric['52WeekHighDate'],
                               "%Y-%m-%d").date()
        Tb = datetime.strptime(self.metric['52WeekLowDate'],
                               "%Y-%m-%d").date()
        self.metric['52WeekHighDate'] = (self.today - Ta).days
        self.metric['52WeekLowDate'] = (self.today - Tb).days

        for key, value in self.metric.items():
            if value is None:
                self.metric['key'] = -1

        return self.metric


# class financial_data_model(basic_financials):
#     def __init__(self, company: str = 'TSLA'):
#         self.API_KEY = "c6vbpq2ad3i9k7i78ehg"
#         self.company = company
#         self.fc = finnhub.Client(api_key=self.API_KEY)

#     def get_basic_financials(self):
#         financials = self.fc.company_basic_financials(self.company, 'all')
