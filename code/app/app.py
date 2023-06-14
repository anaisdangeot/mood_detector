import streamlit as st
import requests
import os
from PIL import Image
left_aligned_logo = """
<style>
.logo-container {
    display: flex;
    align-items: center;
}

.logo {
    width: 50px;  /* Adjust the width of the logo */
    margin-right: 10px;  /* Add some right margin for spacing */
}
</style>"""
st.markdown(left_aligned_logo, unsafe_allow_html=True)
image = Image.open('notebooks/app/logo.png')
st.image(image, caption='logo', use_column_width=False)



st.title("Muz Mood")



search_bar = st.text_input("Enter a search term:")

search_button = st.button("Search")

if search_button:
    response = requests.get(
        "https://spotify-lyric-api.herokuapp.com/".format(search_bar)
    )
    results = response.json()["track_name"]
