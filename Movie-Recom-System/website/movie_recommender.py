import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from omdbapi.movie_search import GetMovie
import imdb

invalid = -1000000000000


def get_title_from_index(index, df):
	""" this function gets the title of the movie from the index
    Args:
        index: index for which we want a title
		df: DataFrame containing all movies and movie information 
    """

	return df[df.index == index]["title"].values[0]

def get_index_from_title(title, df):
	""" this function gets the index of the movie from the title
    Args:
        title: title for which we want a index
		df: DataFrame containing all movies and movie information 
    """

	if(len(df[df.title == title]) == 0):
		return None
	return df[df.title == title]["index"].values[0]



def getTopNMovies(movie, reqestedNo):
	""" this function gets the relevant movies till we have the requested number of relevant movies
    Args:
        movie: movie for which we need to find relevant elements
		reqestedNo: the number of relevant movies we want
    """

	df = pd.read_csv('movie_dataset.csv')
	
	features = ["keywords", "genres", "cast"]

	for feature in features:
		df[feature] = df[feature].fillna('')

	def combine_features(row):
		return row["keywords"] + " " + row["genres"] + " " + row["cast"]
			

	df['combined_features'] = df.apply(combine_features, axis = 1)

	cv = CountVectorizer()

	count_matrix = cv.fit_transform(df["combined_features"])

	cosine_similarityVal = cosine_similarity(count_matrix)
	movie_user_likes = movie 

	movie_index = get_index_from_title(movie_user_likes, df)

	similar_movies = list(enumerate(cosine_similarityVal[movie_index]))

	sorted_similar_movies = sorted(similar_movies, key=lambda x:x[1], reverse = True)

	i = 1
	result = []
	for movie in sorted_similar_movies:

		if i>reqestedNo:
			break

		title = get_title_from_index(movie[0], df)
		result.append(title)
	
		i = i+1

	return result



def findClosenessOfMovies(matchingMovie, userInputtedMovie):
	""" this function returns a score of how close two movies are
    Args:
        userInputtedMovie: movie1 - the movie for which we are trying to find closely matching elements
		matchingMovie: movie2 - the movie for which we are trying to see how close matchingMovie is to userInputtedMovie
    """

	df = pd.read_csv('movie_dataset.csv')

	movie_index1 = get_index_from_title(matchingMovie, df)
	if(movie_index1 == None):
		return invalid

	features = ["keywords", "genres"]

	for feature in features:
		df[feature] = df[feature].fillna('')

	def combine_features(row):
		return row["keywords"] + " " + row["genres"]	

	df['combined_features'] = df.apply(combine_features, axis = 1)

	cv = CountVectorizer()

	count_matrix = cv.fit_transform(df["combined_features"])

	cosine_similarityVal = cosine_similarity(count_matrix)
	
	movie_user_likes = userInputtedMovie 


	movie_index = get_index_from_title(movie_user_likes, df)

	print(movie_user_likes)
	print(movie_index)
	print(matchingMovie)
	print(movie_index1)
	if(movie_index1 != None):
		return (cosine_similarityVal[movie_index][movie_index1])



	
	
	


