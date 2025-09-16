
from src.utility.nlp_dict.stop_words import stop_words

import os
import nltk
from nltk.stem import WordNetLemmatizer
# Set the NLTK data path to your project folder
NLTK_DATA_PATH = r"d:\dotnet\Acidaes.Agentic.MetaData\Acidaes_python_agent\nltk_data"
nltk.data.path.append(NLTK_DATA_PATH)

# Ensure wordnet is downloaded and available
try:
    from nltk.corpus import wordnet
    # Try accessing a file to trigger error if missing
    wordnet.ensure_loaded()
except Exception:
    nltk.download('wordnet', download_dir=NLTK_DATA_PATH)
    from nltk.corpus import wordnet

#from nltk.corpus import stopwords
class QueryNormalization:
    def __init__(self):
        pass

    # trim whitespace

    @staticmethod
    def throw_error_if_not_string(query: str) -> None:
        if not isinstance(query, str):
            raise ValueError("Input must be a string")

    @staticmethod
    def query_strip(query: str) -> str:
        return query.strip()

    # convert to lowercase

    @staticmethod
    def query_lowercase(query: str) -> str:
        return query.lower()

    @staticmethod
    def remove_stop_words(query: str) -> str:
        words = query.split()
        filtered_words = [word for word in words if word.lower() not in stop_words]
        return " ".join(filtered_words)
    
    @staticmethod
    def lemmatize_words(query: str) -> str:
        lemmatizer = WordNetLemmatizer()
        words = query.split()
        lemmatized_words = [lemmatizer.lemmatize(word) for word in words]
        return " ".join(lemmatized_words)

    @staticmethod
    def normalize_query(query: str) -> str:
        QueryNormalization.throw_error_if_not_string(query)

        q = QueryNormalization.query_strip(query)
        q = QueryNormalization.query_lowercase(q)
        q = QueryNormalization.remove_stop_words(q)
        q = QueryNormalization.lemmatize_words(q)
        # Example parsing logic (can be expanded as needed)
        # Add more parsing logic as needed
        return q
