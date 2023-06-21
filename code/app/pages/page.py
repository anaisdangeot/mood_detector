import streamlit as st
import requests
from PIL import Image
import matplotlib.pyplot as plt
from wordcloud import WordCloud,ImageColorGenerator
import sys,os
import numpy as np
import pandas as pd
import pickle
from spotify import get_token,search_track,track_add_info,track_analysis_feat,request_lyrics,cleaning,vectorize,pipeline
from streamlit_extras.switch_page_button import switch_page

def main():
    st.header("Search")
    search_term = st.text_input("What song is on your mind?")
    if st.button("Analyze ▶"):
        st.write("Analyze")
        token =get_token()
        st.write(token)
        track_id = search_track(search_term,token)
        st.write(track_id)
        print('✅ Get token')

        analysis_features = track_analysis_feat(track_id)

        additional_features = track_add_info(track_id)

        dict_non_text = {**analysis_features,**additional_features}

        non_text = pd.DataFrame([dict_non_text])
        st.write('✅ Transformed into Dataframe')

        song_lyrics = request_lyrics(track_id)
        song_lyrics = [song_lyrics]
        st.write('✅ Lyrics extracted')

        cleaned_lyrics = cleaning(song_lyrics[0])
        text_features = vectorize(song_lyrics[0])
        st.write('✅ Lyrics cleaned and vectorized')

        non_text_features = pipeline(non_text)
        text_features = pd.DataFrame(text_features)
        X_combined = pd.concat([non_text_features, text_features], axis=1)
        st.write('✅ Text and Non text features combined')

        model = pickle.load(open('models/modelSVC_bestparams_saved.h5', 'rb'))
        y_predict = model.predict(X_combined.values)
        y_predict = y_predict.tolist()
        st.write('✅ Prediction successfully made')
        st.write(y_predict[0])
        st.write(cleaned_lyrics)
        st.write(dict_non_text)


if __name__ == "__main__":
    main()
