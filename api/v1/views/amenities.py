#!/usr/bin/python3
"""Default RESTFul API for Amenity"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.amenity import Amenity
import json


@app_views.route('/amenities', methods=['GET', 'POST'], strict_slashes=False)
def get_amenities():
    """
    Retrieves the list of all Amenity objects
    Creates a Amenity object
    """
    if request.method == 'GET':
        all_obj = storage.all(Amenity)
        single_objs = []
        for key, value in all_obj.items():
            single_objs.append(value.to_dict())
        return jsonify(single_objs)

    if request.method == 'POST':
        if request.json:
            new_dict = request.get_json()
            if "name" in new_dict.keys():
                new_amenity = Amenity(**new_dict)
                storage.new(new_amenity)
                storage.save()
                return jsonify(new_amenity.to_dict()), 201
            else:
                abort(400, description="Missing name")
        else:
            abort(400, description="Not a JSON")


@app_views.route('/amenities/<amenity_id>',  methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def get_amenity_id(amenity_id):
    """
    Retrieves a Amenity object by id
    Deletes a Amenity object by id
    Updates a Amenity object
    """
    if request.method == 'GET':
        all_obj = storage.all(Amenity)
        new_dict = {}
        for key, value in all_obj.items():
            if amenity_id == value.id:
                new_dict = value.to_dict()
                return jsonify(new_dict)
        abort(404)

    if request.method == 'DELETE':
        all_obj = storage.all(Amenity)
        new_dict = {}
        for key, value in all_obj.items():
            if amenity_id == value.id:
                value.delete()
                storage.save()
                return jsonify(new_dict), 200
        abort(404)

    if request.method == 'PUT':
        if request.json:
            new_dict = request.get_json()
            amenities = storage.all(Amenity).values()
            for amenity in amenities:
                if amenity.id == amenity_id:
                    amenity.name = new_dict['name']
                    storage.save()
                    return jsonify(amenity.to_dict()), 200
            abort(404)
        else:
            abort(400, description="Not a JSON")
