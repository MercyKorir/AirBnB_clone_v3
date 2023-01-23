#!/usr/bin/python3
"""returns JSON status ok"""
from flask import jsonify, request
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route("/status", methods=['GET'])
def status():
    if request.method == 'GET':
        return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'])
def stats():
    stats = {}
    PLURALS = {
            Amenity: "amenities",
            City: "cities",
            Place: "places",
            Review: "reviews",
            State: "states",
            User: "users"
            }
    for key, value in PLURALS.items():
        stats[value] = storage.count(key)
    return jsonify(stats)
