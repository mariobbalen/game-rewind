"""
    GET http://127.0.0.1:5000/games?q=<game_name>
    POST http://127.0.0.1:5000/reviews
    GET http://127.0.0.1:5000/reviews
    DELETE http://127.0.0.1:5000/reviews/<game_id>
"""

import os

from flask import Flask, jsonify, request
from pymongo import MongoClient

from util import get_access_token, search_games

app = Flask(__name__)

# busca a uri do mongo do env, mas se não exisitr, busca pela default
MONGO_URI = os.environ.get("MONGO_URI", "mongodb://localhost:27017")
mongo_client = MongoClient(MONGO_URI)
reviews_collection = mongo_client["game_rewind"]["reviews"]

# ajusta problema de CORS que acontecia ao se comunicar com o front
@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, DELETE, OPTIONS"
    return response

# manda as infos do CORS para dizer que pode mandar a requisição real, pois o CORS deu o ok
@app.route("/reviews", methods=["OPTIONS"])
@app.route("/reviews/<int:game_id>", methods=["OPTIONS"])
def reviews_preflight(game_id=None):
    return "", 204


_access_token = None

# função para deixar o token salvo, fazendo com que n precise pedir toda vez (salva em uma variável global)
def get_cached_token() -> str:
    global _access_token
    if _access_token is None:
        _access_token = get_access_token()
    return _access_token

# pega os jogos
@app.get("/games")
def games():
    query = request.args.get("q", "")
    if not query:
        return jsonify([])
    games = search_games(query, get_cached_token())
    return jsonify(games)

# busca as reviews
@app.get("/reviews")
def list_reviews():
    reviews = list(reviews_collection.find({}, {"_id": False}))
    return jsonify(reviews)

# cria ou atualiza um review
@app.post("/reviews")
def save_review():
    data = request.get_json()

    # faz as verificações de meia estrela
    rating = max(0.0, min(5.0, float(data.get("rating", 0))))
    rating = round(rating * 2) / 2 

    # cria o json que vai ser enviado
    review = {
        "game_id": data["game_id"],
        "name": data["name"],
        "cover_url": data.get("cover_url"),
        "played": bool(data.get("played", False)),
        "rating": rating,
        "review": data.get("review", ""),
    }

    reviews_collection.update_one(
        {"game_id": review["game_id"]}, {"$set": review}, upsert=True
    )
    return jsonify(review), 201

# apaga o review
@app.delete("/reviews/<int:game_id>")
def delete_review(game_id):
    reviews_collection.delete_one({"game_id": game_id})
    return "", 204


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
