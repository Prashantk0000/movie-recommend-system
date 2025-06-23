import pickle
import streamlit as st
import pandas as pd
import requests
import os

# === Function to fetch movie poster ===
def fetch_poster(movie_id):
    try:
        api_key = "8265bd1679663a7ea12ac168da84d2e8"
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US"
        data = requests.get(url).json()
        poster_path = data.get('poster_path')
        if poster_path:
            return "https://image.tmdb.org/t/p/w500/" + poster_path
        else:
            return "https://via.placeholder.com/500x750?text=No+Image"
    except:
        return "https://via.placeholder.com/500x750?text=Error"

# === Function to recommend movies ===
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_names.append(movies.iloc[i[0]].title)
        recommended_movie_posters.append(fetch_poster(movie_id))
    return recommended_movie_names, recommended_movie_posters

# === Streamlit UI ===
st.set_page_config(page_title="🎬 Movie Recommender", layout="wide")
st.header('🎬 Movie Recommender System')

# === Load Data Safely ===
try:
    movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
    similarity = pickle.load(open('similarity.pkl', 'rb'))
    movies = pd.DataFrame(movies_dict)
except FileNotFoundError as e:
    st.error(f"❌ Missing file: {e.filename}")
    st.stop()
except Exception as e:
    st.error(f"⚠️ Failed to load files: {e}")
    st.stop()

# === Movie Selector ===
movie_list = movies['title'].values
selected_movie = st.selectbox("🎥 Type or select a movie", movie_list)

# === Show Recommendations ===
if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            st.text(recommended_movie_names[i])
            st.image(recommended_movie_posters[i])
