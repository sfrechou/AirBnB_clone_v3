#!/usr/bin/python3
"""Default RESTFul API for State"""
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.state import State


@app_views.route('/states',  methods=['GET'])
def get_states():
    """Retrieves the list of all State objects"""
    all_obj = storage.all(State)
    single_objs = []
    for key, value in all_obj.items():
        single_objs.append(value.to_dict())
    print(single_objs)
    return jsonify(single_objs)

@app_views.route('/states/<state_id>',  methods=['GET'])
def get_state_id():
    """Retrieves the list of all State objects"""
    all_obj = storage.all(State)
    single_objs = []
    for key, value in all_obj.items():
        single_objs.append(value.to_dict())
    print(single_objs)
    return jsonify(single_objs)
