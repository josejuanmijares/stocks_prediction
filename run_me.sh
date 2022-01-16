pip install -U pip setuptools wheel
conda install pytorch torchvision torchaudio -c pytorch
conda install -c huggingface transformers
pip install -r requirements.txt
pip install git+https://github.com/JustAnotherArchivist/snscrape.git
pip install -U spacy
python -m spacy download en_core_web_sm
python -m spacy download en_core_web_lg
python -c "from sentence_transformers import SentenceTransformer; model = SentenceTransformer('all-MiniLM-L6-v2'); model.save('src/all-MiniLM-L6-v2.mod');"