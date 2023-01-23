#!/usr/bin/python3
"""Handles all default RESTful API actions"""
from models import storage
from flask import jsonify, request
from api.v1.views import app_views
from models.user import User


@app_views.route("/users", methods=["GET"])
def get_users():
    users = storage.all(User)
    users = [user.to_dict() for user in users.values()]
    return jsonify(users)


@app_views.route("/users/<user_id>", methods=["GET"])
def get_user(user_id):
    user = storage.get(User, user_id)
    if not user:
        return jsonify({"error": "Not found"}), 404
    return jsonify(user.to_dict())


@app_views.route("/users/<user_id>", methods=["DELETE"])
def delete_user(user_id):
    user = storage.get(User, user_id)
    if not user:
        return jsonify({"error": "Not found"}), 404
    storage.delete(user)
    storage.save()
    return jsonify({}), 200


@app_views.route("/users", methods=["POST"])
def create_user():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Not a JSON"}), 400
    if "email" not in data:
        return jsonify({"error": "Missing email"}), 400
    if "password" not in data:
        return jsonify({"error": "Missing password"}), 400
    user = User(**data)
    storage.new(user)
    storage.save()
    return jsonify(user.to_dict()), 201


@app_views.route("/users/<user_id>", methods=["PUT"])
def update_user(user_id):
    user = storage.get(User, user_id)
    if not user:
        return jsonify({"error": "Not found"}), 404
    data = request.get_json()
    if not data:
        return jsonify({"error": "Not a JSON"}), 400
    for key, value in data.items():
        if key not in ["id", "created_at", "updated_at", "email"]:
            setattr(user, key, value)
    storage.save()
    return jsonify(user.to_dict()), 200
