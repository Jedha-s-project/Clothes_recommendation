import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
from sentence_transformers import SentenceTransformer
import sklearn
from sklearn.metrics.pairwise import cosine_similarity

### Config
st.set_page_config(
    page_title="Don't look out: clothes denied",
    page_icon="⭐ ",
    layout="wide"
)

import base64
def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url(data:./{"png"};base64,{encoded_string.decode()});
        background-size: cover
    }}
    </style>
    """,
    unsafe_allow_html=True
    )
add_bg_from_local('background.png')   


photos = "https://github.com/Jedha-s-project/Clothes_recommendation/tree/main/Photos"

### App
st.title("Don't look out : clothes denied ! ⭐ ")

st.markdown("Good morning and welcome to you virtual closet")

model5 = SentenceTransformer("paraphrase-multilingual-mpnet-base-v2")

data = pd.read_excel("./Dataset/Clothes_table.xlsx")
data["cos_sim_list"] = ""

mood = st.text_input(label = "How are you doing today?")
X = model5.encode(mood).reshape(1, -1)

def clothes_reco (mood) :
  for i in range (len(data)) :
    Y = model5.encode(data.loc[i]["description"]).reshape(1, -1)
    cos_sim_mood = sklearn.metrics.pairwise.cosine_similarity(X,Y)
    data.loc[i]["cos_sim_list"] = cos_sim_mood
  clothes_reco_mood = str(data.sort_values(by=['cos_sim_list'], ascending=False).head(1)["id_clothes"].values[0])
  image = Image.open(F'./Photos/{clothes_reco_mood}.jpg')
  st.image(image, caption=clothes_reco_mood)
  st.markdown(F"your clothe recommendation is {clothes_reco_mood}")
  return clothes_reco_mood

if st.button('Find my clothe ! '):
     clothes_reco (mood)



#with open("flower.png", "rb") as file:
     #btn = st.download_button(
             #label="Download image",
             #data=file,
             #file_name="flower.png",
             #mime="image/png"
           #)

