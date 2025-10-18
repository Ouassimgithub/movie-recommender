import os
import pickle
import streamlit as st
import requests

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=39fd8d4d1ce8624768c3d04549424e37&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path'] 
    full_path = "https://image.tmdb.org/t/p/w500/"+poster_path
    return full_path




def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    recommanded_movie_name = []
    recommanded_movie_poster = []
    distances = sorted(list(enumerate(similarity[index])), reverse = True, key = lambda x:x[1])
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        recommanded_movie_poster.append(fetch_poster(movie_id))
        recommanded_movie_name.append(movies.iloc[i[0]].title)
    return recommanded_movie_name,recommanded_movie_poster


st.title("🎬 Discover Movies You'll Love")
st.subheader("AI-powered recommendations in seconds")

is_cloud = os.path.exists("/mount/src")
if is_cloud:
    # Running on Streamlit Cloud (has new pickles)
    movies = pickle.load(open("artifacts/movie_list_new.pkl", "rb"))
    similarity = pickle.load(open("artifacts/similarity_new.pkl", "rb"))
else:
    # Running locally (has old pickles)
    movies = pickle.load(open("artifacts/movie_list.pkl", "rb"))
    similarity = pickle.load(open("artifacts/similarity.pkl", "rb"))

movie_list = movies["title"].values
selected_movie = st.selectbox(
    "Which movie did you enjoy?",
    movie_list
)
# env/python -m streamlit run app.py
if st.button("Show recommendation"):
    recommanded_movies_name, recommanded_movies_poster = recommend(selected_movie)
    col1,col2,col3,col4,col5 = st.columns(5)
    with col1:
        st.text(recommanded_movies_name[0])
        st.image(recommanded_movies_poster[0])
    with col2:
        st.text(recommanded_movies_name[1])
        st.image(recommanded_movies_poster[1])
    with col3:
        st.text(recommanded_movies_name[2])
        st.image(recommanded_movies_poster[2])
    with col4:
        st.text(recommanded_movies_name[3])
        st.image(recommanded_movies_poster[3])
    with col5:
        st.text(recommanded_movies_name[4])
        st.image(recommanded_movies_poster[4])