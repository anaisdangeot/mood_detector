import requests
from googletrans import Translator

base_url = 'https://spotify-lyric-api.herokuapp.com/'

params = {'trackid': '43BSpcCWtZKt6HUZujyY6O'}

response = requests.get(base_url, params=params).json()
song_det = response['lines']
lyrics = []

for i in range(len(song_det)):
    lyrics.append(song_det[i]['words'])
    test = (' '.join(lyrics))

trans = Translator()

# if trans.detect(test).lang != "en":
#     test = trans.translate(test, dest='en').text
print(trans.detect(test).lang)
