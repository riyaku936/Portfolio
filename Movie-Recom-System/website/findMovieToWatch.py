import bs4
from urllib.request import urlopen as uReq
import requests
from bs4 import BeautifulSoup
from datetime import timedelta, date
import movie_recommender
import imdb
import pandas as pd

# this website shows movie results from these channels:
listOfMoveChannels = {'film4': '69035909', 
'sony-movies-uk' : '69046254', 
'sony-movies-action' : '69041512',
'sky-cinema-premiere' : '69036152',
'sky-cinema-select' : '69036142',
'sky-cinema-hits' : '69036180',
'sky-cinema-drama' : '69036124',
'sky-cinema-disney' : '444304394',
'sky-cinema-family' : '69036128',
'sky-cinema-action' : '69036117',
'sky-cinema-greats' : '69036148',
'sky-cinema-thriller' : '69038225',
'sky-cinema-comedy' : '69036121',
'sky-cinema-scfihorror' : '69036166',
'sky-cinema-premiere1' : '69036151',
'horror-channel-uk' : '69040564',
'movies-24' : '69044016'
}


###### TV RELATED FUNCTIONS######


# for a given channel this function will return the TV schedule for coming N days ahead
def getAllMoviesForNDays(channel, channelCode, noDaysAhead):
    """ for a given channel this function will return the TV schedule for coming N days ahead
    Args:
        channel: the channel for which we are getting schedule
        channelCode: the channelCode for the channel we are finding information for
        noDaysAhead: the no of days to find the schedule for 
    """

    schedule = {}

    for i in noDaysAhead:
        today = str(date.today() + timedelta(days=i))
        url = 'https://www.ontvtonight.com/uk/guide/listings/channel/'+channelCode+'/'+channel+'.html?dt=' + today
        listOfMovies = getMoviesOneDay(url)
        schedule[str(today)] = listOfMovies

    return schedule


def getMoviesOneDay(url):
    """ this function will webscrape the given TV schedule on the URL and extract out the movies that are being shown on the TV schedule
    Args:
        url: URL which contains the movie schedule for the channel
    """

    response = requests.get(url)
    html = response.text

    listOfMovieNames = []

    soup = BeautifulSoup(html, 'html.parser')
    movietags = soup.select('td')

    i = 1

    while i < len(movietags):
        element = movietags[i]
        movieName = element.text.split()
        movieNameString = ""
        for element in movieName:
            movieNameString = movieNameString + " " + element

        movieNameString = movieNameString.strip()
        listOfMovieNames.append(movieNameString)
        i = i + 2
    
    return listOfMovieNames


def getDataForAllChannels():
    """this function get the TV schedule for all the available channels 
    """

    allChannels = {}
    for key in listOfMoveChannels:
        allChannels[key] = getAllMoviesForNDays(key, listOfMoveChannels[key], [0])
    return allChannels


def orderBy(element):
    """ this is a helper function that lets us 
    Args:
        element: the element we are ordering
    """
    return element[2]


def getASortedRelevantList(userInputtedMovie):
    """ this function sorts all the Movies available on TV based on how related it is to the user inputted movie
    Args:
        userInputtedMovie: the movie for which we genenrate a list of relevant movies in order of their relevance 
    """
    ia = imdb.IMDb() 
    df = pd.read_csv('movie_dataset.csv')
    allDataForAllChannels = getDataForAllChannels()
    listOfAllFilms = []
    counter = 0
    for channel in allDataForAllChannels:
    	for date in allDataForAllChannels[channel]:
    		for movieName in allDataForAllChannels[channel][date]:
    			results = ia.search_movie(movieName)
    			if(len(results) == 0):
    				continue
    			firstResult = results[0].movieID
    			IMDBmovie = ia.get_movie(str(firstResult)) 
    			IMDBmovieName = IMDBmovie.get('title')
    			indexOfMovie = movie_recommender.get_index_from_title(IMDBmovieName, df)
    			if indexOfMovie != None:
    				listOfAllFilms.append((counter, IMDBmovieName, movie_recommender.findClosenessOfMovies(IMDBmovieName, userInputtedMovie), channel, date))
    				counter = counter + 1
    			else:
    				print("null")
    				print(movieName)
    setOfAllFilms = set(listOfAllFilms)
    listOfAllFilms = list(setOfAllFilms)
    listOfAllFilms.sort(key=orderBy)
    listOfAllFilms.reverse()
    return listOfAllFilms

###### Netflix ######


def getMoviesFromNetflix(movieName):
    """ this function gets a list of all the relevant movies available on netflix using the netflix_titles.csv dataset of netflix titles
    Args:
        movieName: the movie for which we need to find relevant netflix movies
    """

    listOfMostRelevant100 = movie_recommender.getTopNMovies(movieName, 200)

    df = pd.read_csv('netflix_titles.csv')

    result = []

    for movie in listOfMostRelevant100:
        if df.loc[(df['title'] == movie)].empty == False:
            result.append(movie)
        if len(result) > 21:
            break


    return result


###### Amazon ######


def getMoviesFromAmazon(movieName):
    """ this function gets a list of all the relevant movies available on amazon prime using the amazon_titles.csv dataset of amazon prime titles
    Args:
        movieName: the movie for which we need to find relevant amazon prime movies
    """

    listOfMostRelevant100 = movie_recommender.getTopNMovies(movieName, 200)

    df = pd.read_csv('amazon_titles.csv')


    result = []

    for movie in listOfMostRelevant100:
        if df.loc[(df['title'] == movie)].empty == False:
            result.append(movie)
        if len(result) > 21:
            break



    return result



