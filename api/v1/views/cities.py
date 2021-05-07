#!/usr/bin/python3
"""Default RESTFul API for City"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State
from models.city import City
import json
    

@app_views.route('/states/<state_id>/cities', methods=['GET', 'POST'], strict_slashes=False)
def state_id_city(state_id):
    """
    Retrieves the list of all City objects of a State
    Creates a City
    """
    if request.method == 'GET':
        state = storage.get(State, state_id)
        if state:
            single_objs = []
            for city in state.cities:
                single_objs.append(city.to_dict())
            return jsonify(single_objs)
        abort(404)

    if request.method == 'POST':
        if request.json:
            new_dict = request.get_json()
            state = storage.get(State, state_id)
            if state:
                if "name" in new_dict.keys():
                    new_city = State(**new_dict)
                    storage.new(new_city)
                    storage.save()
                    return jsonify(new_city.to_dict()), 201
                else:
                    abort(400, description="Missing name")
            abort(404)
        else:
            abort(400, description="Not a JSON")

@app_views.route('/cities/<city_id>', methods=['GET', 'DELETE', 'PUT'], strict_slashes=False)
def city(city_id):
    """
    Retrieves a City object
    Deletes a City object
    Updates a City object
    """
    if request.method == 'GET':
        city = storage.get(City, city_id)
        if city:
            return jsonify(city.to_dict())
        abort(404)

    if request.method == 'DELETE':
        city = storage.get(City, city_id)
        if city:
            new_dict = {}
            city.delete()
            storage.save()
            return jsonify(new_dict), 200
        abort(404)

    if request.method == 'PUT':
        if request.json:
            city = storage.get(City, city_id)
            if city:
                new_dict = request.get_json()
                city.name = new_dict['name']
                storage.save()
                return jsonify(city.to_dict()), 200
            abort(404)
        else:
            abort(400, description="Not a JSON")
