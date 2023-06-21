
import streamlit as st
import requests
from PIL import Image
import matplotlib.pyplot as plt
from wordcloud import WordCloud,ImageColorGenerator
import sys,os
import numpy as np
import pandas as pd
from spotify import get_token,search_track
from streamlit_extras.switch_page_button import switch_page

# Streamlit app
st.set_page_config(layout="wide")
image = Image.open('/home/shenazbhanja/code/anaisdangeot/mood_detector/code/app/logo.png')
def main():
    # Text of wordcloud
    #text_input = open("/home/shenazbhanja/code/anaisdangeot/mood_detector/code/app/It might seem crazy what I am 'bout.txt",mode="r",encoding='utf-8').read()


    # Create a container with a horizontal layout
    container = st.container()
    col1,mid1,col2=container.columns([2,3,2])
    #with col1:
       # image = st.image('/home/shenazbhanja/code/anaisdangeot/mood_detector/code/app/logo.png', width=180)
    with mid1:
        #title_container = container.empty()
        #st.markdown("<h2 style=> Muz Mood </h2>", unsafe_allow_html=True)
        #st.header("Ask a song and click the button to know your mood 😊")
        st.image(image)
       # st.header('Muz Mood')
        #st.markdown("<h2 style='text-align: center;'>Muz Mood</h2>", unsafe_allow_html=True)
        #st.header("Ask a song and click the button to know your mood 😊")

    # Set page title and description
    #st.title("🎵 Muz Mood 🎵")
        #st.write("Ask a song and click the button to know your mood 😊")

        button_text = "About", "Search", "Team"

        for text, col in zip(button_text, st.columns(len(button_text))):
            if col.button(text):
                new=text.lower()
                if new == "about":
                    display_about()
                elif new == "search":
                    st.write("Redirecting to the next page...")
                    switch_page("page")

                elif new == "team":
                    display_team()


        # Check if Button 2 is clicked
        #if button2:
                #st.write("Button 2 is clicked!")

    # Sidebar section
        #st.sidebar.header("Navigation")
        #page = st.sidebar.radio("Go to", ("About","Search", "Team"))

    #Page content based on selected option
    # if button_text == "About":
    #     display_about()
    # elif button_text == "Search":

    # elif button_text == "Team":
    #     display_team()

# Home page content
def display_about():
    st.title("°𝄞 Muz Mood °𝄞")
    st.write("""Welcome to Muz Mood, your ultimate destination for music tailored to your emotions.
                Whether you're feeling upbeat and energetic or calm and introspective, we have the
                perfect playlist to match your mood. Immerse yourself in the power of music.""")

def generate_wordcolud(text):
        positive_mask = np.array(Image.open("home/shenazbhanja/code/anaisdangeot/mood_detector/code/app/happy.png").convert("RGBA"))
        positive_mask[np.all(positive_mask == [255, 255, 255, 255], axis=2)] = [0, 0, 0, 0]

        wc = WordCloud(background_color="rgba(0, 0, 0, 0)", mask=positive_mask, height=1000, width=1000, max_words=200)
        wc.generate(text)

        plt.figure(figsize=(10, 10), facecolor="none")
        plt.imshow(wc, interpolation="bilinear")
        plt.axis("off")

        st.pyplot()
# About page content
def display_search():
    st.header("Search")
    search_term = st.text_input("What song is on your mind?")
    if st.button("Analyze ▶"):
        st.write("Analyze")
        # token =get_token()
        # st.write(token)
        # track_id = search_track(search_term,token)
        # st.write(track_id)
        # print('✅ Get token')



# Contact page content
def display_team():

    # Set page title and description
    st.title("Meet our awesome team! :D")

    names = "Anaïs Dangeot", "Mathieu Thiboudois", "Shenaz Bhanja"

    for text, col in zip(names, st.columns(len(names))):
        with col:
            if text == "Anaïs Dangeot":
                # First team member
                st.subheader("Anaïs Dangeot")
                st.image("/home/shenazbhanja/code/anaisdangeot/mood_detector/code/app/DSC_6113.JPG")
                linkedin_url="https://www.linkedin.com/in/ana%C3%AFs-dangeot-08864898/"
                st.markdown(f"[LinkedIn Profile]({linkedin_url})")

            elif text == "Mathieu Thiboudois":
                # Second team member
                st.subheader("Mathieu Thiboudois")
                st.image("https://ca.slack-edge.com/T02NE0241-U053V8HKUF3-b9431fa7981c-512")
                linkedin_url = "https://www.linkedin.com/in/mattwest-thiboudois-129709208/"
                st.markdown(f"[LinkedIn Profile]({linkedin_url})")

            elif text == "Shenaz Bhanja":
                # Third team member
                st.subheader("Shenaz Bhanja")
                linkedin_url = "https://mu.linkedin.com/in/shenaz17"

                # Create a clickable hyperlink to the LinkedIn profile
                st.markdown(f"[LinkedIn Profile]({linkedin_url})")





# Run the app
if __name__ == '__main__':
    main()
