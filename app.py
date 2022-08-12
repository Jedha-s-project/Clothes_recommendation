import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image

### Config
st.set_page_config(
    page_title="Don't look out: clothes denied",
    page_icon="⭐ ",
    layout="wide"
)

photos = "https://github.com/Jedha-s-project/Clothes_recommendation/tree/main/Photos"

### App
st.title("Good morning!")

st.markdown("Welcome to you virtual closet")

st.text_input(label = "How are you doing today?")

data_load_state = st.text('Loading data...')

#with open("flower.png", "rb") as file:
     #btn = st.download_button(
             #label="Download image",
             #data=file,
             #file_name="flower.png",
             #mime="image/png"
           #)

