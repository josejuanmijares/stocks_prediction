import datetime
import warnings
import spacy
import numpy as np
import pandas as pd
from spacytextblob.spacytextblob import SpacyTextBlob
from sentence_transformers import SentenceTransformer, util


# warnings.filterwarnings("ignore", message=r"\[W008\]", category=UserWarning)

nlp = spacy.load('en_core_web_lg')
nlp.add_pipe('spacytextblob')
STmodel = SentenceTransformer('src/all-MiniLM-L6-v2.mod')


def dates_diff(date0: str, date1: str):
    d0 = datetime.datetime.strptime(date0, "%Y-%m-%d")
    d1 = datetime.datetime.strptime(date1, "%Y-%m-%d")
    return (d1-d0).days


def check_sentiment_from_text(text: str):
    doc = nlp(text)
    return doc._.polarity


def check_topics_similarity_with_text(topics: list, text: str):

    text_embeddings = STmodel.encode(text, convert_to_tensor=True)
    topics_embeddings = STmodel.encode(topics, convert_to_tensor=True)

    cosine_score = util.cos_sim(text_embeddings, topics_embeddings)
    return {topic: score.item() for topic, score in zip(topics, cosine_score[0])}


def get_statistics(vector: list = None, categorical=False):
    o = {}
    if vector and not categorical:
        o['mean'] = np.mean(vector)
        o['median'] = np.median(vector)
        o['stdev'] = np.std(vector)
        o['min'] = np.min(vector)
        o['max'] = np.max(vector)
    elif vector and categorical:
        vector.sort()
        c = pd.Categorical(vector, ordered=True)
        o['mean'] = vector[int(np.mean(c.codes))]
        o['median'] = vector[int(np.median(c.codes))]
        o['stdev'] = np.std(c.codes)
        o['min'] = vector[int(np.min(c.codes))]
        o['max'] = vector[int(np.max(c.codes))]

    return o


def calculate_feature_distribution(features_timeseries_list: list = None):
    o = {}
    if features_timeseries_list:
        features_keys = features_timeseries_list[0].keys()
        for feature_key in features_keys:
            feature_vector = [sample[feature_key]
                              for sample in features_timeseries_list]
            if 'datetime' == feature_key:
                d0 = min(feature_vector)
                minutes_datetime_vector = [
                    (d1-d0).total_seconds()/60 for d1 in feature_vector]
                days_datetime_vector = [(d1-d0).days for d1 in feature_vector]

                o['minutes_datetime'] = get_statistics(minutes_datetime_vector)
                o['days_datetime'] = get_statistics(days_datetime_vector)

            elif 'category' == feature_key:
                o['category'] = get_statistics(
                    feature_vector, categorical=True)
            else:
                o[feature_key] = get_statistics(feature_vector)
    return o
