import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
from sentence_transformers import SentenceTransformer
import sklearn
from sklearn.metrics.pairwise import cosine_similarity
import base64
from pathlib import Path
import os


### Config
st.set_page_config(
    page_title="Don't look out: clothes denied",
    page_icon="🌟",
    layout="wide"
)

###Première page
def About():
    st.markdown("# About 🤓")
    st.title("Don't look out, clothing denial ! 🙈 ")
    st.subheader("Good morning and welcome to you virtual closet")
    st.markdown("You never know what to wear in the morning ? You end up going back to the same basic clothes? However, in the stores, you can't resist in front of this little dress or this umpteenth little top that suits you perfectly and that you already imagine wearing!  ")
    st.markdown("Our application offers you to choose your outfit for you ! It's very simple:")
    st.markdown("1.After each new purchase, enter the reason of your purchase: why do you like this article? In what circumstances do you think you will wear it?")
    st.markdown("2.Are you hesitating in front of your dressing room? Enter your mood of the day and our algorithm will make you a personalized recommendation !")
    st.markdown("Fantastic, right?")
    st.sidebar.markdown("# About 🤓")

###Deuxième page
def Virtual_closet():

    st.markdown("## 👩 🧔‍♂️ Virtual closet 👕 👗 👚 👔")
    st.sidebar.markdown("# Virtual closet")
    # Texte d'entrée
    st.subheader("How are you doing today ?⭐")
    col1, col2 = st.columns(2)
    with col1:
        mood = st.text_input(label = "Please, tell me how you feel !")

    # Algo de recommandation
    model5 = SentenceTransformer("paraphrase-multilingual-mpnet-base-v2")
    data = pd.read_excel("./Dataset/Clothes_table.xlsx")
    data["cos_sim_list"] = ""
    X = model5.encode(mood).reshape(1, -1)

    #dictionnaire
    dict_corr = {
      'debardeur': ['debardeur', 'pantalon', 'jupe'], 
      'tshirt' : ['tshirt', 'pantalon', 'short'], 
      'pull' : ['pull', 'pantalon', 'jupe'],
      #'veste' : ['veste', 'tshirt', 'pantalon'], 
      'gilet' : ['gilet', 'pantalon', 'robe'],
      'robe': ['robe', 'gilet'],
      'short': ['short', 'debardeur', 'tshirt'], 
      'blouse': ['blouse', 'pantalon'], 
      'jupe': ['jupe', 'debardeur', 'tshirt'], 
      'pantalon': ['pantalon', 'blouse', 'tshirt']
    }

    def clothes_reco (mood) :
      Y = model5.encode(data["description"])
      cos_sim_mood = cosine_similarity(X,Y)
      data["cos_sim_list"] = list(cos_sim_mood[0])


      clothes_reco_3 = data.sort_values(by=['cos_sim_list'], ascending=False).drop_duplicates(subset='category')[["id_clothes", "description", "category"]].reset_index(drop=True)
      clothes_reco_3 = clothes_reco_3[clothes_reco_3.category.isin(dict_corr[clothes_reco_3.loc[0]["category"]])].head(3).reset_index(drop=True) 

      for i in range (len(clothes_reco_3)) :
        product_name = str(clothes_reco_3.loc[i]['id_clothes'])
        st.markdown(F"Your cloth recommendation according to your mood is {product_name}")
        st.markdown(F"Clothe description : {clothes_reco_3.loc[i]['description']}")
        st.image(Image.open(F'./Photos/{product_name}.jpg'), width=250)
    
    if st.button('Find my cloth !'):
      clothes_reco (mood)

      like = st.radio(
      "Do you like this recommendation",
      ('Yes', 'No'))
      if like == 'Yes':
        st.write('Congratulations, you have your clothes for the day!')
      else:
        def clothes_reco_3_swipe (mood) :
          Y = model5.encode(data["description"])
          cos_sim_mood = cosine_similarity(X,Y)
          data["cos_sim_list"] = list(cos_sim_mood[0])
    
          clothes_reco_3_swipe = data.sort_values(by=['cos_sim_list'], ascending=False).groupby(by= 'category').head(2).drop_duplicates(subset = 'category', keep = 'last').reset_index(drop=True)
          clothes_reco_3_swipe = clothes_reco_3_swipe[clothes_reco_3_swipe.category.isin(dict_corr[clothes_reco_3_swipe.loc[0]["category"]])].head(3).reset_index(drop=True) 
      
          for i in range (len(clothes_reco_3_swipe)) :
            product_name = str(clothes_reco_3_swipe.loc[i]['id_clothes'])
            st.markdown(F"Your cloth recommendation according to your mood is {product_name}")
            st.markdown(F"Clothe description : {clothes_reco_3_swipe.loc[i]['description']}")
            st.image(Image.open(F'./Photos/{product_name}.jpg'), width=250)
    
      if st.button('Swipe 👈'):
        clothes_reco_3_swipe (mood)
 
    #Swipe reco

    st.markdown('If you do not like the recommendation, feel free to swipe!')
    
    



