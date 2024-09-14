import csv, requests
from bs4 import BeautifulSoup
from pymongo import MongoClient 
import argparse


client = MongoClient('mongodb://localhost:27017')
db = client['movie_tracker']
movies_collection = db['movies']

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
                              'comment': None
                              }
                if not movies_collection.find_one({"title": movie_data['title']}):
                    movies_collection.insert_one(movie_data)
                    print(f"Inserted: {movie_data['title']}")
                else: 
                    print(f"Movie '{movie_data['title']}' already exists in the database.")
else:
    print("Failed to fetch the webpage.")





