#!/usr/bin/python3
"""Default RESTFul API for City"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.review import Review
import json
    
@app_views.route('/places/<place_id>/reviews', methods=['GET', 'POST'], strict_slashes=False)
def state_id_city(place_id):
    """
    Retrieves the list of all Review objects of a Place
    Creates a Review
    """
    if request.method == 'GET':
        place = storage.get(Place, place_id)
        if place:
            review = place.reviews()
            return jsonify(review)
        abort(404)

    if request.method == 'POST':
        if request.json:
            new_dict = request.get_json()
            place = storage.get(Place, place_id)
            if place:
                if "user_id" not in new_dict.keys():
                    abort(400, description="Missing user_id")
                user = storage.get(User, new_dict['user_id'])
                if not user:
                    abort(404)
                if "text" not in new_dict.keys():
                    abort(400, description="Missing text")
                new_review = Review(**new_dict)
                storage.new(new_review)
                storage.save()
                return jsonify(new_review.to_dict()), 201
            abort(404)
        else:
            abort(400, description="Not a JSON")

@app_views.route('/reviews/<review_id>', methods=['GET', 'DELETE', 'PUT'], strict_slashes=False)
def reviews_id(review_id):
    """
    Retrieves a Review object
    Deletes a Review object
    Updates a Review object
    """
    if request.method == 'GET':
        review = storage.get(Review, review_id)
        if review:
            return jsonify(review.to_dict)

    if request.method == 'DELETE':
        review = storage.get(Review, review_id)
        if review:
            new_dict = {}
            review.delete()
            storage.save()
            return jsonify(new_dict), 200
        abort(404)

    if request.method == 'PUT':
        if request.json:
            new_dict = request.get_json()
            reviews = storage.get(Review, review_id)
            if not reviews:
                abort(404)
            ignore_keys = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
            for key, value in new_dict.items():
                if key not in ignore_keys:
                    setattr(reviews, key, value)
            storage.save()
            return jsonify(reviews.to_dict()), 200
        else:
            abort(400, description="Not a JSON")
