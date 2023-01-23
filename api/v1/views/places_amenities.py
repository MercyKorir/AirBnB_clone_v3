#!/usr/bin/python3
"""Handles all default RESTful API actions"""
from models import storage
from flask import jsonify, request
from api.v1.views import app_views
from models.place import Place
from models.amenity import Amenity
from models.state import State
from models.city import City


@app_views.route("/places/<place_id>/amenities", methods=["GET"])
def get_amenities_by_place(place_id):
    place = storage.get(Place, place_id)
    if not place:
        return jsonify({"error": "Not found"}), 404
    amenities = []
    for amenity in place.amenities:
        amenities.append(amenity.to_dict())
    return jsonify(amenities)


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 methods=["DELETE"])
def delete_amenity_by_place(place_id, amenity_id):
    place = storage.get(Place, place_id)
    if not place:
        return jsonify({"error": "Not found"}), 404
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        return jsonify({"error": "Not found"}), 404
    if amenity not in place.amenities:
        return jsonify({"error": "Not found"}), 404
    place.amenities.remove(amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route("/places/<place_id>/amenities/<amenity_id>", methods=["POST"])
def post_amenity_by_place(place_id, amenity_id):
    place = storage.get(Place, place_id)
    if not place:
        return jsonify({"error": "Not found"}), 404
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        return jsonify({"error": "Not found"}), 404
    if amenity in place.amenities:
        return jsonify(amenity.to_dict()), 200
    place.amenities.append(amenity)
    storage.save()
    return jsonify(amenity.to_dict()), 201
