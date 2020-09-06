# Sudoku Scanner Solver

## Quick Links

**Youtube video of project demo:** https://youtu.be/VNiINQXK_7w 

## Directory Structure
```
|-static --> contains all the css and other files related to the visual part of website 
|-templates
  |- index.html --> the home page where the user can enter in a movie name 
  |- whereToWatch.html --> displays all the palces the current movie can be watched 
|-amazon_titles.csv --> list of all movies on amazon prime
|-findMovieToWatch.py --> contains the functions to find the movies on TV, Prime, and Netflix
|-main.py --> contains the functions that redirects the user to the right website and loads up index.html and whereToWatch.html
|-movie_dataset.csv --> this is the Movie Lens data set utilised to create the cosine similarity 
|-movie_recommender.py --> this is the function that applies cosine similarity to determine the similar movies
|-netflix_titles.csv --> list of all movies on netflix
```
## Project Information

The goal of this Python based project was to develop a system that can take a movie title and return similar movies available on TV, Amazon & Netflix. The application uses cosine similarity and the Movie Lens dataset to identify similar movies. These similar movies are then found by web scraping TV schedules via Beautiful Soup. Similar movies on Netflix & Amazon are extracted from the Kaggle datasets. The IMDB & OMDb APIs were then called to extract movie information to display to the user. 

## Technologies used
<ul>
  <li> Flask <\li>
  <li> Flask <\li>
</ul>
    

## Additional Information
All the datasets for this project were taken from kaggle.
