from flask import Flask, jsonify, request
from pymongo import MongoClient
from flask_cors import CORS


app = Flask(__name__)
CORS(app) 

client = MongoClient('mongodb://localhost:27017')
db = client['movie_tracker']
movies_collection = db['movies']


@app.route('/api/movies', methods=['GET'])
def getMovies():
    movies = list(movies_collection.find({}, {'_id':0}))
    return jsonify(movies)

@app.route('/movies/watched', methods=['POST'])
def markAsWatched():
    title = request.json.get('title')
    movies_collection.update_one({"title": title}, {"$set": {"watched": True}})
    return jsonify({"message": f"Marked '{title}' as watched"})

@app.route('/movies/rate', methods=['POST'])
def rate_movie():
    title = request.json.get('title')
    rating = request.json.get('rating')
    comments = request.json.get('comments')
    movies_collection.update_one({"title": title}, {"$set": {"rating": rating, "comments": comments}})
    return jsonify({"message": f"Updated '{title}' with rating and comments"})

if __name__ == '__main__':
    app.run(debug=True)