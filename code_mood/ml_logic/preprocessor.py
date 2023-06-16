# GENERAL
import pandas as pd
import numpy as np

# Sklearn
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer, TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder
from sklearn.preprocessing import FunctionTransformer

# Language processing
import nltk
from langdetect import detect
import string
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import unicodedata
import re

''' The following lists has the column of our train dataset:
['Unnamed: 0.2', 'Unnamed: 0.1', 'Unnamed: 0', 'track_id', 'artists',
       'album_name', 'track_name', 'popularity', 'duration_ms', 'explicit',
       'danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness',
       'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo',
       'time_signature', 'track_genre', 'lyrics_extracted', 'lyrics_language'],

when calling Spotify's API we will get the following columns only:
- track_id
- popularity,
- duration_ms
- explicit
- danceability
- energy
- key
- mode
- speechiness
- instrumentalness
- liveness
- tempo
- time_signature
- valence

Whe will also get our lyrics and their language to complement our data:
- lyrics_extracted
- lyrics_language

'''

## TEXT FEATURE PREPROCESSING
#  Applying cleaning steps and vectorization
def clean_vectorize(sentence):
        #  Cleaning steps
    def cleaning():
        # Basic cleaning
        sentence = sentence.strip() ## remove whitespaces
        sentence = sentence.lower() ## lowercase
        sentence = ''.join(char for char in sentence if not char.isdigit()) ## remove numbers

        # Advanced cleaning
        for punctuation in string.punctuation:
            sentence = sentence.replace(punctuation, '') ## remove punctuation

        # function to remove accented characters
        def remove_accented_chars(txt):
            new_text = unicodedata.normalize('NFKD', txt).encode('ascii', 'ignore').decode('utf-8', 'ignore')
            return new_text
        sentence = remove_accented_chars(sentence)

        tokenized_sentence = nltk.word_tokenize(sentence) ## tokenize
        stop_words = set(stopwords.words('english')) ## define stopwords

        tokenized_sentence_cleaned = [ ## remove stopwords
            w for w in tokenized_sentence if not w in stop_words
        ]

        lemmatized = [
            WordNetLemmatizer().lemmatize(word, pos = "v")
            for word in tokenized_sentence_cleaned
        ]

        cleaned_sentence = ' '.join(word for word in lemmatized)

        return cleaned_sentence
    cleaned_text = cleaning()
    vectorizer = TfidfVectorizer(ngram_range=(1,2), max_df=0.35, max_features=300)
    text_vectors = vectorizer.fit_transform(cleaned_text(sentence)).toarray()

    print("✅ Text vectors of shape", text_vectors.shape)

    return text_vectors

## NON TEXT FEATURE PREPROCESSING
# Scale numerical values and one hot encode categorical vars:
def pipeline(X: pd.DataFrame) -> np.ndarray:

    num_transformer = Pipeline([('min_max_scaler', MinMaxScaler())
    ])

    cat_transformer = OneHotEncoder(handle_unknown='ignore')

    # Parallelize "num_transformer" and "cat_transfomer"
    preprocessor = ColumnTransformer([
        ('num_transformer', num_transformer, dtype_include=['int64','float64']),
        ('cat_transformer', cat_transformer, dtype_include=['bool','object'])
    ])

    X_transformed = preprocessor.fit_transform(X)
    print("✅ Non text array of shape", X_transformed.shape)

    return X_transformed

## COMBINING NON TEXT AND TEXT FEATURES
def combined_features(text: np.ndarray,
                      non_text:np.ndarray) -> np.ndarray:
    X_combined = pd.concat([non_text, text], axis=1)
    print("✅ X_combined_preprocessed, with shape", X_combined.shape)

    return X_combined

if
