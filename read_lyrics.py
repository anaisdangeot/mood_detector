import pandas as pd
import requests
from google.cloud import bigquery
from colorama import Fore, Style
from googletrans import Translator

def request_lyrics(track_id):
    params = {'trackid': track_id}
    response = requests.get(base_url, params=params).json()
    trans = Translator()
    try:
        song_det = response['lines']
        lyrics = []
        for i in range(len(song_det)):
            lyrics.append(song_det[i]['words'])
            lyrics_clean= (' '.join(lyrics))
        if trans.detect(lyrics_clean).lang != "en":
            lyrics_clean = trans.translate(lyrics_clean, dest='en').text
        lyrics_language = trans.detect(lyrics_clean).lang
        return lyrics_clean, lyrics_language
    except:
        return '999', '999'

def clean_data(data):
    data['lyrics'] = data['track_id'].map(lambda x: request_lyrics(x)[0])
    data['lyrics_language'] = data['track_id'].map(lambda x: request_lyrics(x)[1])
    return data

def load_data_to_bq(data: pd.DataFrame,
              truncate: bool) -> None:
    """
    - Save dataframe to bigquery
    - Empty the table beforehands if `truncate` is True, append otherwise.
    """
    assert isinstance(data, pd.DataFrame)
    full_table_name = f"mood-detector-389611.dataset.dataset_with_lyrics"
    print(Fore.BLUE + f"\nSave data to bigquery {full_table_name}...:" + Style.RESET_ALL)

    # Load data to full_table_name
    # 🎯 Hint for "*** TypeError: expected bytes, int found":
    # BQ can only accept "str" columns starting with a letter or underscore column

    # $CHA_BEGIN
    # TODO: simplify this solution if possible, but student may very well choose another way to do it.
    # We don't test directly against their own BQ table, but only the result of their query.
    data.columns = [f"_{column}" if not str(column)[0].isalpha() and not str(column)[0] == "_"
                                                        else str(column) for column in data.columns]

    #print(data.columns)
    client = bigquery.Client()

    # define write mode and schema
    write_mode = "WRITE_TRUNCATE" if truncate else "WRITE_APPEND"
    #job_config = bigquery.LoadJobConfig(write_disposition=write_mode)
    job_config = bigquery.LoadJobConfig(

    schema = [
        bigquery.SchemaField(data.columns[0], "INTEGER"),
        bigquery.SchemaField(data.columns[1], "STRING"),
        bigquery.SchemaField(data.columns[2], "STRING"),
        bigquery.SchemaField(data.columns[3], "STRING"),
        bigquery.SchemaField(data.columns[4], "STRING"),
        bigquery.SchemaField(data.columns[5], "INTEGER"),
        bigquery.SchemaField(data.columns[6], "INTEGER"),
        bigquery.SchemaField(data.columns[7], "BOOL"),
        bigquery.SchemaField(data.columns[8], "FLOAT64"),
        bigquery.SchemaField(data.columns[9], "FLOAT64"),
        bigquery.SchemaField(data.columns[10], "INTEGER"),
        bigquery.SchemaField(data.columns[11], "FLOAT64"),
        bigquery.SchemaField(data.columns[12], "INTEGER"),
        bigquery.SchemaField(data.columns[13], "FLOAT64"),
        bigquery.SchemaField(data.columns[14], "FLOAT64"),
        bigquery.SchemaField(data.columns[15], "FLOAT64"),
        bigquery.SchemaField(data.columns[16], "FLOAT64"),
        bigquery.SchemaField(data.columns[17], "FLOAT64"),
        bigquery.SchemaField(data.columns[18], "FLOAT64"),
        bigquery.SchemaField(data.columns[19], "INTEGER"),
        bigquery.SchemaField(data.columns[20], "STRING"),
        bigquery.SchemaField(data.columns[21], "STRING"),
        bigquery.SchemaField(data.columns[22], "STRING")
    ],
    autodetect=False,
    source_format=bigquery.SourceFormat.CSV
    )

    #print(f"\n{'Write' if truncate else 'Append'} {full_table_name} ({data.shape[0]} rows)")

    # load data
    job = client.load_table_from_dataframe(data, full_table_name, job_config=job_config)
    result = job.result()  # wait for the job to complete

if __name__ == '__main__':
    data = pd.read_csv('raw_data/dataset.csv')
    base_url = 'https://spotify-lyric-api.herokuapp.com/'
    data = clean_data(data)
    load_data_to_bq(data, truncate=False)
