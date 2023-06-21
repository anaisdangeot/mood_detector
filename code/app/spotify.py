import pickle
import base64
import json
from requests import post
import streamlit as st
from PIL import Image
import pickle
import requests
from requests import post
import pandas as pd
import string
import unicodedata
import nltk
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import numpy as np



model = pickle.load(open('/home/shenazbhanja/code/anaisdangeot/streamlit_mood/models/modelSVC_bestparams_saved.h5', 'rb'))

client_id="3669e068676c4da7b3a8108c136e285f"
client_secret="ffafcfb9df4645e78915c7bd3265d29f"

def get_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode('utf-8')
    auth_base64 = str(base64.b64encode(auth_bytes),"utf-8")

    url= "https://accounts.spotify.com/api/token"
    headers ={
    "Authorization": "Basic " + auth_base64,
    "Content-Type": "application/x-www-form-urlencoded"
}

    data ={"grant_type":"client_credentials"}
    result = post(url,headers=headers,data=data)
    json_result = json.loads(result.content)
    token =json_result["access_token"]
    return token

def search_track(query, token):
    url = "https://api.spotify.com/v1/search"
    headers = {
        "Authorization": "Bearer " + token
    }
    params = {
        "q": query,
        "type": "track",
        "total": 6
    }
    response = requests.get(url, headers=headers, params=params)
    json_response = json.loads(response.text)

    if "tracks" in json_response and "items" in json_response["tracks"]:
        tracks = json_response["tracks"]["items"]
        if len(tracks) > 0:
            track = tracks[0]
            track_id = track["id"]
            track_name = track["name"]
            artist_name = track["artists"][0]["name"]
            album_name = track["album"]["name"]

            return track_id
        else:
            print("Music not found:", query)
    else:
        print("error occurs while search")
def track_analysis_feat(track_id):
    url = "https://api.spotify.com/v1/audio-features"
    token = get_token()
    headers = {
        "Authorization": "Bearer " + token
        }
    params = {
        'ids': track_id
        }
    response = requests.get(url, headers=headers, params=params)
    json_response = json.loads(response.text)
    audio_feat = json_response['audio_features']

    # features to collect
    features_dict = {'danceability' : audio_feat[0]['danceability'],
                     'energy' : audio_feat[0]['energy'],
                     'key' : audio_feat[0]['key'],
                     'mode' : audio_feat[0]['mode'],
                     'speechiness' : audio_feat[0]['speechiness'],
                     'instrumentalness' : audio_feat[0]['instrumentalness'],
                     'liveness' : audio_feat[0]['liveness'],
                     'tempo' : audio_feat[0]['tempo'],
                     'time_signature': audio_feat[0]['time_signature'],
                     'duration_ms': audio_feat[0]['duration_ms']
    }

    return features_dict

def track_add_info(track_id):
    url = 'https://api.spotify.com/v1/tracks/'
    token = get_token()
    headers = {
        "Authorization": "Bearer " + token
        }
    params = {
        'ids': track_id
        }
    response = requests.get(url, headers=headers, params=params)
    json_response = json.loads(response.text)

    # features to collect
    feat_dict = {'popularity' : json_response['tracks'][0]['popularity'],
                 'explicit' : json_response['tracks'][0]['explicit']
    }
    return feat_dict

def request_lyrics(track_id):
    base_url = 'https://spotify-lyric-api.herokuapp.com/'
    params = {'trackid': track_id}
    response = requests.get(base_url, params=params).json()
    try:
        song_det = response['lines']
        lyrics = []
        for i in range(len(song_det)):
            lyrics.append(song_det[i]['words'])
            lyrics_extracted= (' '.join(lyrics))
        return lyrics_extracted
    except:
        return '999'

def cleaning(text):
    # Basic cleaning
    text = text.strip() ## remove whitespaces
    text = text.lower() ## lowercase
    text = ''.join(char for char in text if not char.isdigit()) ## remove numbers

    # Advanced cleaning
    for punctuation in string.punctuation:
        text = text.replace(punctuation, '') ## remove punctuation

    # function to remove accented characters
    def remove_accented_chars(txt):
        new_text = unicodedata.normalize('NFKD', txt).encode('ascii', 'ignore').decode('utf-8', 'ignore')
        return new_text
    text = remove_accented_chars(text)

    tokenized_sentence = nltk.word_tokenize(text) ## tokenize
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

def vectorize(sentence):
    cleaned_text = cleaning(sentence)
    vectorizer = pickle.load(open('models/vectorizer.pickle', 'rb'))
    text_vectors = vectorizer.transform([cleaned_text]).toarray()

    print("✅ Text vectors of shape", text_vectors.shape)

    return text_vectors

def pipeline(X: pd.DataFrame) -> np.ndarray:

    # num_transformer = Pipeline([('min_max_scaler', MinMaxScaler())
    # ])
    # cat_transformer = OneHotEncoder(handle_unknown='ignore')

    # # Parallelize "num_transformer" and "cat_transfomer"
    # preprocessor = ColumnTransformer(
    #     transformers=[
    #         ('num_transformer', num_transformer, ['int64', 'float64']),
    #         ('cat_transformer', cat_transformer, ['bool', 'object'])
    #     ]
    # )
    # use saved fitted preprocessor pipeline
    preprocessor = pickle.load(open('models/pipeline.pickle', 'rb'))

    X_transformed = pd.DataFrame(preprocessor.transform(X),columns=preprocessor.get_feature_names_out().astype(str))
    print("✅ Non text array of shape", X_transformed.shape)

    return X_transformed
