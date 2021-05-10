#!/usr/bin/python3
"""Default RESTFul API for User"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.user import User
import json


@app_views.route('/users', methods=['GET', 'POST'], strict_slashes=False)
def get_users():
    """
    Retrieves the list of all User objects
    Creates a User object
    """
    if request.method == 'GET':
        all_obj = storage.all(User)
        single_objs = []
        for key, value in all_obj.items():
            single_objs.append(value.to_dict())
        return jsonify(single_objs)

    if request.method == 'POST':
        if request.json:
            new_dict = request.get_json()
            if "email" not in new_dict.keys():
                abort(400, description="Missing email")
            if "password" not in new_dict.keys():
                abort(400, description="Missing password")
            new_user = User(**new_dict)
            storage.new(new_user)
            storage.save()
            return jsonify(new_user.to_dict()), 201
        else:
            abort(400, description="Not a JSON")


@app_views.route('/users/<user_id>',  methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def get_user_id(user_id):
    """
    Retrieves a User object by id
    Deletes a User object by id
    Updates a User object
    """
    if request.method == 'GET':
        all_obj = storage.all(User)
        new_dict = {}
        for key, value in all_obj.items():
            if user_id == value.id:
                new_dict = value.to_dict()
                return jsonify(new_dict)
        abort(404)

    if request.method == 'DELETE':
        all_obj = storage.all(User)
        new_dict = {}
        for key, value in all_obj.items():
            if user_id == value.id:
                value.delete()
                storage.save()
                return jsonify(new_dict), 200
        abort(404)

    if request.method == 'PUT':
        if request.json:
            new_dict = request.get_json()
            users = storage.all(User).values()
            ignore_keys = ['id', 'email', 'created_at', 'updated_at']
            for user in users:
                if user.id == user_id:
                    for key, value in new_dict.items():
                        if key not in ignore_keys:
                            setattr(user, key, value)
                    storage.save()
                    return jsonify(user.to_dict()), 200
            abort(404)
        else:
            abort(400, description="Not a JSON")
