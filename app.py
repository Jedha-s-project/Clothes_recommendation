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
import itertools
import time


### Config
st.set_page_config(
    page_title="Don't look out: clothes denied",
    page_icon="🌟",
    layout="wide"
)

def check_password():
    """Returns `True` if the user had the correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if st.session_state["password"] == st.secrets["password"]:
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # don't store password
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # First run, show input for password.
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        return False
    elif not st.session_state["password_correct"]:
        # Password not correct, show input + error.
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        st.error("😕 Password incorrect")
        return False
    else:
        # Password correct.
        return True

if check_password():
    ###Première page
    def About():
        st.markdown("# About 🤓")
        st.title("Don't look out, clothing denial ! 🙈 ")
        st.subheader("Good morning and welcome to you virtual closet")
        st.markdown("You never know what to wear in the morning ? You end up going back to the same basic clothes? However, in the stores, you can't resist in front of this little dress or this umpteenth little top that suits you perfectly and that you already imagine wearing!  ")
        st.markdown("Our application offers you to choose your outfit for you ! It's very simple:")
        st.markdown("**1.After each new purchase, enter the reason of your purchase: why do you like this article? In what circumstances do you think you will wear it?**")
        st.markdown("**2.Are you hesitating in front of your dressing room? Enter your mood of the day and our algorithm will make you a personalized recommendation !**")
        st.markdown("Fantastic, right?")
        st.sidebar.markdown("# About 🤓")

    ###Deuxième page
    
    def Virtual_closet():

        if 'button_clicked' not in st.session_state :
          st.session_state.button_clicked = False
    
        def callback() :
          st.session_state.button_clicked = True

        #dictionnaire
        dict_corr = {
          'debardeur': ['debardeur', 'pantalon', 'jupe'], 
          'tshirt' : ['tshirt', 'pantalon', 'short'], 
          'pull' : ['pull', 'pantalon', 'jupe'],
          'veste' : ['veste', 'tshirt', 'pantalon'], 
          'gilet' : ['gilet', 'pantalon', 'robe'],
          'robe': ['robe', 'gilet', 'veste'],
          'short': ['short', 'debardeur', 'tshirt'], 
          'blouse': ['blouse', 'pantalon', 'jupe'], 
          'jupe': ['jupe', 'debardeur', 'tshirt'], 
          'pantalon': ['pantalon', 'blouse', 'tshirt']
          }

        def paginator(label, items, items_per_page=3, on_sidebar=True):
          # Figure out where to display the paginator
          if on_sidebar:
            location = st.sidebar.empty()
          else:
            location = st.empty()

        # Display a pagination selectbox in the specified location.
          items = list(items)
          n_pages = len(items)
          n_pages = (len(items) - 1) // items_per_page + 1
          page_format_func = lambda i: "Page %s" % i
          page_number = location.selectbox(label, range(n_pages), format_func=page_format_func)

        # Iterate over the items in the page to let the user display them.
          min_index = page_number * items_per_page
          max_index = min_index + items_per_page
          return itertools.islice(enumerate(items), min_index, max_index)

        def clothes_reco_3_swipe (mood) :
          Y = model5.encode(data["description"])
          cos_sim_mood = cosine_similarity(X,Y)
          data["cos_sim_list"] = list(cos_sim_mood[0])
          
          clothes_reco_3_swipe = data.sort_values(by=['cos_sim_list'], ascending=False).groupby(by= 'category').head(2).drop_duplicates(subset = 'category', keep = 'last').reset_index(drop=True)
          clothes_reco_3_swipe = clothes_reco_3_swipe[clothes_reco_3_swipe.category.isin(dict_corr[clothes_reco_3_swipe.loc[0]["category"]])].head(3).reset_index(drop=True) 
          st.image(Image.open(F"./Photos/{clothes_reco_3_swipe.loc[0]['id_clothes']}.jpg"), width=350)
          st.markdown(F"Your cloth recommendation according to your mood is this {clothes_reco_3_swipe.loc[0]['category']} : *{clothes_reco_3_swipe.loc[0]['description']}*")

          st.markdown('With this item, we recommand you two options :')

          item_imgs_swipe =[]
          for elem in range (1,3) :
              product_name_swipe = str(clothes_reco_3_swipe.loc[elem]['id_clothes'])
              imgs_swipe = Image.open(F'./Photos/{product_name_swipe}.jpg')
              item_imgs_swipe.append (imgs_swipe)
          image_iterator_swipe = paginator("", item_imgs_swipe)
          indices_on_page, images_on_page = map(list, zip(*image_iterator_swipe))
          st.image(images_on_page, width=200)

        def clothes_reco (mood) :
          Y = model5.encode(data["description"])
          cos_sim_mood = cosine_similarity(X,Y)
          data["cos_sim_list"] = list(cos_sim_mood[0])

          clothes_reco_3 = data.sort_values(by=['cos_sim_list'], ascending=False).drop_duplicates(subset='category')[["id_clothes", "description", "category"]].reset_index(drop=True)
          clothes_reco_3 = clothes_reco_3[clothes_reco_3.category.isin(dict_corr[clothes_reco_3.loc[0]["category"]])].head(3).reset_index(drop=True)
          st.image(Image.open(F"./Photos/{clothes_reco_3.loc[0]['id_clothes']}.jpg"), width=350)
          st.markdown(F"Your cloth recommendation according to your mood is this {clothes_reco_3.loc[0]['category']} : *{clothes_reco_3.loc[0]['description']}*")
          
          st.markdown('With this item, we recommand you two options :')

          item_imgs =[]
          for elem in range (1,3) :
              product_name = str(clothes_reco_3.loc[elem]['id_clothes'])
              img = Image.open(F'./Photos/{product_name}.jpg')
              item_imgs.append (img)
          image_iterator = paginator("Recommendation", item_imgs)
          indices_on_page, images_on_page = map(list, zip(*image_iterator))
          st.image(images_on_page, width=200)
              

        st.markdown("## 👩 🧔‍♂️ Virtual closet 👕 👗 👚 👔")
        st.sidebar.markdown("# Virtual closet")

        # Texte d'entrée
        st.subheader("How are you doing today ?⭐")
        col1, col2 = st.columns(2)
        with col1:
            mood = st.text_input(label = "")

        # Algo de recommandation
        #model5 = SentenceTransformer("paraphrase-multilingual-mpnet-base-v2")
        #data = pd.read_excel("./Dataset/Clothes_table.xlsx")
        #data["cos_sim_list"] = ""
        #X = model5.encode(mood).reshape(1, -1)
        @st.cache(allow_output_mutation=True)
        def load_model(model_name):
          model5 = SentenceTransformer(model_name)
          return (model5)
        model5 = load_model("paraphrase-multilingual-mpnet-base-v2")
        data = pd.read_excel("./Dataset/Clothes_table.xlsx")
        data["cos_sim_list"] = ""
        X = model5.encode(mood).reshape(1, -1)

        if (st.button('Go to my wardrobe !', on_click=callback) or st.session_state.button_clicked ):
          clothes_reco (mood)
          st.balloons()
          st.markdown('**If you do not like this recommendation, feel free to swipe !**')
          if (st.button('Swipe 👈', on_click=callback) or st.session_state.button_clicked):
            clothes_reco_3_swipe (mood)

    ###Troisième page

    def Update_virtual_closet():
      st.markdown("# Update virtual closet 🔧")
      st.sidebar.markdown("# Update virtual closet ")
      data_page_3 = pd.read_excel("./Dataset/Clothes_table.xlsx")

      ## Explore the virtual closet
      def paginator(label, items, items_per_page=10, on_sidebar=True):
          # Figure out where to display the paginator
        if on_sidebar:
          location = st.sidebar.empty()
        else:
          location = st.empty()

      # Display a pagination selectbox in the specified location.
        items = list(items)
        n_pages = len(items)
        n_pages = (len(items) - 1) // items_per_page + 1
        page_format_func = lambda i: "Page %s" % i
        page_number = location.selectbox(label, range(n_pages), format_func=page_format_func)

      # Iterate over the items in the page to let the user display them.
        min_index = page_number * items_per_page
        max_index = min_index + items_per_page
        return itertools.islice(enumerate(items), min_index, max_index)

      st.subheader("Explore your virtual closet")
      category_to_display = st.selectbox("Select a clothing category you want to see", data_page_3["category"].sort_values().unique())
      mask = data_page_3["category"] == category_to_display
      product_name = data_page_3["id_clothes"][mask]
      item_imgs= []
      for elem in product_name :
        img = Image.open(F'./Photos/{elem}.jpg')
        #st.image(Image.open(F'./Photos/{elem}.jpg'), width=150, caption=elem)
        item_imgs.append (img)
      image_iterator = paginator("Select a page", item_imgs)
      indices_on_page, images_on_page = map(list, zip(*image_iterator))
      st.image(images_on_page, width=150, caption=indices_on_page)


      ## Add a new item
      st.subheader("Add a new item")
      col1, col2 = st.columns(2)
      
      ## To upload a picture
      i = 10
      with col1:
        uploaded_file = st.file_uploader("Upload a picture")
        
        if uploaded_file is not None :
          img = Image.open(uploaded_file)
          st.image(img, width=500)
          st.success("**The item is sucessfully Uploaded.**")
          item_category = st.selectbox("Select the item category", data_page_3["category"].sort_values().unique())
          item_description = st.text_input(label = "Why did you buy this clothing? In what circumstances do you imagine yourself wearing it?")
          file_details = {uploaded_file.name : F"{item_category}_{i}.jpg", uploaded_file.type : "jpg"}

          download_picture = st.button("Save your item")
          if download_picture :
            with open("Downloads", "wb") as f:
              f.write(uploaded_file.getbuffer())
            st.success(f'File {F"{item_category}{i}.jpg"} is successfully saved!')
        i += 1  

            
      ### To take a picture
      with col2:
        camera_input = st.camera_input("Take a picture")
        if camera_input is not None:
        # To read image file buffer as bytes:
          picture = camera_input.getvalue()
          picture_item_category = st.selectbox("Select the category", data_page_3["category"].sort_values().unique())
          picture_item_description = st.text_input(label = "Why did you buy this clothing? In what circumstances do you imagine yourself wearing it?")
          
          download_picture_camera = st.button("Save your item !")
          if download_picture_camera :
            with open("Downloads", "wb") as f:
              f.write(camera_input.getbuffer())
              st.success(f'File {F"{picture_item_category}{i}.jpg"} is successfully saved!')
            i += 1  


    page_names_to_funcs = {
        "About us 🤓": About,
        "Your recommendation of the day 🌟": Virtual_closet,
        "Admin your virtual closet 🔧": Update_virtual_closet,
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







