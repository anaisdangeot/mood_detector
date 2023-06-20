import os
import base64
import requests
from requests import post
import json
from googletrans import Translator


### SPOTIFY METRICS
'''
ANALYSIS FEATURES
https://api.spotify.com/v1/audio-features
- duration_ms
- danceability
- energy
- speechiness
- instrumentalness
- liveness
- tempo
- key
- mode
- time_signature

GET TRACK INFO
https://api.spotify.com/v1/tracks/
- explicit
- popularity
'''

client_id = os.environ.get("CLIENT_ID")
client_secret = os.environ.get("CLIENT_SECRET")


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

def get_auth_header():
    token_s = get_token()
    return {"Authorization":"Bearer" + token_s}

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


### GETTING SONG'S LYRICS
''' Code to get song's lyrics from spotify-lyric-api
'''
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
