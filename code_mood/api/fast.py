from fastapi import FastAPI
from code_mood.api.spotify_api import *
from code_mood.ml_logic.preprocessor import *
from tensorflow import keras
from fastapi.templating import Jinja2Templates
templates = Jinja2Templates(directory="htmlDirectory")

app = FastAPI()
# $WIPE_BEGIN
# 💡 Preload the model to accelerate the predictions
# We want to avoid loading the heavy model at each `get("/predict")`
# The trick is to load the model in memory when the Uvicorn server starts
# and then store the model in an `app.state.model` global variable, accessible across all routes!
# This will prove very useful for the Demo Day
# load model from pickle file
#app.state.model = keras.models.load_model('/home/anais/code/anaisdangeot/mood_detector/notebooks/modelSVC_bestparams_saved.h5')
model_path = "/home/anais/code/anaisdangeot/mood_detector/notebooks/model_saved.h5"
app.state.model = pickle.load(open(model_path, 'rb'))
# $WIPE_END

@app.get("/predict")
def predict(
        track_name: str,  # 'viva forever'
    ):      # 1
    """
    Make a single course prediction.
    """
    # Step 2: Get spotify's track_id
    token =get_token()
    track_id = search_track(track_name,token)
    print('Get token, OK')

    # Step 3: Get spotify's features (non-text): analysis features and additional ones
    analysis_features = track_analysis_feat(track_id)
    print('Get analysis features, OK')
    additional_features = track_add_info(track_id)
    print('Get additional non text features, OK')
    dict_non_text = {**analysis_features,**additional_features}
    non_text = pd.DataFrame([dict_non_text])
    print('Transformed into Dataframe, OK')

    # Step 4: Get lyrics
    song_lyrics = request_lyrics(track_id)
    song_lyrics = [song_lyrics]

    # # Step 5: Preprocess and concatenate
    #text_features = clean_vectorize(song_lyrics)

    #non_text_features = pipeline(non_text)
    # X_combined = pd.concat([non_text_features, text_features], axis=1)

    # # Step 7: Return prediction (1 or 0)
    # model = app.state.model
    # y_predict = model.predict(X_combined)

    # ⚠️ fastapi only accepts simple Python data types as a return value
    # among them dict, list, str, int, float, bool
    # in order to be able to convert the api response to JSON

    return non_text
# #templates.TemplateResponse(
#         'df_representation.html',
#         {'data': non_text.to_html()}
#         )
    #dict(mood_prediction = y_predict)
    # $CHA_END

@app.get("/")
def root():
    # $CHA_BEGIN
    return dict(greeting="Hello")
    # $CHA_END
