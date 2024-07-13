import streamlit as st
import pickle
import main

movies_list = pickle.load(open('movies.pkl', 'rb'))
movies_list = movies_list['title'].values
st.title('Movie Recommender System')

selected_movie_name = st.selectbox('Type or select a movie from the dropdown', movies_list)

if 'recommendations' not in st.session_state or st.session_state.selected_movie_name != selected_movie_name:
    if st.button('Show Recommendation'):
        st.session_state.recommendations = main.recommend(selected_movie_name)
        st.session_state.selected_movie_name = selected_movie_name

if 'recommendations' in st.session_state:
    for idx, movie in enumerate(st.session_state.recommendations):
        with st.container():  
            st.write(movie['title'])  
            st.image(movie['poster'], width=150)  
            with st.expander("Show Details"):
                st.write(f"**Overview:** {movie['overview']}")
                st.write(f"**Release Date:** {movie['release_date']}")
                st.write(f"**Genres:** {movie['genres']}")
                st.write(f"**Cast:** {movie['cast']}")
                st.write(f"**Director:** {movie['crew']}")
