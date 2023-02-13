import nltk, os

# dirname = os.path.dirname(__file__)
# path = os.path.join(dirname, '/NLTK_DATA')
nltk.download(['stopwords', 'vader_lexicon'], download_dir='../NLTK_DATA')