"""REST endpoints for the Songs service."""

import json
import os
from pathlib import Path

from flask import jsonify, request
from pymongo import MongoClient
from pymongo.errors import PyMongoError

from . import app


def _database():
    host = os.environ.get("MONGODB_SERVICE", "localhost")
    if host == "mock":
        import mongomock

        client = mongomock.MongoClient()
    else:
        username = os.environ.get("MONGODB_USERNAME")
        password = os.environ.get("MONGODB_PASSWORD")
        port = os.environ.get("MONGODB_PORT", "27017")
        if username and password:
            from urllib.parse import quote_plus

            uri = f"mongodb://{quote_plus(username)}:{quote_plus(password)}@{host}:{port}"
        else:
            uri = f"mongodb://{host}:{port}"
        client = MongoClient(uri, serverSelectionTimeoutMS=3000)
    return client.songs.songs


collection = _database()
if collection.count_documents({}) == 0:
    seed = json.loads((Path(__file__).parent / "data" / "songs.json").read_text())
    collection.insert_many(seed)


def _public(song):
    if song is None:
        return None
    return {key: value for key, value in song.items() if key != "_id"}


@app.get("/health")
def health():
    try:
        collection.database.client.admin.command("ping")
    except PyMongoError:
        return jsonify(status="ERROR"), 503
    return jsonify(status="OK"), 200


@app.get("/count")
def count():
    return jsonify(length=collection.count_documents({})), 200


@app.get("/song")
def get_songs():
    return jsonify([_public(song) for song in collection.find().sort("id", 1)]), 200


@app.get("/song/<int:song_id>")
def get_song(song_id):
    song = _public(collection.find_one({"id": song_id}))
    if song is None:
        return jsonify(message="song not found"), 404
    return jsonify(song), 200


@app.post("/song")
def create_song():
    song = request.get_json(silent=True)
    if not isinstance(song, dict) or not isinstance(song.get("id"), int):
        return jsonify(message="song must contain an integer id"), 400
    if collection.find_one({"id": song["id"]}):
        return jsonify(Message=f"song with id {song['id']} already present"), 302
    collection.insert_one(song.copy())
    return jsonify(song), 201


@app.put("/song/<int:song_id>")
def update_song(song_id):
    song = request.get_json(silent=True)
    if not isinstance(song, dict):
        return jsonify(message="a JSON song is required"), 400
    song["id"] = song_id
    result = collection.replace_one({"id": song_id}, song)
    if result.matched_count == 0:
        return jsonify(message="song not found"), 404
    return jsonify(song), 200


@app.delete("/song/<int:song_id>")
def delete_song(song_id):
    result = collection.delete_one({"id": song_id})
    if result.deleted_count == 0:
        return jsonify(message="song not found"), 404
    return "", 204
