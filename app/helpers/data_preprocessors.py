import datetime
import warnings
import spacy
from spacytextblob.spacytextblob import SpacyTextBlob
from sentence_transformers import SentenceTransformer, util


# warnings.filterwarnings("ignore", message=r"\[W008\]", category=UserWarning)

nlp = spacy.load('en_core_web_lg')
nlp.add_pipe('spacytextblob')
STmodel = SentenceTransformer('all-MiniLM-L6-v2.mod')


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


def calculate_feature_distribution(feature_vector, model='gaussian'):
    pass
