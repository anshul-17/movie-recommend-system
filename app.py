from http.client import responses

import requests
import streamlit as st
import  pickle
import  pandas as pd
import requests

def fetch_poster(movie_id):
    response = requests.get("https://api.themoviedb.org/3/movie/{}?api_key=9a231046b02c4b1f35179f5c40a69d62&language=en-US".format(movie_id))
    data = response.json()
    print(data)
    #return "https://image.tmdb.org/t/p/w500/" + data.get['poster_path']
    poster_path = data.get('poster_path')

    if poster_path:
        return f"https://image.tmdb.org/t/p/w500/{poster_path}"
    else:
        return "https://via.placeholder.com/500x750?text=No+Poster+Available"



def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_poster = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        # fettch poster from API
        recommended_movies_poster.append(fetch_poster(movie_id))
    return recommended_movies,recommended_movies_poster


movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies=pd.DataFrame(movies_dict)

similarity=pickle.load(open('similarity.pkl', 'rb'))


st.title("Movie Recommender System")

selected_movies_name = st.selectbox(
    "Select Movie Here",
    movies['title'].values
)

if st.button('Recommend'):
    name,poster = recommend(selected_movies_name)
    col1, col2, col3, col4, col5  = st.columns(5)
    with col1:
        st.text(name[0])
        st.image(poster[0])

    with col2:
        st.text(name[1])
        st.image(poster[1])

    with col3:
        st.text(name[2])
        st.image(poster[2])

    with col4:
        st.text(name[3])
        st.image(poster[3])

    with col5:
        st.text(name[4])
        st.image(poster[4])