###Troisième page


def Update_virtual_closet():
  st.markdown("# Update virtual closet 🔧")
  st.sidebar.markdown("# Update virtual closet ")
  data_page_3 = pd.read_excel("./Dataset/Clothes_table.xlsx")

  ## Explore the virtual closet
  st.subheader("Explore your virtual closet")
  category_to_display = st.selectbox("Select a clothing category you want to see", data_page_3["category"].sort_values().unique())
  #nouvelle_liste = [x for x in data_page_3["id_clothes"] if data_page_3.loc[x]['category'] == category_to_display]
  #st.image(Image.open(F"{nouvelle_liste}".png), width=500)
    

  ## Add a new item
  st.subheader("Add a new item")
  col1, col2 = st.columns(2)
  
  ## To upload a picture
  i = 10
  with col1:
    uploaded_file = st.file_uploader("Upload a picture")
    
    if uploaded_file is not None :
      item_category = st.selectbox("Select the item category", data_page_3["category"].sort_values().unique())
      item_description = st.text_input(label = "Why did you buy this clothing? In what circumstances do you imagine yourself wearing it?")
      file_details = {uploaded_file.name : F"{item_category}_{i}.jpg", uploaded_file.type : "jpg"}
      st.write(file_details)
      img = Image.open(uploaded_file)
      st.image(img, width=500)
      st.markdown("**The item is sucessfully Uploaded.**")

      download_picture = st.button("Save your item")
      if download_picture :
        with open(".\Photos", "wb") as f:
          f.write(uploaded_file.getbuffer())
          st.success(f'File {F"{item_category}{i}.jpg"} is successfully saved!')
          i += 1  

        

  ### To take a picture
  with col2:
    camera_input = st.camera_input("Take a picture")
    if camera_input is not None:
    # To read image file buffer as bytes:
      picture = camera_input.getvalue()
    # Check the type of bytes_data:
    # Should output: <class 'bytes'>
      st.write(type(picture))
      item_category = st.selectbox("Select the item category", data_page_3["category"].sort_values().unique())
      item_description = st.text_input(label = "Why did you buy this clothing? In what circumstances do you imagine yourself wearing it?")
      download_picture_camera = st.button("Save your item")
      if download_picture_camera :
        with open(".\Photos", "wb") as f:
          f.write(picture.getbuffer())
          st.success(f'File {F"{item_category}{i}.jpg"} is successfully saved!')
          i += 1 


page_names_to_funcs = {
    "About": About,
    "Virtual closet": Virtual_closet,
    "Update virtual closet": Update_virtual_closet,
}

selected_page = st.sidebar.selectbox("Select a page", page_names_to_funcs.keys())
page_names_to_funcs[selected_page]()


### Background
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


### App

#def clothes_reco (mood) :
  #for i in range (len(data)) :
   #Y = model5.encode(data.loc[i]["description"]).reshape(1, -1)
    #cos_sim_mood = cosine_similarity(X,Y)
    #data.loc[i]["cos_sim_list"] = cos_sim_mood
  #clothes_reco_mood = str(data.sort_values(by=['cos_sim_list'], ascending=False).head(1)["id_clothes"].values[0])
  #clothes_description = str(data.sort_values(by=['cos_sim_list'], ascending=False).head(1)["description"].values[0])
  #image = Image.open(F'./Photos/{clothes_reco_mood}.jpg')
  #st.image(image, caption=clothes_reco_mood)
  #st.markdown(F"Your clothe recommendation is {clothes_reco_mood}")
  #st.markdown(F"Clothe description : {clothes_description}")
  #return clothes_reco_mood







