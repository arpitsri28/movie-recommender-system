import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
import helper

def load_and_process_data():
    movies = pd.read_csv('tmdb_5000_movies.csv')
    credits = pd.read_csv('tmdb_5000_credits.csv')
    movies = movies.merge(credits, on="title")
    movies = movies[['movie_id', 'release_date', 'title', 'overview', 'genres', 'keywords', 'cast', 'crew']]
    movies.dropna(inplace=True)

    movies['genres'] = movies['genres'].apply(helper.convert)
    movies['keywords'] = movies['keywords'].apply(helper.convert)
    movies['cast'] = movies['cast'].apply(helper.convert_cast)
    movies['crew'] = movies['crew'].apply(helper.fetch_director)
    other_details = movies[['movie_id', 'title', 'release_date', 'overview', 'genres', 'cast', 'crew']]
    movies['overview'] = movies['overview'].apply(lambda x: x.split())
    movies['genres'] = movies['genres'].apply(lambda x: [i.replace(" ", "") for i in x])
    movies['keywords'] = movies['keywords'].apply(lambda x: [i.replace(" ", "") for i in x])
    movies['cast'] = movies['cast'].apply(lambda x: [i.replace(" ", "") for i in x])
    movies['crew'] = movies['crew'].apply(lambda x: [i.replace(" ", "") for i in x])
    movies['tags'] = movies['overview'] + movies['genres'] + movies['keywords'] + movies['cast'] + movies['crew']

    new_df = movies[['movie_id', 'title', 'tags']]
    new_df.loc[:, 'tags'] = new_df['tags'].apply(lambda x: " ".join(x))
    new_df.loc[:, 'tags'] = new_df['tags'].apply(lambda x: x.lower())
    new_df.loc[:, 'tags'] = new_df['tags'].apply(helper.stem)

    other_details.loc[:, 'genres'] = other_details['genres'].apply(lambda x: ', '.join(x))
    other_details.loc[:, 'cast'] = other_details['cast'].apply(lambda x: ', '.join(x))
    other_details.loc[:, 'crew'] = other_details['crew'].apply(lambda x: ', '.join(x))

    cv = CountVectorizer(max_features=5000, stop_words='english')
    vectors = cv.fit_transform(new_df['tags']).toarray()

    return new_df, vectors, cv, other_details

def get_feature_names(cv):
    return cv.get_feature_names_out()

