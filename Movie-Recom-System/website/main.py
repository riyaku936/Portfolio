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

    
    # factFileTV = [(39, 'Wall Street: Money Never Sleeps', 0.408248290463863, 'sky-cinema-greats', '2020-09-04', {'name': 'Wall Street Money Never Sleeps', 'plot': 'Now out of prison but still disgraced by his peers Gordon Gekko works his future soninlaw an idealistic stock broker when he sees an opportunity to take down a Wall Street enemy and rebuild his empire', 'poster': 'https://m.media-amazon.com/images/M/MV5BMTU5MDEzMzYwMF5BMl5BanBnXkFtZTcwNTcwMjUxMw@@._V1_SX300.jpg'}), (1, 'Shooter', 0.30618621784789724, 'film4', '2020-09-04', {'name': 'Shooter', 'plot': 'A marksman living in exile is coaxed back into action after learning of a plot to kill the President After being double crossed for the attempt and on the run he sets out for the real killer and the truth', 'poster': 'https://m.media-amazon.com/images/M/MV5BMGRjMzY0OGItNDc4YS00OGNlLWI3MGYtZjRkNjdiNWUyNDY4XkEyXkFqcGdeQXVyNTA4NzY1MzY@._V1_SX300.jpg'}), (18, 'The Counselor', 0.294174202707276, 'sky-cinema-hits', '2020-09-04', {'name': 'The Counselor', 'plot': 'A lawyer finds himself in over his head when he gets involved in drug trafficking', 'poster': 'https://m.media-amazon.com/images/M/MV5BMTc3ODk0MTY0N15BMl5BanBnXkFtZTgwOTU2MTEzMDE@._V1_SX300.jpg'}), (45, 'Miss Congeniality', 0.24999999999999994, 'sky-cinema-comedy', '2020-09-04', {'name': 'Miss Congeniality', 'plot': 'An FBI Agent must go undercover in the Miss United States beauty pageant to prevent a group from bombing the event', 'poster': 'https://m.media-amazon.com/images/M/MV5BZDhjNzc4N2MtNWE5ZC00N2M4LWFiYjEtMTE5YmYyMTg3OGY5XkEyXkFqcGdeQXVyMTkzODUwNzk@._V1_SX300.jpg'}), (42, 'Zero Dark Thirty', 0.24999999999999994, 'sky-cinema-greats', '2020-09-04', {'name': 'Zero Dark Thirty', 'plot': 'A chronicle of the decadelong hunt for alQaeda terrorist leader Osama bin Laden after the September 2001 attacks and his death at the hands of the Navy SEALs Team 6 in May 2011', 'poster': 'https://m.media-amazon.com/images/M/MV5BMTQ4OTUyNzcwN15BMl5BanBnXkFtZTcwMTQ1NDE3OA@@._V1_SX300.jpg'}), (23, 'The Wolf of Wall Street', 0.24999999999999994, 'sky-cinema-drama', '2020-09-04', {'name': 'The Wolf of Wall Street', 'plot': 'Based on the true story of Jordan Belfort from his rise to a wealthy stockbroker living the high life to his fall involving crime corruption and the federal government', 'poster': 'https://m.media-amazon.com/images/M/MV5BMjIxMjgxNTk0MF5BMl5BanBnXkFtZTgwNjIyOTg2MDE@._V1_SX300.jpg'}), (43, 'Enemy of the State', 0.2357022603955158, 'sky-cinema-thriller', '2020-09-04', {'name': 'Enemy of the State', 'plot': 'A lawyer becomes targeted by a corrupt politician and his NSA goons when he accidentally receives key evidence to a politically motivated crime', 'poster': 'https://m.media-amazon.com/images/M/MV5BMWI0Y2NhMzMtYTE5ZS00MDlhLTg0ZjEtMjAwZmEwNTc0ODc2XkEyXkFqcGdeQXVyNjU0OTQ0OTY@._V1_SX300.jpg'}), (34, 'Beverly Hills Cop', 0.2357022603955158, 'sky-cinema-action', '2020-09-04', {'name': 'Beverly Hills Cop', 'plot': 'A freewheeling Detroit cop pursuing a murder investigation finds himself dealing with the very different culture of Beverly Hills', 'poster': 'https://m.media-amazon.com/images/M/MV5BN2MyZDE0YjAtNWFjYy00MWRlLTk3MTktMzY3ZDVhNTJkZTlmXkEyXkFqcGdeQXVyNDk3NzU2MTQ@._V1_SX300.jpg'}), (33, 'Desperado', 0.2357022603955158, 'sky-cinema-action', '2020-09-04', {'name': 'Desperado', 'plot': 'Former musician and gunslinger El Mariachi arrives at a small Mexican border town after being away for a long time His past quickly catches up with him and he soon gets entangled with the local drug kingpin Bucho and his gang', 'poster': 'https://m.media-amazon.com/images/M/MV5BYjA0NDMyYTgtMDgxOC00NGE0LWJkOTQtNDRjMjEzZmU0ZTQ3XkEyXkFqcGdeQXVyMTQxNzMzNDI@._V1_SX300.jpg'}), (44, "Ocean's Eleven", 0.22360679774997896, 'sky-cinema-thriller', '2020-09-04', {'name': 'Oceans Eleven', 'plot': 'Danny Ocean and his ten accomplices plan to rob three Las Vegas casinos simultaneously', 'poster': 'https://m.media-amazon.com/images/M/MV5BYzVmYzVkMmUtOGRhMi00MTNmLThlMmUtZTljYjlkMjNkMjJkXkEyXkFqcGdeQXVyNDk3NzU2MTQ@._V1_SX300.jpg'})]
    # postersTV = ['https://m.media-amazon.com/images/M/MV5BMTU5MDEzMzYwMF5BMl5BanBnXkFtZTcwNTcwMjUxMw@@._V1_SX300.jpg', 'https://m.media-amazon.com/images/M/MV5BMGRjMzY0OGItNDc4YS00OGNlLWI3MGYtZjRkNjdiNWUyNDY4XkEyXkFqcGdeQXVyNTA4NzY1MzY@._V1_SX300.jpg', 'https://m.media-amazon.com/images/M/MV5BMTc3ODk0MTY0N15BMl5BanBnXkFtZTgwOTU2MTEzMDE@._V1_SX300.jpg', 'https://m.media-amazon.com/images/M/MV5BZDhjNzc4N2MtNWE5ZC00N2M4LWFiYjEtMTE5YmYyMTg3OGY5XkEyXkFqcGdeQXVyMTkzODUwNzk@._V1_SX300.jpg', 'https://m.media-amazon.com/images/M/MV5BMTQ4OTUyNzcwN15BMl5BanBnXkFtZTcwMTQ1NDE3OA@@._V1_SX300.jpg', 'https://m.media-amazon.com/images/M/MV5BMjIxMjgxNTk0MF5BMl5BanBnXkFtZTgwNjIyOTg2MDE@._V1_SX300.jpg', 'https://m.media-amazon.com/images/M/MV5BMWI0Y2NhMzMtYTE5ZS00MDlhLTg0ZjEtMjAwZmEwNTc0ODc2XkEyXkFqcGdeQXVyNjU0OTQ0OTY@._V1_SX300.jpg', 'https://m.media-amazon.com/images/M/MV5BN2MyZDE0YjAtNWFjYy00MWRlLTk3MTktMzY3ZDVhNTJkZTlmXkEyXkFqcGdeQXVyNDk3NzU2MTQ@._V1_SX300.jpg', 'https://m.media-amazon.com/images/M/MV5BYjA0NDMyYTgtMDgxOC00NGE0LWJkOTQtNDRjMjEzZmU0ZTQ3XkEyXkFqcGdeQXVyMTQxNzMzNDI@._V1_SX300.jpg', 'https://m.media-amazon.com/images/M/MV5BYzVmYzVkMmUtOGRhMi00MTNmLThlMmUtZTljYjlkMjNkMjJkXkEyXkFqcGdeQXVyNDk3NzU2MTQ@._V1_SX300.jpg']



    ####### COLLECT RELEVANT NETFLIX MOVIES ######

    listOfMoviesOnNetflix = getMoviesFromNetflix(movieName)


    factFileNeflix = []

    for movieOnNetflix in listOfMoviesOnNetflix:
        factFile = getInfoAboutMovie(movieOnNetflix)
        newEntry = factFile
        factFileNeflix.append(newEntry)


    postersNetflix = [element.get('poster') for element in factFileNeflix]

    
    getInfoAboutMovie("Titanic")

    postersNetflix  = ['https://m.media-amazon.com/images/M/MV5BYzVmYzVkMmUtOGRhMi00MTNmLThlMmUtZTljYjlkMjNkMjJkXkEyXkFqcGdeQXVyNDk3NzU2MTQ@._V1_SX300.jpg', 'https://m.media-amazon.com/images/M/MV5BMmJmYzBjNTktMTJjZS00ZGRhLWE1Y2QtOWQxZGU0Y2RmMjkyXkEyXkFqcGdeQXVyMTQxNzMzNDI@._V1_SX300.jpg', 'https://m.media-amazon.com/images/M/MV5BMTMyNTc1NzY5MV5BMl5BanBnXkFtZTcwNDM4NTQzMw@@._V1_SX300.jpg', 'https://m.media-amazon.com/images/M/MV5BMTI1MTY2OTIxNV5BMl5BanBnXkFtZTYwNjQ4NjY3._V1_SX300.jpg', 'https://m.media-amazon.com/images/M/MV5BODA3NDhiZjYtYTk2NS00ZWYwLTljYTQtMjU0NzcyMGEzNTU2L2ltYWdlL2ltYWdlXkEyXkFqcGdeQXVyMTQxNzMzNDI@._V1_SX300.jpg', 'https://m.media-amazon.com/images/M/MV5BMjdlMjI2ZjgtN2ViOS00ZmI0LWE0ZTMtZjg1ZjczYWYzOGZjL2ltYWdlL2ltYWdlXkEyXkFqcGdeQXVyNjc1NTYyMjg@._V1_SX300.jpg', 'https://m.media-amazon.com/images/M/MV5BMjYwNGRmMGUtMmI0ZC00MGM0LWI2MTQtNGM0ZGNkMzRhNmY5XkEyXkFqcGdeQXVyODU2MDg1NzU@._V1_SX300.jpg', 'https://m.media-amazon.com/images/M/MV5BYTJkZDljNGYtNjRiNC00ZmY2LTg1NmItYTI1MTllNDQzMWVmXkEyXkFqcGdeQXVyMTMxODk2OTU@._V1_SX300.jpg', 'https://m.media-amazon.com/images/M/MV5BZjk3YmZhMDAtOWUzMS00YjE5LTkxNzAtY2I1NGZjMDA2ZTk0XkEyXkFqcGdeQXVyMTQxNzMzNDI@._V1_SX300.jpg', 'https://m.media-amazon.com/images/M/MV5BMTg4ODg5NzkzNl5BMl5BanBnXkFtZTcwNzAyODM5Mw@@._V1_SX300.jpg', 'https://m.media-amazon.com/images/M/MV5BY2FhZGI5M2QtZWFiZS00NjkwLWE4NWQtMzg3ZDZjNjdkYTJiXkEyXkFqcGdeQXVyMTMxODk2OTU@._V1_SX300.jpg', 'https://m.media-amazon.com/images/M/MV5BMTc4MDIyMTM3NV5BMl5BanBnXkFtZTcwNDQ2Nzg2Mg@@._V1_SX300.jpg', 'https://m.media-amazon.com/images/M/MV5BNzk5ZmQxMWYtM2QyNi00MTY3LTlmNjItYjUwODY3Y2YwOTIwXkEyXkFqcGdeQXVyNDk3NzU2MTQ@._V1_SX300.jpg', 'https://m.media-amazon.com/images/M/MV5BOTJiNDEzOWYtMTVjOC00ZjlmLWE0NGMtZmE1OWVmZDQ2OWJhXkEyXkFqcGdeQXVyNTIzOTk5ODM@._V1_SX300.jpg', 'https://m.media-amazon.com/images/M/MV5BMzViMmMxMzItYmYyYi00NGU3LWI2MDMtNjcwOWFmZTZkOTcwXkEyXkFqcGdeQXVyNDkzNTM2ODg@._V1_SX300.jpg', 'https://m.media-amazon.com/images/M/MV5BYzUxOTg2MzAtOTY3Yi00NDVhLTk4OWItNjFjZmZlMWI2MjdlXkEyXkFqcGdeQXVyNjc1NTYyMjg@._V1_SX300.jpg', 'https://m.media-amazon.com/images/M/MV5BMTI0NjEwNDgwOV5BMl5BanBnXkFtZTYwOTI1NTA3._V1_SX300.jpg', 'https://m.media-amazon.com/images/M/MV5BMjAyMzExMDM1N15BMl5BanBnXkFtZTcwNTcyMTQ5Mg@@._V1_SX300.jpg', 'https://m.media-amazon.com/images/M/MV5BMjQ0OTNjOTMtYWU1MC00MWQwLTllMmMtNWZmYmE3NDY0ZTgxXkEyXkFqcGdeQXVyMTE2OTg4Mjg@._V1_SX300.jpg', 'https://m.media-amazon.com/images/M/MV5BMTEyNDY2Njc1NzheQTJeQWpwZ15BbWU4MDc1NzY2NjYx._V1_SX300.jpg', 'https://m.media-amazon.com/images/M/MV5BMTI5MTE1OTAzOV5BMl5BanBnXkFtZTcwNDc2OTgyMQ@@._V1_SX300.jpg', 'https://m.media-amazon.com/images/M/MV5BYzZiNGUxZmUtYjc0ZC00YzkxLWI2MWMtNDc0MWFiNjc5NGRkXkEyXkFqcGdeQXVyNTIzOTk5ODM@._V1_SX300.jpg']
    factFileNeflix  = [{'name': 'Oceans Eleven', 'plot': 'Danny Ocean and his ten accomplices plan to rob three Las Vegas casinos simultaneously', 'poster': 'https://m.media-amazon.com/images/M/MV5BYzVmYzVkMmUtOGRhMi00MTNmLThlMmUtZTljYjlkMjNkMjJkXkEyXkFqcGdeQXVyNDk3NzU2MTQ@._V1_SX300.jpg'}, {'name': 'Oceans Twelve', 'plot': 'Daniel Ocean recruits one more team member so he can pull off three major European heists in this sequel to Oceans Eleven 2001', 'poster': 'https://m.media-amazon.com/images/M/MV5BMmJmYzBjNTktMTJjZS00ZGRhLWE1Y2QtOWQxZGU0Y2RmMjkyXkEyXkFqcGdeQXVyMTQxNzMzNDI@._V1_SX300.jpg'}, {'name': 'Oceans Thirteen', 'plot': 'Danny Ocean rounds up the boys for a third heist after casino owner Willy Bank doublecrosses one of the original eleven', 'poster': 'https://m.media-amazon.com/images/M/MV5BMTMyNTc1NzY5MV5BMl5BanBnXkFtZTcwNDM4NTQzMw@@._V1_SX300.jpg'}, {'name': 'The Departed', 'plot': 'An undercover cop and a mole in the police attempt to identify each other while infiltrating an Irish gang in South Boston', 'poster': 'https://m.media-amazon.com/images/M/MV5BMTI1MTY2OTIxNV5BMl5BanBnXkFtZTYwNjQ4NjY3._V1_SX300.jpg'}, {'name': 'The Talented Mr Ripley', 'plot': 'In late 1950s New York Tom Ripley a young underachiever is sent to Italy to retrieve Dickie Greenleaf a rich and spoiled millionaire playboy But when the errand fails Ripley takes extreme measures', 'poster': 'https://m.media-amazon.com/images/M/MV5BODA3NDhiZjYtYTk2NS00ZWYwLTljYTQtMjU0NzcyMGEzNTU2L2ltYWdlL2ltYWdlXkEyXkFqcGdeQXVyMTQxNzMzNDI@._V1_SX300.jpg'}, {'name': 'The Rainmaker', 'plot': 'An underdog lawyer takes on a fraudulent insurance company', 'poster': 'https://m.media-amazon.com/images/M/MV5BMjdlMjI2ZjgtN2ViOS00ZmI0LWE0ZTMtZjg1ZjczYWYzOGZjL2ltYWdlL2ltYWdlXkEyXkFqcGdeQXVyNjc1NTYyMjg@._V1_SX300.jpg'}, {'name': 'The Pelican Brief', 'plot': 'A law student uncovers a conspiracy putting herself and others in danger', 'poster': 'https://m.media-amazon.com/images/M/MV5BMjYwNGRmMGUtMmI0ZC00MGM0LWI2MTQtNGM0ZGNkMzRhNmY5XkEyXkFqcGdeQXVyODU2MDg1NzU@._V1_SX300.jpg'}, {'name': 'Babel', 'plot': 'Tragedy strikes a married couple on vacation in the Moroccan desert touching off an interlocking story involving four different families', 'poster': 'https://m.media-amazon.com/images/M/MV5BYTJkZDljNGYtNjRiNC00ZmY2LTg1NmItYTI1MTllNDQzMWVmXkEyXkFqcGdeQXVyMTMxODk2OTU@._V1_SX300.jpg'}, {'name': 'From Dusk Till Dawn', 'plot': 'Two criminals and their hostages unknowingly seek temporary refuge in a truck stop populated by vampires with chaotic results', 'poster': 'https://m.media-amazon.com/images/M/MV5BZjk3YmZhMDAtOWUzMS00YjE5LTkxNzAtY2I1NGZjMDA2ZTk0XkEyXkFqcGdeQXVyMTQxNzMzNDI@._V1_SX300.jpg'}, {'name': 'Takers', 'plot': 'A group of bank robbers find their multimillion dollar plan interrupted by a hardboiled detective', 'poster': 'https://m.media-amazon.com/images/M/MV5BMTg4ODg5NzkzNl5BMl5BanBnXkFtZTcwNzAyODM5Mw@@._V1_SX300.jpg'}, {'name': 'Secret in Their Eyes', 'plot': 'A tightknit team of rising investigators along with their supervisor is suddenly torn apart when they discover that one of their own teenage daughters has been brutally murdered', 'poster': 'https://m.media-amazon.com/images/M/MV5BY2FhZGI5M2QtZWFiZS00NjkwLWE4NWQtMzg3ZDZjNjdkYTJiXkEyXkFqcGdeQXVyMTMxODk2OTU@._V1_SX300.jpg'}, {'name': 'The Informant', 'plot': 'The US government decides to go after an agro business giant with a pricefixing accusation based on the evidence submitted by their star witness vice president turned informant', 'poster': 'https://m.media-amazon.com/images/M/MV5BMTc4MDIyMTM3NV5BMl5BanBnXkFtZTcwNDQ2Nzg2Mg@@._V1_SX300.jpg'}, {'name': 'Swordfish', 'plot': 'A covert counterterrorist unit called Black Cell led by Gabriel Shear wants the money to help finance their war against international terrorism but its all locked away Gabriel brings in convicted hacker Stanley Jobson to help him', 'poster': 'https://m.media-amazon.com/images/M/MV5BNzk5ZmQxMWYtM2QyNi00MTY3LTlmNjItYjUwODY3Y2YwOTIwXkEyXkFqcGdeQXVyNDk3NzU2MTQ@._V1_SX300.jpg'}, {'name': 'Inglourious Basterds', 'plot': 'In Nazioccupied France during World War II a plan to assassinate Nazi leaders by a group of Jewish US soldiers coincides with a theatre owners vengeful plans for the same', 'poster': 'https://m.media-amazon.com/images/M/MV5BOTJiNDEzOWYtMTVjOC00ZjlmLWE0NGMtZmE1OWVmZDQ2OWJhXkEyXkFqcGdeQXVyNTIzOTk5ODM@._V1_SX300.jpg'}, {'name': 'Rounders', 'plot': 'A young reformed gambler must return to playing big stakes poker to help a friend pay off loan sharks while balancing his relationship with his girlfriend and his commitments to law school', 'poster': 'https://m.media-amazon.com/images/M/MV5BMzViMmMxMzItYmYyYi00NGU3LWI2MDMtNjcwOWFmZTZkOTcwXkEyXkFqcGdeQXVyNDkzNTM2ODg@._V1_SX300.jpg'}, {'name': 'Point Blank', 'plot': 'An ER nurse and a career criminal are forced into an unlikely partnership in taking down a ring of corrupt cops threatening the lives of both their families', 'poster': 'https://m.media-amazon.com/images/M/MV5BYzUxOTg2MzAtOTY3Yi00NDVhLTk4OWItNjFjZmZlMWI2MjdlXkEyXkFqcGdeQXVyNjc1NTYyMjg@._V1_SX300.jpg'}, {'name': 'Mona Lisa Smile', 'plot': 'A freethinking art professor teaches conservative 1950s Wellesley girls to question their traditional social roles', 'poster': 'https://m.media-amazon.com/images/M/MV5BMTI0NjEwNDgwOV5BMl5BanBnXkFtZTYwOTI1NTA3._V1_SX300.jpg'}, {'name': 'Invictus', 'plot': 'Nelson Mandela in his first term as President of South Africa initiates a unique venture to unite the Apartheidtorn land enlist the national rugby team on a mission to win the 1995 Rugby World Cup', 'poster': 'https://m.media-amazon.com/images/M/MV5BMjAyMzExMDM1N15BMl5BanBnXkFtZTcwNTcyMTQ5Mg@@._V1_SX300.jpg'}, {'name': 'The Peacemaker', 'plot': 'A US Army colonel and a civilian woman supervising him must track down stolen Russian nuclear weapons before theyre used by terrorists', 'poster': 'https://m.media-amazon.com/images/M/MV5BMjQ0OTNjOTMtYWU1MC00MWQwLTllMmMtNWZmYmE3NDY0ZTgxXkEyXkFqcGdeQXVyMTE2OTg4Mjg@._V1_SX300.jpg'}, {'name': 'Trash', 'plot': 'Set in Brazil three kids who make a discovery in a garbage dump soon find themselves running from the cops and trying to right a terrible wrong', 'poster': 'https://m.media-amazon.com/images/M/MV5BMTEyNDY2Njc1NzheQTJeQWpwZ15BbWU4MDc1NzY2NjYx._V1_SX300.jpg'}, {'name': 'Layer Cake', 'plot': 'A successful cocaine dealer gets two tough assignments from his boss on the eve of his planned early retirement', 'poster': 'https://m.media-amazon.com/images/M/MV5BMTI5MTE1OTAzOV5BMl5BanBnXkFtZTcwNDc2OTgyMQ@@._V1_SX300.jpg'}, {'name': 'The Brothers Grimm', 'plot': 'Will and Jake Grimm are traveling conartists who encounter a genuine fairytale curse which requires true courage instead of their usual bogus exorcisms', 'poster': 'https://m.media-amazon.com/images/M/MV5BYzZiNGUxZmUtYjc0ZC00YzkxLWI2MWMtNDc0MWFiNjc5NGRkXkEyXkFqcGdeQXVyNTIzOTk5ODM@._V1_SX300.jpg'}]

    
    ###### COLLECT RELEVANT AMAZON MOVIES ######

    listOfMoviesOnAmazon = getMoviesFromAmazon(movieName)


    factFileAmazon = []

    for movieOnAmazon in listOfMoviesOnAmazon:
        factFile = getInfoAboutMovie(movieOnAmazon)
        newEntry = factFile
        factFileAmazon.append(newEntry)

    postersAmazon = [element.get('poster') for element in factFileAmazon]


    factFileAmazon = [{'name': 'Wild Card', 'plot': 'When a Las Vegas bodyguard with lethal skills and a gambling problem gets in trouble with the mob he has one last playand its all or nothing', 'poster': 'https://m.media-amazon.com/images/M/MV5BMjAyNjkyOTgzNF5BMl5BanBnXkFtZTgwMTk0MDc2MzE@._V1_SX300.jpg'}, {'name': 'The Rainmaker', 'plot': 'An underdog lawyer takes on a fraudulent insurance company', 'poster': 'https://m.media-amazon.com/images/M/MV5BMjdlMjI2ZjgtN2ViOS00ZmI0LWE0ZTMtZjg1ZjczYWYzOGZjL2ltYWdlL2ltYWdlXkEyXkFqcGdeQXVyNjc1NTYyMjg@._V1_SX300.jpg'}, {'name': 'Bound', 'plot': 'Tough excon Corky and her lover Violet concoct a scheme to steal millions of stashed mob money and pin the blame on Violets crooked boyfriend', 'poster': 'https://m.media-amazon.com/images/M/MV5BNjcwN2RhYWYtOWY1NC00M2JkLTllYWItYzZhOTg4NjZmMDcwXkEyXkFqcGdeQXVyMTQxNzMzNDI@._V1_SX300.jpg'}, {'name': 'Man on a Ledge', 'plot': 'As a police psychologist works to talk down an excon who is threatening to jump from a Manhattan hotel rooftop the biggest diamond heist ever committed is in motion', 'poster': 'https://m.media-amazon.com/images/M/MV5BMTc5MTE4MzY2N15BMl5BanBnXkFtZTcwNjMwNDc3Ng@@._V1_SX300.jpg'}, {'name': 'Dick Tracy', 'plot': 'The comic strip detective finds his life vastly complicated when Breathless Mahoney makes advances towards him while he is trying to battle Big Boy Caprices united mob', 'poster': 'https://m.media-amazon.com/images/M/MV5BMzA5MDg5ZDAtOWE1YS00Nzg2LTk5NzUtMDY3ZDZlN2U2M2ZlXkEyXkFqcGdeQXVyNjUwNzk3NDc@._V1_SX300.jpg'}, {'name': 'Bandits', 'plot': 'Two bank robbers fall in love with the girl theyve kidnapped', 'poster': 'https://m.media-amazon.com/images/M/MV5BMTkyMzA3OTI3NV5BMl5BanBnXkFtZTYwMjU0ODM3._V1_SX300.jpg'}, {'name': 'Escape from Alcatraz', 'plot': 'Alcatraz is the most secure prison of its time It is believed that no one can ever escape from it until three daring men make a possible successful attempt at escaping from one of the most infamous prisons in the world', 'poster': 'https://m.media-amazon.com/images/M/MV5BNDQ3MzNjMDItZjE0ZS00ZTYxLTgxNTAtM2I4YjZjNWFjYjJlL2ltYWdlXkEyXkFqcGdeQXVyNTAyODkwOQ@@._V1_SX300.jpg'}, {'name': 'Bully', 'plot': 'A pack of naïve teenagers conspire to murder a mutual friend whose aggressive demeanor has proved too much', 'poster': 'https://m.media-amazon.com/images/M/MV5BMjE2OTYwMzQzNl5BMl5BanBnXkFtZTcwNDM1MjMzMQ@@._V1_SX300.jpg'}, {'name': 'Point Blank', 'plot': 'An ER nurse and a career criminal are forced into an unlikely partnership in taking down a ring of corrupt cops threatening the lives of both their families', 'poster': 'https://m.media-amazon.com/images/M/MV5BYzUxOTg2MzAtOTY3Yi00NDVhLTk4OWItNjFjZmZlMWI2MjdlXkEyXkFqcGdeQXVyNjc1NTYyMjg@._V1_SX300.jpg'}, {'name': 'The Brothers Grimm', 'plot': 'Will and Jake Grimm are traveling conartists who encounter a genuine fairytale curse which requires true courage instead of their usual bogus exorcisms', 'poster': 'https://m.media-amazon.com/images/M/MV5BYzZiNGUxZmUtYjc0ZC00YzkxLWI2MWMtNDc0MWFiNjc5NGRkXkEyXkFqcGdeQXVyNTIzOTk5ODM@._V1_SX300.jpg'}, {'name': 'City of Ghosts', 'plot': 'A con man Matt Dillon travels to Cambodia also on the run from law enforcement in the US to collect his share in an insurance scam but discovers more than he bargained for', 'poster': 'https://m.media-amazon.com/images/M/MV5BMTE5ODk5OTc3Ml5BMl5BanBnXkFtZTcwMzcxMjAwMQ@@._V1_SX300.jpg'}, {'name': 'Out of the Dark', 'plot': 'A couple and their daughter move to Colombia to take over a family manufacturing plant only to realize their new home is haunted', 'poster': 'https://m.media-amazon.com/images/M/MV5BMzY5MDE1ODE2N15BMl5BanBnXkFtZTgwMDY5NTc5MzE@._V1_SX300.jpg'}, {'name': 'Dutch Kills', 'plot': 'A desperate excon is forced to gather his old crew for one last job to pay off his sisters debt to a dangerous local criminal', 'poster': 'https://m.media-amazon.com/images/M/MV5BMjAzNTA1NzQ5MV5BMl5BanBnXkFtZTgwOTUxODgwNzE@._V1_SX300.jpg'}, {'name': 'Madeas Witness Protection', 'plot': 'A Wall Street investment banker who has been set up as the linchpin of his companys mobbacked Ponzi scheme is relocated with his family to Aunt Madeas southern home', 'poster': 'https://m.media-amazon.com/images/M/MV5BMjAzMjczMTU4Nl5BMl5BanBnXkFtZTcwMDk1MTE5Nw@@._V1_SX300.jpg'}, {'name': 'Chicago Overcoat', 'plot': 'The fates of an aging hitman and a washed up detective become entwined when one last job leads to one last chance to settle an old score', 'poster': 'https://m.media-amazon.com/images/M/MV5BYzQyYTgxODMtNzAyNy00NTFhLWI0YTktM2NjZDVlYjRmZTEzXkEyXkFqcGdeQXVyMzMzMDQ3MzY@._V1_SX300.jpg'}, {'name': 'The Maids Room', 'plot': 'THE MAIDS ROOM is a psychological thriller that explores the complex relationships between truth and justice hubris and power wealth and fear', 'poster': 'https://m.media-amazon.com/images/M/MV5BYTMwZTdhYzEtNjVhNi00NTVlLWE5ZWItNjM3Nzc1YTVlNjNhXkEyXkFqcGdeQXVyMTMxMTY0OTQ@._V1_SX300.jpg'}, {'name': 'Slow Burn', 'plot': 'A district attorney is involved in a 24hour showdown with a gang leader and is at the same time being manipulated by an attractive assistant district attorney and a cryptic stranger', 'poster': 'https://m.media-amazon.com/images/M/MV5BMjAxNDQ3NTg0MF5BMl5BanBnXkFtZTcwNTUxNzQ0MQ@@._V1_SX300.jpg'}, {'name': 'Shade', 'plot': 'A group of hustlers encounter The Dean and pull off a successful sting that results in their pursuit by a vengeful gangster', 'poster': 'https://m.media-amazon.com/images/M/MV5BOWFmMDYxNjgtYTYyNy00MGZiLTllOGYtM2FkYzkxZWNhZDhmXkEyXkFqcGdeQXVyNDk3NzU2MTQ@._V1_SX300.jpg'}, {'name': 'The Jerk', 'plot': 'A simpleminded sheltered country boy suddenly decides to leave his family home to experience life in the big city where his naivete is both his best friend and his worst enemy', 'poster': 'https://m.media-amazon.com/images/M/MV5BZDNmNThjMTMtNzVlZC00MzgyLWE3M2UtNGQ3ZTZmNjM3YWI2XkEyXkFqcGdeQXVyMTQxNzMzNDI@._V1_SX300.jpg'}, {'name': 'Checkmate', 'plot': 'Don Corey and Jed Sills operate Checkmate Inc a very high priced detective agency in San Francisco Helping them protect the lives of their clients is British criminologist once an Oxford professor Carl Hyatt', 'poster': 'https://m.media-amazon.com/images/M/MV5BNTQyMjEzODE2OF5BMl5BanBnXkFtZTgwMzU2MDE4NjE@._V1_SX300.jpg'}, {'name': 'Legends of the Fall', 'plot': 'In the early 1900s three brothers and their father living in the remote wilderness of Montana are affected by betrayal history love nature and war', 'poster': 'https://m.media-amazon.com/images/M/MV5BMTYwMjYxNTAyN15BMl5BanBnXkFtZTgwMTc3MjkyMTE@._V1_SX300.jpg'}, {'name': 'Star Trek III The Search for Spock', 'plot': 'Admiral Kirk and his bridge crew risk their careers stealing the decommissioned USS Enterprise to return to the restricted Genesis Planet to recover Spocks body', 'poster': 'https://m.media-amazon.com/images/M/MV5BMTliZGVjZmMtNzEzMy00MzVhLWFhYjYtNDhlYmViNGNiMGFlXkEyXkFqcGdeQXVyMTQxNzMzNDI@._V1_SX300.jpg'}]
    postersAmazon = ['https://m.media-amazon.com/images/M/MV5BMjAyNjkyOTgzNF5BMl5BanBnXkFtZTgwMTk0MDc2MzE@._V1_SX300.jpg', 'https://m.media-amazon.com/images/M/MV5BMjdlMjI2ZjgtN2ViOS00ZmI0LWE0ZTMtZjg1ZjczYWYzOGZjL2ltYWdlL2ltYWdlXkEyXkFqcGdeQXVyNjc1NTYyMjg@._V1_SX300.jpg', 'https://m.media-amazon.com/images/M/MV5BNjcwN2RhYWYtOWY1NC00M2JkLTllYWItYzZhOTg4NjZmMDcwXkEyXkFqcGdeQXVyMTQxNzMzNDI@._V1_SX300.jpg', 'https://m.media-amazon.com/images/M/MV5BMTc5MTE4MzY2N15BMl5BanBnXkFtZTcwNjMwNDc3Ng@@._V1_SX300.jpg', 'https://m.media-amazon.com/images/M/MV5BMzA5MDg5ZDAtOWE1YS00Nzg2LTk5NzUtMDY3ZDZlN2U2M2ZlXkEyXkFqcGdeQXVyNjUwNzk3NDc@._V1_SX300.jpg', 'https://m.media-amazon.com/images/M/MV5BMTkyMzA3OTI3NV5BMl5BanBnXkFtZTYwMjU0ODM3._V1_SX300.jpg', 'https://m.media-amazon.com/images/M/MV5BNDQ3MzNjMDItZjE0ZS00ZTYxLTgxNTAtM2I4YjZjNWFjYjJlL2ltYWdlXkEyXkFqcGdeQXVyNTAyODkwOQ@@._V1_SX300.jpg', 'https://m.media-amazon.com/images/M/MV5BMjE2OTYwMzQzNl5BMl5BanBnXkFtZTcwNDM1MjMzMQ@@._V1_SX300.jpg', 'https://m.media-amazon.com/images/M/MV5BYzUxOTg2MzAtOTY3Yi00NDVhLTk4OWItNjFjZmZlMWI2MjdlXkEyXkFqcGdeQXVyNjc1NTYyMjg@._V1_SX300.jpg', 'https://m.media-amazon.com/images/M/MV5BYzZiNGUxZmUtYjc0ZC00YzkxLWI2MWMtNDc0MWFiNjc5NGRkXkEyXkFqcGdeQXVyNTIzOTk5ODM@._V1_SX300.jpg', 'https://m.media-amazon.com/images/M/MV5BMTE5ODk5OTc3Ml5BMl5BanBnXkFtZTcwMzcxMjAwMQ@@._V1_SX300.jpg', 'https://m.media-amazon.com/images/M/MV5BMzY5MDE1ODE2N15BMl5BanBnXkFtZTgwMDY5NTc5MzE@._V1_SX300.jpg', 'https://m.media-amazon.com/images/M/MV5BMjAzNTA1NzQ5MV5BMl5BanBnXkFtZTgwOTUxODgwNzE@._V1_SX300.jpg', 'https://m.media-amazon.com/images/M/MV5BMjAzMjczMTU4Nl5BMl5BanBnXkFtZTcwMDk1MTE5Nw@@._V1_SX300.jpg', 'https://m.media-amazon.com/images/M/MV5BYzQyYTgxODMtNzAyNy00NTFhLWI0YTktM2NjZDVlYjRmZTEzXkEyXkFqcGdeQXVyMzMzMDQ3MzY@._V1_SX300.jpg', 'https://m.media-amazon.com/images/M/MV5BYTMwZTdhYzEtNjVhNi00NTVlLWE5ZWItNjM3Nzc1YTVlNjNhXkEyXkFqcGdeQXVyMTMxMTY0OTQ@._V1_SX300.jpg', 'https://m.media-amazon.com/images/M/MV5BMjAxNDQ3NTg0MF5BMl5BanBnXkFtZTcwNTUxNzQ0MQ@@._V1_SX300.jpg', 'https://m.media-amazon.com/images/M/MV5BOWFmMDYxNjgtYTYyNy00MGZiLTllOGYtM2FkYzkxZWNhZDhmXkEyXkFqcGdeQXVyNDk3NzU2MTQ@._V1_SX300.jpg', 'https://m.media-amazon.com/images/M/MV5BZDNmNThjMTMtNzVlZC00MzgyLWE3M2UtNGQ3ZTZmNjM3YWI2XkEyXkFqcGdeQXVyMTQxNzMzNDI@._V1_SX300.jpg', 'https://m.media-amazon.com/images/M/MV5BNTQyMjEzODE2OF5BMl5BanBnXkFtZTgwMzU2MDE4NjE@._V1_SX300.jpg', 'https://m.media-amazon.com/images/M/MV5BMTYwMjYxNTAyN15BMl5BanBnXkFtZTgwMTc3MjkyMTE@._V1_SX300.jpg', 'https://m.media-amazon.com/images/M/MV5BMTliZGVjZmMtNzEzMy00MzVhLWFhYjYtNDhlYmViNGNiMGFlXkEyXkFqcGdeQXVyMTQxNzMzNDI@._V1_SX300.jpg']
    
    
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


