import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

pd.set_option('display.max_rows', None) 
ani_data = pd.read_json('./anime_data.json')
ani_data = ani_data[ani_data['popularity'] >= 1500]
ani_data = ani_data[ani_data['score'] >= 5.0]
x = np.array(ani_data.desc)
pd.set_option('display.expand_frame_repr', False)
description_data = x
all_genres = sorted(set(genre for sublist in ani_data['genres'] for genre in sublist))
print(all_genres)
for genre in all_genres:
    ani_data.loc[:,genre] = ani_data.loc[:,'genres'].apply(lambda x: 1 if genre in x else 0)    

genre_columns = ani_data.columns[7:]
liked_anime = pd.read_json('./anime_liked.json')
user_profile = {'user' : [liked_anime.loc[1:,'user'][1]]}
user_profile = pd.DataFrame(data=user_profile)

user_ratings = liked_anime['rating']
liked_genres = []
general_rating = []
for anime in liked_anime['anime']:
    liked_genres.append(anime['genres'])
    general_rating.append(anime['score'])

user_profile['score'] = sum(general_rating)/len(general_rating)

for g in all_genres:
    user_profile[g]=0.0

liked_anime['rating']= liked_anime['rating'].fillna(5)

liked_anime['genres'] = liked_genres
liked_anime['general_rating'] = general_rating

for index, row in liked_anime.iterrows():
    liked_genres = row['genres']
    for g in liked_genres:
        user_profile.loc[0:,g] += row['rating']

user_profile.iloc[0:,2:] = user_profile.iloc[0:,2:].apply(lambda x: x/(liked_anime['rating'].sum()))
sim = pd.DataFrame(cosine_similarity(user_profile.iloc[0:,1:],ani_data.iloc[:,[5] + list(range(7,ani_data.shape[1]))]))
simularity_indexes = sim.T.sort_values(by=0, ascending=False).index
recommendations = ani_data.iloc[simularity_indexes].iloc[:,0:7]
print(sim)
