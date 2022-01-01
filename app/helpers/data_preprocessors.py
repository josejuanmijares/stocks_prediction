import datetime
import warnings
import spacy
from spacytextblob.spacytextblob import SpacyTextBlob

# warnings.filterwarnings("ignore", message=r"\[W008\]", category=UserWarning)

nlp = spacy.load('en_core_web_lg')
nlp.add_pipe('spacytextblob')


def dates_diff(date0: str, date1: str):
    d0 = datetime.datetime.strptime(date0, "%Y-%m-%d")
    d1 = datetime.datetime.strptime(date1, "%Y-%m-%d")
    return (d1-d0).days


def check_sentiment_from_text(text: str):
    doc = nlp(text)
    return doc._.polarity


def check_keywords_similarity_with_text(keywords: str, text: str):
    output = []
    doc = nlp(text)
    tokens = nlp(keywords)
    if doc:
        for token in tokens:
            output.append(doc.similarity(token))
    if len(output) == 0:
        output = [0]
    return output
