from flask import Flask, render_template, request
from findMovieToWatch import getASortedRelevantList, getMoviesFromNetflix, getMoviesFromAmazon
app = Flask(__name__)
import imdb
import omdb
import re
from omdbapi.movie_search import GetMovie
import string

API_KEY = '4d138262'
omdb.set_default('apikey', API_KEY)


@app.route("/")
@app.route("/index.html", methods=['GET'])
def home():
    """ this function renders the home page 
    """
    
    return render_template('index.html')


@app.route("/whereToWatch.html", methods=['GET'])
def whereToWatch():
    """ this function renders to whereToWatch page displaying which similar movies are on TV, Netflix and Amazon Prime
    """

    movieName = request.args.get("movie")

    ####### COLLECT RELEVANT TV MOVIES ######


    listOfMoviesOnTV = getASortedRelevantList(movieName)[:10]


    factFileTV = []


    for movieOnTV in listOfMoviesOnTV:
        movieName = movieOnTV[1]
        factFile = getInfoAboutMovie(movieName)
        newEntry = (movieOnTV[0], movieOnTV[1], movieOnTV[2], movieOnTV[3], movieOnTV[4], factFile)
        
        factFileTV.append(newEntry)
    postersTV = [v[5].get('poster') for v in factFileTV]

   

    ####### COLLECT RELEVANT NETFLIX MOVIES ######

    listOfMoviesOnNetflix = getMoviesFromNetflix(movieName)


    factFileNeflix = []

    for movieOnNetflix in listOfMoviesOnNetflix:
        factFile = getInfoAboutMovie(movieOnNetflix)
        newEntry = factFile
        factFileNeflix.append(newEntry)


    postersNetflix = [element.get('poster') for element in factFileNeflix]

    
    getInfoAboutMovie("Titanic")

    ###### COLLECT RELEVANT AMAZON MOVIES ######

    listOfMoviesOnAmazon = getMoviesFromAmazon(movieName)


    factFileAmazon = []

    for movieOnAmazon in listOfMoviesOnAmazon:
        factFile = getInfoAboutMovie(movieOnAmazon)
        newEntry = factFile
        factFileAmazon.append(newEntry)

    postersAmazon = [element.get('poster') for element in factFileAmazon]


    
    return render_template('whereToWatch.html', factFileTV = factFileTV, image = postersTV, factFileNeflix = factFileNeflix, postersNetflix = postersNetflix, factFileAmazon = factFileAmazon, postersAmazon = postersAmazon)


def removePunct(inputStr):
    """ this function removes the punctuation from content to avoid errors in displaying content
    Args:
        inputStr: string to reformat
    """

    return re.sub(r'[^\w\s]','',inputStr)


def getInfoAboutMovie(movie):
    """ this function uses the IMDB and OMDB apis to get the following information about the inputted API: name | plot | poster
    Args:
        movie: movie to get details for
    """

    ia = imdb.IMDb() 
    search = ia.search_movie(movie) 
    firstResult = search[0].movieID
    movie = ia.get_movie(str(firstResult))
    name = movie.get('title')
    
    plot = movie.get('plot')[0]

    withAuthor = plot.split("::")
    print("this is plot:")
    print(plot)

    print("withAuthor")
    print(withAuthor)

    withAuthor.pop()

    strResult = ""
    for i in withAuthor:
        strResult = strResult + withAuthor[i]

    
    plot = strResult

    print("this is plot:")
    print(plot)

    poster_response = omdb.search_movie(name, timeout=5)
    if(len(poster_response) == 0):
        poster = 'https://www.pciglobal.org/wp-content/uploads/2018/04/vertical-rectangle-4.jpg'
    
    else:
        poster = poster_response[0].get('poster')

    return {"name": removePunct(name), "plot": removePunct(plot), "poster" : poster}
    


if __name__ == "__main__":
    app.static_folder = 'static'
    # app.run(debug=True)
    app.run(host='0.0.0.0', port=8000)  


