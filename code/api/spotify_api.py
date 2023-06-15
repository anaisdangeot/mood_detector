from dotenv import load_dotenv
import os
import base64
import requests
from requests import post
import json
import spotifysearch

load_dotenv()

client_id =os.getenv("CLIENT_ID")
client_secret =os.getenv("CLIENT_SECRET")

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

def get_auth_header(token):
    return {"Authorization":"Bearer" + token}

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

            print("Song name:", track_name)
            print("Artiste:", artist_name)
            print("Album:", album_name)
            print("ID:",track_id)

        else:
            print("Music not found:", query)
    else:
        print("error occurs while search")


token =get_token()
search_query = input("What's in your mind?")

search_track(search_query,token)
print (token)
