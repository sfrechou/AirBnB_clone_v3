#!/usr/bin/python3
"""Default RESTFul API for Place"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State
from models.city import City
from models.place import Place
from models.user import User
import json


@app_views.route('/cities/<city_id>/places', methods=['GET', 'POST'], strict_slashes=False)
def city_id_places(city_id):
    """
    Retrieves the list of all Place objects of a City
    Creates a Place
    """
    if request.method == 'GET':
        city = storage.get(City, city_id)
        if city:
            single_objs = []
            for place in city.places:
                single_objs.append(place.to_dict())
            return jsonify(single_objs)
        abort(404)

    if request.method == 'POST':
        if request.json:
            new_dict = request.get_json()
            city = storage.get(City, city_id)
            if city:
                if "user_id" in new_dict.keys():
                    user = storage.get(User, new_dict['user_id'])
                    if user:
                        if "nam" in new_dict.keys():
                            new_place = City(**new_dict)
                            storage.new(new_place)
                            storage.save()
                            return jsonify(new_place.to_dict()), 201
                        else:
                            abort(400, description="Missing name")
                    abort(404)
                else:
                    abort(400, description="Missing user_id")
            abort(404)
        else:
            abort(400, description="Not a JSON")

@app_views.route('/places/<place_id>', methods=['GET', 'DELETE', 'PUT'], strict_slashes=False)
def place(place_id):
    """
    Retrieves a Place object
    Deletes a Place object
    Updates a Place object
    """
    if request.method == 'GET':
        place = storage.get(Place, place_id)
        if place:
            return jsonify(place.to_dict())
        abort(404)

    if request.method == 'DELETE':
        place = storage.get(Place, place_id)
        if place:
            new_dict = {}
            place.delete()
            storage.save()
            return jsonify(new_dict), 200
        abort(404)

    if request.method == 'PUT':
        if request.json:
            place = storage.get(Place, place_id)
            if place:
                new_dict = request.get_json()
                ignore_keys = ['id', 'user_id', 'created_at', 'updated_at']
                for key, value in new_dict.items():
                        if key not in ignore_keys:
                            setattr(place, key, value)
                storage.save()
                return jsonify(place.to_dict()), 200
            abort(404)
        else:
            abort(400, description="Not a JSON")
