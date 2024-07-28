import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

def importAnimeDataAndProcess(all_anime):
    '''import all anime into pandas df and filters out unwanted detail
       in this case, obscure and low rated anime are filtered out'''
    import json
    from io import StringIO
    ani_data = pd.read_json(StringIO(json.dumps(all_anime)))
    ani_data = ani_data[ani_data['popularity'] >= 1500]
    ani_data = ani_data[ani_data['score'] >= 5.0]
    return ani_data

def importLikedAnimeAndProcess(liked_anime_data, all_genres):
    '''imports user liked anime'''
    import json
    from io import StringIO
    liked_anime = pd.read_json(StringIO(json.dumps(liked_anime_data)))
    user_profile = {'user' : [liked_anime.loc[1:,'user'][1]]}
    user_profile = pd.DataFrame(data=user_profile)

    '''obtaining user ratings and the anime's average rating'''
    user_ratings = liked_anime['rating']
    liked_genres = []
    general_rating = []
    for anime in liked_anime['anime']:
        liked_genres.append(anime['genres'])
        general_rating.append(anime['score'])

    '''to create the user profile, the score attribute is the mean of all general ratings from the anime'''
    user_profile['score'] = sum(general_rating)/len(general_rating)
    '''setting up the genres this user likes'''
    for g in all_genres:
        user_profile[g]=0.0
    '''all liked anime that has not been rated by the user will be default of 5'''
    liked_anime['rating']= liked_anime['rating'].fillna(5)

    liked_anime['genres'] = liked_genres
    liked_anime['general_rating'] = general_rating

    '''weighted genre. for each genre in liked anime, add the user score to that genre column'''
    for index, row in liked_anime.iterrows():
        liked_genres = row['genres']
        for g in liked_genres:
            user_profile.loc[0:,g] += row['rating']

    '''divide all genre columns by the sum of all ratings'''
    user_profile.iloc[0:,2:] = user_profile.iloc[0:,2:].apply(lambda x: x/(liked_anime['rating'].sum()))
    return user_profile

def getFavouriteGenres(liked_anime_data):
    import json
    from io import StringIO
    
    '''getting liked anime data'''
    liked_anime = pd.read_json(StringIO(json.dumps(liked_anime_data)))
    '''unrated anime filled with default val of 5'''
    liked_anime['rating']= liked_anime['rating'].fillna(5)
    
    '''once again, weighted genre'''
    all_genres = list(set(genre for anime in liked_anime['anime'] for genre in anime['genres']))
    res = pd.DataFrame(0, index=range(1),columns=all_genres)
    score = liked_anime['rating']
    index = 0
    for anime in liked_anime['anime']:
        for genre in anime['genres']:
            res[genre] += score.iloc[index]
        index += 1
    '''sorted by the most liked genre'''
    return(res.T.sort_values(by=0, ascending=False).to_dict())

def recommend(liked_anime_data,all_anime):
    pd.set_option('display.max_rows', None) 
    pd.set_option('display.expand_frame_repr', False)
    '''import and clean anime data and user data'''
    ani_data = importAnimeDataAndProcess(all_anime)

    all_genres = sorted(set(genre for sublist in ani_data['genres'] for genre in sublist))

    '''set up genre attributes for all anime'''
    for genre in all_genres:
        ani_data.loc[:,genre] = ani_data.loc[:,'genres'].apply(lambda x: 1 if genre in x else 0)   
    
    user_profile = importLikedAnimeAndProcess(liked_anime_data,all_genres)
    
    '''cosine similarity with user profile genres and all anime genres'''
    simGenre = pd.DataFrame(cosine_similarity(user_profile.iloc[0:,2:],ani_data.iloc[:,8:]))
    from scipy.stats import norm
    '''gets absolute val of the difference of scores'''
    score_diff = abs(ani_data.iloc[:,6] - user_profile.iloc[0,1])
    max=score_diff.max()
    '''gets normal distribution likely hood of whether or not the user would probably be satisfied the anime score'''
    meow = (1- norm.cdf(score_diff, loc=0, scale=max))*2
    '''extra weighting on the score'''
    meow *=2
    '''cos sim and score passed through cdf is combined and the recommendation score is the mean of those two'''
    recommend_sim = (simGenre+meow)/2
    '''mow'''
    simularity_indexes = recommend_sim.T.sort_values(by=0, ascending=False).index
    recommendations = ani_data.iloc[simularity_indexes].iloc[:300,0:8]

    return recommendations.reset_index(drop=True).to_dict(orient="index")
    