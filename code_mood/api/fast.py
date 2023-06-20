from fastapi import FastAPI
from code_mood.api.spotify_api import *
from code_mood.ml_logic.preprocessor import *
import pickle

app = FastAPI()
# $WIPE_BEGIN
# 💡 Preload the model to accelerate the predictions
# We want to avoid loading the heavy model at each `get("/predict")`
# The trick is to load the model in memory when the Uvicorn server starts
# and then store the model in an `app.state.model` global variable, accessible across all routes!
# This will prove very useful for the Demo Day
# load model from pickle file
model_path = "/code_mood/ml_logic/model_pipeline/modelSVC_bestparams_saved.h5"
app.state.model = pickle.load(open(model_path, 'rb'))
# $WIPE_END

@app.get("/predict")
def predict(
        track_name: str,
    ):      # 1
    """
    Make a single course prediction.
    """
    # Step 1: Get spotify's track_id
    token =get_token()
    track_id = search_track(track_name,token)
    print('✅ Get token')

    # Step 2: Get spotify's features (non-text): analysis features and additional ones
    analysis_features = track_analysis_feat(track_id)
    print('✅ Get analysis features')
    additional_features = track_add_info(track_id)
    print('✅ Get additional non text features')
    dict_non_text = {**analysis_features,**additional_features}
    non_text = pd.DataFrame([dict_non_text])
    print('✅ Transformed into Dataframe')

    # Step 3: Get lyrics
    song_lyrics = request_lyrics(track_id)
    song_lyrics = [song_lyrics]
    print('✅ Lyrics extracted')

    # Step 4: Clean lyrics for word cloud ONLY
    cleaned_lyrics = cleaning(song_lyrics[0]) # created for API to return cleaned lyrics

    # Step 5: Preprocess and concatenate
    text_features = vectorize(song_lyrics[0]) # will be used to create combined features
    print('✅ Lyrics cleaned and vectorized')
    non_text_features = pipeline(non_text)
    print('✅ Non text features went through pipeline')
    text_features = pd.DataFrame(text_features)
    X_combined = pd.concat([non_text_features, text_features], axis=1)
    print(X_combined)
    print('✅ Text and Non text features combined')

    # Step 6: Return prediction (1 or 0)
    model = app.state.model
    print('✅ Model loaded successfully')
    y_predict = model.predict(X_combined.values)
    y_predict = y_predict.tolist()
    print('✅ Prediction successfully made')

    # ⚠️ fastapi only accepts simple Python data types as a return value
    # among them dict, list, str, int, float, bool
    # in order to be able to convert the api response to JSON

    return {'mood_prediction' : y_predict[0],
            'cleaned_lyrics' : cleaned_lyrics,
            'non_text_features': dict_non_text
            }
    # $CHA_END

@app.get("/")
def root():
    # $CHA_BEGIN
    return dict(greeting="Hello")
    # $CHA_END
