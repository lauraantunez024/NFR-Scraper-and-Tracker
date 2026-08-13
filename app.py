from flask import Flask, jsonify, request
from pymongo import MongoClient
from flask_cors import CORS
from dotenv import load_dotenv
from pymongo.server_api import ServerApi
import os
from bson.objectid import ObjectId
from bson.errors import InvalidId


app = Flask(__name__)
CORS(app) 
load_dotenv()
MONGO_PASSWORD = os.getenv('MONGO')
ADDRESS = os.getenv('ADDRESS')
uri = os.getenv('MONGODB_URI')
client = MongoClient(uri, server_api=ServerApi('1'))
db = client['movie_tracker']
movies_collection = db['movies']
ITEMS_PER_PAGE = 24



@app.route("/", methods=["GET", "HEAD"])
def health():
    return jsonify({"status": "ok"}), 200

@app.route('/api/movies', methods=['GET'])
def getMovies():
    limit = min(int(request.args.get('limit', ITEMS_PER_PAGE)), 50)
    cursor = request.args.get('cursor')
    
    query = {}
    
    if cursor:
        try:
            query['_id'] = {'$gt': ObjectId(cursor)}
        except InvalidId:
            return({'error': 'Invalid cursor'}), 400
        
    docs = list(movies_collection.find(query.sort('_id', 1).limit(limit + 1)))
    
    has_more = len(docs) > limit
    page = docs[:limit]
    
    movies = []
    for doc in page:
        doc_id = str(doc['_id'])
        doc.pop('_id')
        movies.append(doc)
    next_cursor = str(page[-1]['_id']) if has_more else None 
    
    movies = list(movies_collection.find({}, {'_id':0}))
    return jsonify({
                    'movies': movies,
                    'nextCursor': next_cursor,
                    'hasMore': has_more})

@app.route('/api/movies/watched', methods=['POST'])
def markAsWatched():
    title = request.json.get('title')
    movies_collection.update_one({"title": title}, {"$set": {"watched": True}})
    return jsonify({"message": f"Marked '{title}' as watched"})

@app.route('/api/movies/rate', methods=['POST'])
def rate_movie():
    title = request.json.get('title')
    rating = request.json.get('rating')
    comments = request.json.get('comments')
    movies_collection.update_one({"title": title}, {"$set": {"rating": rating, "comments": comments}})
    return jsonify({"message": f"Updated '{title}' with rating and comments"})

if __name__ == '__main__':
    app.run(debug=True)