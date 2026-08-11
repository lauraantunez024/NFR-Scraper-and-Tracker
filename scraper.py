import csv, requests
from bs4 import BeautifulSoup
from flask import Blueprint, jsonify, request
from pymongo import MongoClient 
from pymongo.server_api import ServerApi
import argparse
import math
import random
from dotenv import load_dotenv
import os

# Set up MongoDB Connection 
load_dotenv()
OMDB_API_KEY = os.getenv('OMDB_API_KEY')
RADARR_API_KEY = os.getenv('RADARR_API_KEY')
ADDRESS = os.getenv('ADDRESS')
MONGO_PASSWORD = os.getenv('MONGO')
uri = f"mongodb+srv://admin:{MONGO_PASSWORD}@nfr.8fo4vg6.mongodb.net/?appName=NFR"
MONGO_URI=os.getenv('MONGODB_URI')
ATLAS_URI=os.getenv('ATLAS_URI')
client = MongoClient(ATLAS_URI, server_api=ServerApi('1'))
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
db = client['movie_tracker']
movies_collection = db['movies']
url = f"http://www.omdbapi.com/?"
# Fetch movies from OMDB

def fetchMovies(title): 
    payload = {
        't': title,
        # 'y': year,
        'apikey': OMDB_API_KEY
    }
    response = requests.get(url, params=payload)
    if response.status_code == 200:
        return response.json()
    else:
        print(response.json())
    
    
# Scrape Website and add data to database
def scrapeMovies():
    url =  'https://www.loc.gov/programs/national-film-preservation-board/film-registry/complete-national-film-registry-listing/'
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        table_body = soup.find('tbody')
        if table_body:
            rows = table_body.find_all('tr')
            for row in rows:
                film_name = row.find('th')
                columns = row.find_all('td')
                if film_name and len(columns) >= 1:
                    year = columns[0].text.strip()
                    yearInducted = columns[1].text.strip()
                    title = film_name.text.strip() 
                    movie_data = { 
                                'title': title,
                                'year': year,
                                'yearInducted': yearInducted,
                                'watched': False,
                                'rating': None,
                                'comments': None,
                                'genre': None,
                                'country': None,
                                'imDB_Rating': None,
                                'runtime': None,
                                'imDB_ID': None,
                                'plot': None,
                                }
                    if not movies_collection.find_one({"title": movie_data['title']}):
                        movies_collection.insert_one(movie_data)
                        
                        print(f"Inserted: {movie_data['title']}")
                    else: 
                        print(f"Movie '{movie_data['title']}' already exists in the database.")
                    if not movies_collection.find_one({"yearInducted": movie_data['yearInducted']}):
                        movies_collection.update_one({"yearInducted": movie_data['yearInducted']}, {"$set": {"yearInducted": movie_data['yearInducted']}})
                        print(f"Inserted: {movie_data['yearInducted']}")
                    else:
                        print(f"Year '{movie_data['yearInducted']}' already exists in the database.")
    else:
            print("Failed to fetch the webpage.")
        
def addMovieDetails(title):
    movie_title = movies_collection.find_one({"title": title})
    searchable_title = movie_title['title'].replace(':', '%3A').replace(' ', '+')
    omdb_data = fetchMovies(searchable_title)
    if omdb_data and omdb_data.get('Response') == 'True':
        movies_collection.update_one(
            {"title": title}, 
            {"$set": {"genre": omdb_data.get('Genre'), "country": omdb_data.get('Country'), "plot": omdb_data.get('Plot'), "imDB_Rating": omdb_data.get('imdbRating'), "runtime": omdb_data.get('Runtime'), "imDB_ID": omdb_data.get('imdbID')}})
        # print(f"Movie details were added for {title}")
    else:
        print(f" somethings wrong for {title} ({movie_title['year']})=======> {omdb_data}")
            
            

# Mark movies as watched and rate them from CLI

def watched_movie(title):
    movie = movies_collection.find_one({"title": title})
    if movie:
        movies_collection.update_one({"title": title}, {"$set": {"watched": True}})
        print(f"Marked '{title}' as watched.")
    else: 
        print(f"Movie '{title}' not found.")

def ratings_and_comments(title, rating, comments):
    movie = movies_collection.find_one({"title": title})
    if movie:
        movies_collection.update_one(
            {"title": title},
            {"$set": {"rating": rating, "comments": comments}}
        )
        print(f"Thoughts and rating have been noted for '{title}'")
    else: 
        print(f"You might've seen that for no reason because it's not in here.... or you spelled it wrong.")
        
# pick a random movie for me to watch that i haven't already. Either totally random or by year

