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
import time

# Set up MongoDB Connection 
load_dotenv()
OMDB_API_KEY = os.getenv('OMDB_API_KEY')
TMDB_API_KEY = os.getenv('NEXT_PUBLIC_TMDB_API_KEY')
RADARR_API_KEY = os.getenv('RADARR_API_KEY')
ADDRESS = os.getenv('ADDRESS')
MONGO_PASSWORD = os.getenv('MONGO')
uri = f"mongodb+srv://admin:{MONGO_PASSWORD}@nfr.8fo4vg6.mongodb.net/?appName=NFR"
MONGO_URI=os.getenv('MONGODB_URI')
client = MongoClient(MONGO_URI, server_api=ServerApi('1'))
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
db = client['movie_tracker']
movies_collection = db['movies']
tmdbUrl = f"https://api.themoviedb.org/3"


    
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
                                'posterImage': None,
                                'LogoImage': None,
                                'tmdb_id': None,
                                'budget' : None,
                                
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
            
            
def tmdb_get(path, params=None):
    params = params or {}
    params["api_key"] = TMDB_API_KEY
    response = requests.get(f"{tmdbUrl}{path}", params=params, timeout=15)
    response.raise_for_status()
    return response.json()

def search_tmdb_movie(title, year):
    data = tmdb_get("search/movie", {
        "query": title,
        "year": year,
        "include_adult": "false"
    })
    results = data.get("results", [])
    if not results:
        return None
    return results[0]

def fetch_tmdb_images(tmdb_id):
    return tmdb_get(f"/movie/{tmdb_id}", {
        "append_to_response": "external_ids"
    })

def build_logo_url(images_data):
    logos = images_data.get("logos") or []
    if not logos:
        return None
    return f"https://image.tmdb.org/t/p/w200{logos[0]['file_path']}"

def build_poster_url(images_data, details_data):
    posters = images_data.get("posters") or []
    if posters:
        return f"https://image.tmdb.org/t/p/w500"
    poster_path = details_data.get("poster_path")
    if poster_path:
        return f"https://image.tmdb.org/t/p/w500{poster_path}"
    return None

def addTmdbDetails(title):
    movie = movies_collection.find_one({"title": title})
    if not movie:
        print(f"{title} movie not found")
        return
    if movie.get("tmdb_id"):
        print(f"Movie aleady enriched {title}")
        return
    try:
        search_result = search_tmdb_movie(movie["title"], movie["year"])
        if not search_result:
            print(f"No TMDB match for {title}")
            return
        
        tmdb_id = search_result["id"]
        details = fetch_tmdb_images(tmdb_id)
        
        images = fetch_tmdb_images(tmdb_id)
        genres = ", ".join(g["name"] for g in details.get("genres", []))
        countries = ", ".join(
            c["name"] for c in details.get("production_countries", [])
        )
        imdb_id = details.get("external_ids", {}).get("imdb_id")
        
        update = {
            "tmdb_id": tmdb_id,
            "plot": details.get("overview"),
            "runtime": f"{details.get('runtime')} min" if details.get("runtime") else None,
            "genre": genres or None,
            "country": countries or None,
            "imDB_Rating": details.get("vote_average"),
            "budget": details.get("budget"),
            "posterImage": build_poster_url(images, details),
            "LogoImage": build_logo_url(images)
        }
        
        movies_collection.update_one({"title": title}, {"$set": update})
        print(f"enriched ----> {title}")
    except Exception as e:
        print(f"Failed for {title}: {e}")
        
def enrich_all_tmdb():
    movies = movies_collection.find({"tmdb_id": None})
    for movie in movies:
        addTmdbDetails(movie["title"])

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
    parser.add_argument('-t', '--tmdb_details', help='Usage: --tmdb_details "imdb_id"')
    args = parser.parse_args()
    
    if args.scrape:
        scrapeMovies()
    
    if args.add_details:
        enrich_all_tmdb()
    
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
        
if __name__ == '__main__':
    main()
        




