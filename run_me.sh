pip install -U pip setuptools wheel
pip install -r requirements.txt
pip install git+https://github.com/JustAnotherArchivist/snscrape.git
pip install -U spacy
python -m spacy download en_core_web_sm
python -m spacy download en_core_web_lg