import csv, requests
from bs4 import BeautifulSoup
from pymongo import MongoClient 
import argparse
import math
import random

# Set up MongoDB Connection 
client = MongoClient('mongodb://localhost:27017')
db = client['movie_tracker']
movies_collection = db['movies']

# Scrape Website and add data to database
def scrapeMovies():
    url =  'https://www.loc.gov/programs/national-film-preservation-board/film-registry/complete-national-film-registry-listing/'
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        films = []
        table_body = soup.find('tbody')
        if table_body:
            rows = table_body.find_all('tr')
            for row in rows:
                film_name = row.find('th')
                columns = row.find_all('td')
                if film_name and len(columns) >= 1:
                    year = columns[0].text.strip()
                    movie_data = { 
                                'title': film_name.text.strip(),
                                'year': year,
                                'watched': False,
                                'rating': None,
                                'comments': None
                                }
                    if not movies_collection.find_one({"title": movie_data['title']}):
                        movies_collection.insert_one(movie_data)
                        print(f"Inserted: {movie_data['title']}")
                    else: 
                        print(f"Movie '{movie_data['title']}' already exists in the database.")
    else:
        print("Failed to fetch the webpage.")



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
        
def pickRandomUnwatched():
    unwatched_movies = list(movies_collection.find({"watched": False}))
   
    if not unwatched_movies:
        print("No unwatched films found.")
        return
    
    random_movie = random.choice(unwatched_movies)
    print(f"This is your random film: '{random_movie['title']}' ({random_movie['year']})")
        
        
        
def main():
    parser = argparse.ArgumentParser(description="Track, rate and comment the movies from the national film registry")
    parser.add_argument('--scrape', action='store_true', help='Scrape any freshly added movies')
    parser.add_argument('--watched', type=str, help='Usage: --watched "Movie Title"')
    parser.add_argument('--rate', type=str, nargs=3, metavar=('TITLE', 'RATING', 'COMMENTS'), help='Usage: --rate "Movie Title" 8 "Thoughts, critiques, etc"')
    parser.add_argument('--pick_random', action='store_true', help='pick a random unwatched movie')
    
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
    
if __name__ == '__main__':
    main()
        




