#!/usr/bin/python3
"""Handles all default RESTful API actions"""
from models import storage
from flask import jsonify, request
from api.v1.views import app_views
from models.place import Place
from models.city import City
from models.user import User
from models.amenity import Amenity
from models.state import State
from sqlalchemy import and_


@app_views.route("/cities/<city_id>/places", methods=["GET"])
def get_city_places(city_id):
    city = storage.get(City, city_id)
    if not city:
        return jsonify({"error": "Not found"}), 404
    places = [place.to_dict() for place in city.places]
    return jsonify(places)


@app_views.route("/places/<place_id>", methods=["GET"])
def get_place(place_id):
    place = storage.get(Place, place_id)
    if not place:
        return jsonify({"error": "Not found"}), 404
    return jsonify(place.to_dict())


@app_views.route("/places/<place_id>", methods=["DELETE"])
def delete_place(place_id):
    place = storage.get(Place, place_id)
    if not place:
        return jsonify({"error": "Not found"}), 404
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route("/cities/<city_id>/places", methods=["POST"])
def create_place(city_id):
    city = storage.get(City, city_id)
    if not city:
        return jsonify({"error": "Not found"}), 404
    data = request.get_json()
    if not data:
        return jsonify({"error": "Not a JSON"}), 400
    if "user_id" not in data:
        return jsonify({"error": "Missing user_id"}), 400
    user = storage.get(User, data["user_id"])
    if not user:
        return jsonify({"error": "Not found"}), 404
    if "name" not in data:
        return jsonify({"error": "Missing name"}), 400
    place = Place(**data)
    place.city_id = city_id
    storage.new(place)
    storage.save()
    return jsonify(place.to_dict()), 201


@app_views.route("/places/<place_id>", methods=["PUT"])
def update_place(place_id):
    place = storage.get(Place, place_id)
    if not place:
        return jsonify({"error": "Not found"}), 404
    data = request.get_json()
    if not data:
        return jsonify({"error": "Not a JSON"}), 400
    for key, value in data.items():
        if key not in ["id", "created_at", "updated_at", "user_id", "city_id"]:
            setattr(place, key, value)
    storage.save()
    return jsonify(place.to_dict()), 200


@app_views.route("/places_search", methods=["POST"])
def places_search():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Not a JSON"}), 400
    states = data.get("states", [])
    cities = data.get("cities", [])
    amenities = data.get("amenities", [])
    if not states and not cities and not amenities:
        return jsonify([place.to_dict() for place in storage.all(Place)])
    query = storage._DBStorage__session.query(Place)
    if states:
        query = query.join(City, State).filter(State.id.in_(states))
    if cities:
        query = query.filter(Place.city_id.in_(cities))
    if amenities:
        query = query.filter(and_(Place.amenities.any(
                            Amenity.id.in_(amenities))))
    places = query.all()
    return jsonify([place.to_dict() for place in places])
