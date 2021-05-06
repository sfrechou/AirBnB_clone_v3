#!/usr/bin/python3
"""Default RESTFul API for State"""
from api.v1.views import app_views
from flask import jsonify, abort
from models import storage
from models.state import State


@app_views.route('/states/',  methods=['GET'])
def get_states():
    """Retrieves the list of all State objects"""
    all_obj = storage.all(State)
    single_objs = []
    for key, value in all_obj.items():
        single_objs.append(value.to_dict())
    return jsonify(single_objs)

@app_views.route('/states/<state_id>',  methods=['GET'])
def get_state_id(state_id):
    """Retrieves a State object by id"""
    all_obj = storage.all(State)
    new_dict = {}
    for key, value in all_obj.items():
        if state_id in key:
            new_dict = value.to_dict()
            return jsonify(new_dict)
    abort(404)
