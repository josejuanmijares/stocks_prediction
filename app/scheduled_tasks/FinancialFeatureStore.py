import finnhub
import datetime
import pandas as pd
import numpy as np
from app.helpers.data_preprocessors import dates_diff, check_sentiment_from_text, check_keywords_similarity_with_text

API_KEY = "c6vbpq2ad3i9k7i78ehg"


class HighFrequencyFinancials:
    def __init__(self, company='AAP'):
        self.company = company
        self.fh_client = finnhub.Client(api_key=API_KEY)

    def get_fundamental_company_data(self, recommended_freq='daily'):
        '''
        This function collects daily fundamental information on a company, like  "ipo", "marketCapitalization", "shareOutstanding"

        There wont be historical data to retrive from previous days.
        '''

        raw_dict = self.fh_client.company_profile2(symbol=self.company)
        sampling_datetime = datetime.date.today()
        d0 = datetime.date.today().strftime('%Y-%m-%d')
        d1 = raw_dict.get('ipo', d0)

        temp_dict = {
            "time_to_ipo": dates_diff(d0, d1),
            "market_capitalization": raw_dict.get('marketCapitalization', -1),
            "shares_outstanding": raw_dict.get('shareOutstanding', -1),
        }

        return temp_dict, recommended_freq

    def get_company_news(self, _from: str = None, _to: str = None, recommended_freq='daily', sample_timestamp_rounding=True):
        '''
        This function collects company news, and it has acess to 1 year of historical data.
        '''
        today = datetime.date.today().strftime('%Y-%m-%d')
        yesterday = (datetime.date.today() -
                     datetime.timedelta(days=1)).strftime('%Y-%m-%d')

        raw_list_dict = self.fh_client.company_news(
            symbol=self.company,
            _from=_from if _from else yesterday,
            to=_to if _to else today
        )

        sentiment_data = []
        for raw_dict in raw_list_dict:
            datetime_sample = None
            if sample_timestamp_rounding:
                datetime_sample = pd.to_datetime(
                    raw_dict['datetime'], unit="s")
                datetime_sample = datetime_sample.replace(
                    minute=datetime_sample.minute - datetime_sample.minute % 5, second=0, microsecond=0)
            else:
                datetime_sample = pd.to_datetime(
                    raw_dict['datetime'], unit="s")
            d = {
                'datetime': datetime_sample,
                'company_news_sentiment': check_sentiment_from_text(raw_dict['headline'])
            }
            sentiment_data.append(d)

        return sentiment_data, recommended_freq

    def get_market_news(self, markets=['all'], recommended_freq='daily', sample_timestamp_rounding=True):
        '''
        This function collects company news, and it has acess to 1 year of historical data.
        '''
        raw_list_dict = self.fh_client.general_news('general')

        temp_news_vector = []
        for raw_dict in raw_list_dict:
            datetime_sample = None
            if sample_timestamp_rounding:
                datetime_sample = pd.to_datetime(
                    raw_dict['datetime'], unit="s")
                datetime_sample = datetime_sample.replace(
                    minute=datetime_sample.minute - datetime_sample.minute % 5, second=0, microsecond=0)
            else:
                datetime_sample = pd.to_datetime(
                    raw_dict['datetime'], unit="s")

            d = {
                "category": raw_dict['category'],
                "datetime": datetime_sample,
                "market_news_sentiment_political_instability": np.mean(check_keywords_similarity_with_text('political instability', raw_dict['summary'])),
                "market_news_sentiment_health_safety": np.mean(check_keywords_similarity_with_text('health safety', raw_dict['summary'])),
                "market_news_sentiment_economic_instability": np.mean(check_keywords_similarity_with_text('economic instability', raw_dict['summary'])),
                "market_news_sentiment_technological_innovation": np.mean(check_keywords_similarity_with_text('technological innovation', raw_dict['summary'])),
                "market_news_sentiment_voting_rights": np.mean(check_keywords_similarity_with_text('voting rights campaing', raw_dict['summary'])),
                "market_news_sentiment_climate_change": np.mean(check_keywords_similarity_with_text('climate change global warming', raw_dict['summary'])),
                "market_news_sentiment_covid": np.mean(check_keywords_similarity_with_text('Social work healthcare covid pandemic', raw_dict['summary'])),
                "market_news_sentiment_refugee_crisis": np.mean(check_keywords_similarity_with_text('refugee crisis migration', raw_dict['summary'])),
                "market_news_sentiment_racial_injustice": np.mean(check_keywords_similarity_with_text('racial crisis discrimination injustice', raw_dict['summary'])),
                "market_news_sentiment_income_gap": np.mean(check_keywords_similarity_with_text('income gap unfair', raw_dict['summary'])),
                "market_news_sentiment_gun_violence": np.mean(check_keywords_similarity_with_text('gun violence stress tensions unsafe', raw_dict['summary'])),
                "market_news_sentiment_hunger": np.mean(check_keywords_similarity_with_text('hunger food insecurity famine', raw_dict['summary'])),
                "market_news_sentiment_gender_inequality": np.mean(check_keywords_similarity_with_text('gender inequality discrimination privilege', raw_dict['summary']))
            }
            temp_news_vector.append(d)

        return temp_news_vector, recommended_freq
