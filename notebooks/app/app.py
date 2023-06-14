import streamlit as st
import requests
from PIL import Image

st.set_page_config(layout="wide")

left_aligned_logo = """
<style>
.header-container {
        display: flex;
        align-items: center;
}

.logo-container {
    display: flex;
    align-items: center;
}

.logo {
    width: 100px;  /* Adjust the width of the logo */
    margin-right: 20px;  /* Add some right margin for spacing */
}

.sidebar .sidebar-content {
        background-color: #e6e6e6;  /* Specify your desired color here */
    }

.css-1aumxhk {
    width: 20%;
}
</style>"""

st.markdown(left_aligned_logo, unsafe_allow_html=True)
image = Image.open('notebooks/app/logo2.png')

if st.sidebar.button("Home"):
    st.text("""Welcome to Muz Mood, your ultimate destination for music tailored to your emotions.
                Whether you're feeling upbeat and energetic or calm and introspective, we have the
                perfect playlist to match your mood. Immerse yourself in the power of music.""")

if st.sidebar.button("Search"):
    search_term = st.text_input("What's in your mind?")

if st.sidebar.button("Library"):
    # Perform actions to show the user's playlist
    st.sidebar.write("User's Playlist:")

if st.sidebar.aria_expanded == "true":
    st.sidebar.image(image, width=240)
else:
    st.image(image, width=180)
