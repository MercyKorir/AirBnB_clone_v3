#!/usr/bin/python3
"""Handles all default RESTful API operations"""
from models import storage
from api.v1.views import app_views
from flask import jsonify, request
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route("/places/<place_id>/reviews", methods=["GET"])
def get_place_reviews(place_id):
    place = storage.get(Place, place_id)
    if not place:
        return jsonify({"error": "Not found"}), 404
    reviews = [review.to_dict() for review in place.reviews]
    return jsonify(reviews)


@app_views.route("/reviews/<review_id>", methods=["GET"])
def get_review(review_id):
    review = storage.get(Review, review_id)
    if not review:
        return jsonify({"error": "Not found"}), 404
    return jsonify(review.to_dict())


@app_views.route("/reviews/<review_id>", methods=["DELETE"])
def delete_review(review_id):
    review = storage.get(Review, review_id)
    if not review:
        return jsonify({"error": "Not found"}), 404
    storage.delete(review)
    storage.save()
    return jsonify({}), 200


@app_views.route("/places/<place_id>/reviews", methods=["POST"])
def create_review(place_id):
    place = storage.get(Place, place_id)
    if not place:
        return jsonify({"error": "Not found"}), 404
    data = request.get_json()
    if not data:
        return jsonify({"error": "Not a JSON"}), 400
    if "user_id" not in data:
        return jsonify({"error": "Missing user_id"}), 400
    user = storage.get(User, data["user_id"])
    if not user:
        return jsonify({"error": "Not found"}), 404
    if "text" not in data:
        return jsonify({"error": "Missing text"}), 400
    review = Review(**data)
    review.place_id = place_id
    review.save()
    return jsonify(review.to_dict()), 201


@app_views.route("/reviews/<review_id>", methods=["PUT"])
def update_review(review_id):
    review = storage.get(Review, review_id)
    if not review:
        return jsonify({"error": "Not found"}), 404
    data = request.get_json()
    if not data:
        return jsonify({"error": "Not a JSON"}), 400
    for key, value in data.items():
        if key not in ["id", "created_at", "updated_at",
                       "user_id", "place_id"]:
            setattr(review, key, value)
    storage.save()
    return jsonify(review.to_dict()), 200
