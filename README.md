
# Don't look out: clothes denial!

Project carried out in two weeks, in August 2022, within the framework of our training Data Fullstack, Jedha's Bootcamp Paris. 

We created a virtual closet, offering you to choose your outfit for you according to your daily mood or your diary.
The app select one item, the one which best fit your mood and display two more items to wear with. 
If you don't agree whith this first proposition, you can swipe to get a second one.

To do so, we used the Sentence Transformer model to evaluate the text similarities between the user's mood (input section) and the description of the clothes (input section description for each items, done once when you put your clothes in your virtual wardrobe).





## Installation

To install our project in local, you first need to git clone our repository (https://github.com/Jedha-s-project/Clothes_recommendation). Then, create a virtual environment (see Environment Variables section). Finally, run our app on Streamlit (terminal command: streamlit run app.py).

    
## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

`numpy==1.23.1`
`pandas==1.4.3`
`Pillow==9.2.0`
`scikit_learn==1.1.2`
`sentence_transformers==2.2.2`
`streamlit==1.12.0`
`openpyxl`



## Demo

https://share.vidyard.com/watch/95gwXFzFWPqU8kHNNrAz5i?



## Screenshots

![App page 1 "About us"](https://github.com/Jedha-s-project/Clothes_recommendation/blob/main/Screenshot%20About%20page.png)
![App page 2 "Virtual Closet"](https://github.com/Jedha-s-project/Clothes_recommendation/blob/main/Screenshot%20Virtual%20Closet%20page.png)
![App page 3 "Update virtual closet"](https://github.com/Jedha-s-project/Clothes_recommendation/blob/main/Screenshot%20Virtual%20Closet%20page.png)
## Roadmap

- To go further with the model you can: integrate weather, diary and clothes recognition. You can also try to fine tuning the model to be more performant. 
- To go further with the streamlit app you can: add a user login connection, add items categories (like shoes), develop the consulting-adding-deleting part in the administration page, add inspiring and attractive sentences according to the user's mood.  


## Deployment

You won't be able to deploy this project with the free version of Heroku, as Sentence Transfromer is too heavy.


## Authors

- [Coralie Guillotte ](https://github.com/CoralieGM)

- [Fanny Malmartel ](https://github.com/Fanny-Mlmrtl)


