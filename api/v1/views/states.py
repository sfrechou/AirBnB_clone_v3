#!/usr/bin/python3
"""Default RESTFul API for State"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State
import json

@app_views.route('/states', methods=['GET', 'POST'])
@app_views.route('/states/',  methods=['GET', 'POST'])
def get_states():
    """
    Retrieves the list of all State objects
    Creates a State object
    """
    if request.methods == 'GET':
        all_obj = storage.all(State)
        single_objs = []
        for key, value in all_obj.items():
            single_objs.append(value.to_dict())
        return jsonify(single_objs)
  
    if request.methods == 'POST':
        if request.json:
            new_dict = request.get_json()
            if "name" in new_dict.keys():
                new_state = State(**new_dict)
                storage.new(new_state)
                storage.save()
                return jsonify(new_state.to_dict()), 201
            else:
                abort(400, description="Missing name")
        else:
            abort(400, description="Not a JSON")


@app_views.route('/states/<state_id>',  methods=['GET', 'DELETE', 'PUT'])
def get_state_id(state_id):
    """
    Retrieves a State object by id
    Deletes a State object by id
    Updates a State object
    """
    if request.methods == 'GET':
        all_obj = storage.all(State)
        new_dict = {}
        for key, value in all_obj.items():
            if state_id == value.id:
                new_dict = value.to_dict()
                return jsonify(new_dict)
        abort(404)
    
    if request.methods == 'DELETE':
        all_obj = storage.all(State)
        new_dict = {}
        for key, value in all_obj.items():
            if state_id == value.id:
                value.delete()
                storage.save()
                return jsonify(new_dict), 200
        abort(404)

    if request.methods == 'PUT':
        if request.json:
            new_dict = request.get_json()
            states = storage.all(State).values()
            for state in states:
                if state.id == state_id:
                    state.name = new_dict['name']
                    storage.save()
                    return jsonify(state.to_dict()), 200
            abort(404)
        else:
            abort(400, description="Not a JSON")

