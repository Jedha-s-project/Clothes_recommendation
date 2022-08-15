import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
from sentence_transformers import SentenceTransformer
import sklearn
from sklearn.metrics.pairwise import cosine_similarity
import base64


### Config
st.set_page_config(
    page_title="Don't look out: clothes denied",
    page_icon="🌟",
    layout="wide"
)

### Pages
st.selectbox(
  'Gender',
  ('Female','Male')
)

### Side bar 
st.sidebar.header("Choose your clothes with Don't look out")
st.sidebar.markdown("""
    * [About](#About)
    * [Virtual Closet](#virtual-closet)
    * [Update](#update)
""")
e = st.sidebar.empty()
e.write("")
st.sidebar.write("Made with 💖 by Coralie & Fanny")

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


# photos = "https://github.com/Jedha-s-project/Clothes_recommendation/tree/main/Photos" = quel intérêt si elles sont en local ?

### App

# Titre
st.title("Don't look out, clothing denial ! 🙈 ")

# Sous titre
st.subheader("Good morning and welcome to you virtual closet")

# Présentation 
st.markdown("You never know what to wear in the morning ? You end up going back to the same basic clothes? However, in the stores, you can't resist in front of this little dress or this umpteenth little top that suits you perfectly and that you already imagine wearing!  ")
st.markdown("Our application offers you to choose your outfit for you ! It's very simple:")
st.markdown("1.After each new purchase, enter the reason of your purchase: why do you like this article? In what circumstances do you think you will wear it?")
st.markdown("2.Are you hesitating in front of your dressing room? Enter your mood of the day and our algorithm will make you a personalized recommendation !")
st.markdown("Fantastic, right?")

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

#dictionnaire
dict_corr = {
    'debardeur': ['debardeur', 'pantalon', 'gilet'], 
    'tshirt' : ['tshirt', 'pantalon', 'gilet'], 
    'pull' : ['pull', 'pantalon', 'jupe'],
    'veste' : ['veste', 'tshirt', 'pantalon'], 
    'gilet' : ['gilet', 'pantalon', 'robe'],
    'robe': ['robe', 'gilet', 'veste'],
    'short': ['short', 'debardeur', 'tshirt'], 
    'blouse': ['blouse', 'pantalon', 'veste'], 
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
      st.markdown(F"Your clothe recommendation is {product_name}")
      st.markdown(F"Clothe description : {clothes_reco_3.loc[i]['description']}")
      st.image(Image.open(F'./Photos/{product_name}.jpg'), width=500)
      
  return clothes_reco

if st.button('Find my clothe ! '):
     clothes_reco (mood)