def add_movie_to_radarr(title, year):
    movie = movies_collection.find_one({"title": title})
    movie_id = movie['imDB_ID']

    RADARR_MOVIE_URL = f'{ADDRESS}/api/v3/movie?apikey={RADARR_API_KEY}'
    RADARR_LOOKUP_URL = f"{ADDRESS}/api/v3/movie/lookup/imdb?imdbId={movie_id}&apikey={RADARR_API_KEY}"
    
    headers = {'X-Api-Key': RADARR_API_KEY}

    lookup_response = requests.get(RADARR_LOOKUP_URL, headers=headers)
    
    # Payload for Radarr API to search for a movie
    payload = lookup_response.json()
    
    headers = {'X-Api-Key': RADARR_API_KEY}
    
    payload["rootFolderPath"] = f"../Volumes/Laura/Media/Movies"  # Change this to your actual media directory
    payload["path"] = f"../Volumes/Laura/Media/Movies/{movie['title']} {movie['year']}"  # Change this to your actual media directory
    payload["monitored"] = True 
    payload["qualityProfileId"] = 3
    payload["tags"] = "national-film-registry"
    payload['addOptions'] = {
    'searchForMovie': True,
    "addMethod": "manual",
    "ignoreEpisodesWithFiles": False,
    "ignoreEpisodesWithoutFiles": False,
    "monitor": "movieOnly"
    }

    
    response = requests.post(RADARR_MOVIE_URL, json=payload, headers=headers)
    
    if response.status_code == 201:
        print(f"'{title}' ({year}) has been added to Radarr and is being searched for.")
        # keeping below for debugging
        # print(f"{response.content} ======================= {payload}")

    elif response.status_code == 400:
        print(f"Movie '{title}' already exists in Radarr or could not be added.")
    else:
        print(f"{response.content} ======================= {payload}")
        
def pickRandomUnwatched() :
    unwatched_movies = list(movies_collection.find({"watched": False}))
    if not unwatched_movies:
        print("All movies have been seen.")
        return
    random_movie = random.choice(unwatched_movies)
    title = random_movie['title']
    year = random_movie['year']
    
    add_movie_to_radarr(title, year)
    print(f"This is your random film: '{random_movie['title']}' ({random_movie['year']})")
        
        
def pickByYears(yearx, yeary):
    # Makes the years chosen inclusive 
    if yearx > yeary:
        yearx = str(int(yearx) + 1)
        yeary = str(int(yeary) - 1)
    else: 
        yeary = str(int(yeary) + 1)
        yearx = str(int(yearx) - 1)
    moviesInRange = list(movies_collection.find({ "$and" : [ { "year": { "$gt" : yearx }}, { "year" : { "$lt" : yeary }}, {"watched": False}] }))
    if not moviesInRange:
        print("There are no movies between those time ranges")
        return
    random_movie = random.choice(moviesInRange)
    print(f"This a random movie between {yearx} and {yeary} ----> {random_movie['title']} ({random_movie['year']})")
    # add_movie_to_radarr(random_movie['title'], random_movie['year'])

          
def main():
    parser = argparse.ArgumentParser(description="Track, rate and comment the movies from the national film registry")
    parser.add_argument('-s', '--scrape', action='store_true', help='Scrape any freshly added movies')
    parser.add_argument('-w', '--watched', type=str, help='Usage: --watched "Movie Title"')
    parser.add_argument('-r', '--rate', type=str, nargs=3, metavar=('TITLE', 'RATING', 'COMMENTS'), help='Usage: --rate "Movie Title" 8 "Thoughts, critiques, etc"')
    parser.add_argument('-random', '--pick_random', action='store_true', help='pick a random unwatched movie')
    parser.add_argument('-y', '--pick_by_year', type=int, nargs=2, metavar=('yearX', 'yearY'), help='Usage: --pick_by_year 1990 2010')
    parser.add_argument('-d', '--add_details', action='store_true')
    parser.add_argument('-u', '--update_details', help='Usage: --update_details "Movie Title"')
    args = parser.parse_args()
    
    if args.scrape:
        scrapeMovies()
    
    if args.watched:
        watched_movie(args.watched)
        
    if args.rate:
        title, rating, comments = args.rate
        ratings_and_comments(title, int(rating), comments)
        
    if args.pick_random:
        pickRandomUnwatched()
    
    if args.pick_by_year:
        yearx, yeary = args.pick_by_year
        pickByYears(yearx, yeary)
        
    if args.add_details:
        movies = movies_collection.find()
        for movie in movies:
            addMovieDetails(movie['title'])
    
if __name__ == '__main__':
    main()
        




