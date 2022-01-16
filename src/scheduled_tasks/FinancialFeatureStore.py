import finnhub
import datetime
from numpy.lib.arraysetops import isin
import pandas as pd
import numpy as np
from src.helpers.data_preprocessors import dates_diff, check_sentiment_from_text, check_topics_similarity_with_text, calculate_feature_distribution

API_KEY = "c6vbpq2ad3i9k7i78ehg"

TOPICS = ['political inestability', 'health safety', 'economic instability', 'technological innovation', 'costs reduction', 'new investments', 'expansion and market dominance', 'legal problems', 'media scandal', 'voting rights campaing', 'climate change global warming', 'Social work healthcare covid pandemic', 'refugee crisis migration', 'racial crisis discrimination injustice', 'income gap unfair', 'gun violence stress tensions unsafe', 'hunger food insecurity famine', 'gender inequality discrimination privilege', 'Change in interest rates, monitory or fiscal policies.', 'Major policy changes.', 'Major government changes.', 'Storms, Hurricanes, low rains (especially for agricultural catastrofies), heat waves, wild fires', 'Earnings and profits reports.', 'Launch of new product or features.', 'Changes in management.', 'Bagging of large contracts.', 'Financial scandals, court cases, patents', 'Big news about competitors', 'incentives, credits, exports, infrastructure, tax reduction', 'lack of raw materials', 'delays in shipping, supply chain problems', 'strikes, protests, tensions', 'raw materials price increase', 'services cost increased']


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

    def get_company_news_sentiment(self, company=None, _from: str = None, _to: str = None, recommended_freq='daily', sample_timestamp_rounding=True):
        '''
        This function collects company news, and it has acess to 1 year of historical data.
        '''
        today = datetime.date.today().strftime('%Y-%m-%d')
        yesterday = (datetime.date.today() -
                     datetime.timedelta(days=1)).strftime('%Y-%m-%d')

        raw_list_dict = self.fh_client.company_news(
            symbol=self.company if company is None else company,
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

    def get_company_news_features(self, company=None, _from: str = None, _to: str = None, recommended_freq='daily', sample_timestamp_rounding=True):
        '''
        This function collects company news, and it has acess to 1 year of historical data.
        '''
        today = datetime.date.today().strftime('%Y-%m-%d')
        yesterday = (datetime.date.today() -
                     datetime.timedelta(days=1)).strftime('%Y-%m-%d')

        raw_list_dict = self.fh_client.company_news(
            symbol=self.company if company is None else company,
            _from=_from if _from else yesterday,
            to=_to if _to else today
        )

        feature_data = []
        for raw_dict in raw_list_dict:
            datetime_sample = None
            if sample_timestamp_rounding:
                datetime_sample = pd.to_datetime(raw_dict['datetime'], unit="s")
                datetime_sample = datetime_sample.replace(minute=datetime_sample.minute - datetime_sample.minute % 5,
                                                          second=0, 
                                                          microsecond=0)
            else:
                datetime_sample = pd.to_datetime(raw_dict['datetime'], unit="s")

            features_dict = check_topics_similarity_with_text(topics=TOPICS, text=raw_dict['summary'])
            d = {'datetime': datetime_sample, "category": raw_dict['category']}
            d.update(features_dict)
            feature_data.append(d)

        return feature_data, recommended_freq

    def get_market_news(self, markets=['all'], recommended_freq='daily', sample_timestamp_rounding=True):
        '''
        This function collects company news, and it has acess to 1 year of historical data.
        '''

        raw_list_dict = []
        if ('all' in markets) or ('general' in markets):
            raw_list_dict.extend(self.fh_client.general_news('general'))
        if ('all' in markets) or ('forex' in markets):
            raw_list_dict.extend(self.fh_client.general_news('forex'))
        if ('all' in markets) or ('crypto' in markets):
            raw_list_dict.extend(self.fh_client.general_news('crypto'))
        if ('all' in markets) or ('merger' in markets):
            raw_list_dict.extend(self.fh_client.general_news('merger'))

        feature_data = []
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
            
            features_dict = check_topics_similarity_with_text(topics=TOPICS, text=raw_dict['summary'])
            d = {'datetime': datetime_sample, "category": raw_dict['category']}
            d.update(features_dict)
            feature_data.append(d)

        return feature_data, recommended_freq

    def get_company_peers_news(self, _from: str = None, _to: str = None, recommended_freq='daily', sample_timestamp_rounding=True):

        list_of_companies = self.fh_client.company_peers(self.company)

        group_features_data = []
        for peer_company in list_of_companies:
            peer_features_list, _ = self.get_company_news_features(peer_company, _from, _to)
            group_features_data.append(peer_features_list)
        
        return group_features_data, recommended_freq
    
    def transform_feature_data_to_statistics(self, feature_data, group_summary=False):
        statistics = None
        if isinstance(feature_data, list):
            if len(feature_data) > 0:
                if isinstance(feature_data[0], dict): 
                    statistics = [calculate_feature_distribution(feature_data)]
                elif isinstance(feature_data[0], list) and not group_summary: 
                    statistics = [calculate_feature_distribution(f) for f in feature_data]
                elif isinstance(feature_data[0], list) and group_summary: 
                    statistics = [calculate_feature_distribution([fi for f in feature_data for fi in f])]
        return statistics
