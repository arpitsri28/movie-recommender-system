from sklearn.metrics.pairwise import cosine_similarity
from preprocessing import load_and_process_data, get_feature_names
import pickle 
import requests

new_df, vectors, cv, other_details = load_and_process_data()
feature_names = get_feature_names(cv)
similarity = cosine_similarity(vectors)

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=acd48610c34b4bfc4230df49d7f66393&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path


def recommend(movie):
  movie_index = new_df[new_df['title'] == movie].index[0]
  distances = similarity[movie_index]
  movies_list = sorted(list(enumerate(distances)), reverse = True, key = lambda x: x[1])[1:6]
  recommendations = []
  for i in movies_list:
    movie_id = new_df.iloc[i[0]].movie_id
    details = {
            'title': new_df.iloc[i[0]].title,
            'poster': fetch_poster(movie_id),
            'genres': other_details.iloc[i[0]].genres,
            'release_date': other_details.iloc[i[0]].release_date,
            'cast': other_details.iloc[i[0]].cast,
            'overview': other_details.iloc[i[0]].overview,
            'crew': other_details.iloc[i[0]].crew,
        }
    recommendations.append(details)

  return recommendations

with open('movies.pkl', 'wb') as file:
    pickle.dump(new_df, file)
