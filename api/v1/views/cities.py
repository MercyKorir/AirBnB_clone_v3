#!/usr/bin/python3
"""Handles all default RESTful API actions"""
from models import storage
from models.state import State
from models.city import City
from flask import jsonify, request
from api.v1.views import app_views


@app_views.route("/cities/<city_id>", methods=["GET"])
def get_city(city_id):
    city = storage.get(City, city_id)
    if not city:
        return jsonify({"error": "Not found"}), 404
    return jsonify(city.to_dict())


@app_views.route("states/<state_id>/cities", methods=["GET"])
def get_cities_of_state(state_id):
    state = storage.get(State, state_id)
    if state is None:
        return jsonify({"error": "Not found"}), 404
    cities = [city.to_dict() for city in state.cities]
    return jsonify(cities)


@app_views.route("/cities/<city_id>", methods=["DELETE"])
def delete_city(city_id):
    city = storage.get(City, city_id)
    if not city:
        return jsonify({"error": "Not found"}), 404
    storage.delete(city)
    storage.save()
    return jsonify({}), 200


@app_views.route("/states/<state_id>/cities", methods=["POST"])
def create_city(state_id):
    state = storage.get(State, state_id)
    if not state:
        return jsonify({"error": "Not found"}), 404
    data = request.get_json()
    if not data:
        return jsonify({"error": "Not a JSON"}), 400
    if "name" not in data:
        return jsonify({"error": "Missing name"}), 400
    city = City(name=data["name"], state_id=state_id)
    city.save()
    return jsonify(city.to_dict()), 201


@app_views.route("/cities/<city_id>", methods=["PUT"])
def update_city(city_id):
    city = storage.get(City, city_id)
    if not city:
        return jsonify({"error": "Not found"}), 404
    data = request.get_json()
    if not data:
        return jsonify({"error": "Not a JSON"}), 400
    for key, value in data.items():
        if key not in ["id", "state_id", "created_at", "updated_at"]:
            setattr(city, key, value)
    city.save()
    return jsonify(city.to_dict()), 200
