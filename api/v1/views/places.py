#!/usr/bin/python3
"""Default RESTFul API for Place"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State
from models.city import City
from models.place import Place
from models.user import User
from models.amenity import Amenity
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
                        if "name" in new_dict.keys():
                            new_dict['city_id'] = city_id
                            new_place = Place(**new_dict)
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

@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def places_search():
    """
    Retrieves all Place objects depending of the JSON in the body of the request
    """
    if request.json:
        new_dict = request.get_json()
        if new_dict:
            cont = 0
            for lists in new_dict.values():
                if lists != []:
                    cont += 1
            if cont == 0:
                places = storage.all(Place).values()
                single_places = []
                for place in places:
                    single_places.append(place.to_dict())
                return jsonify(single_places)
            else:
                all_places = []
                city_ids = []
                places_filter = []
                states_filter = []
                city_filter = []
                if "states" in new_dict.keys() and len(new_dict['states']) != 0:
                    for state in new_dict['states']:
                        new_state = storage.get(State, state)
                        for city in new_state.cities:
                            new_city = storage.get(City, city.id)
                            city_ids.append(city.id)
                            for place in new_city.places:
                                new_place = storage.get(Place, place.id)
                                states_filter.append(new_place.to_dict())
                                places_filter.append(new_place)
                if "cities" in new_dict.keys() and len(new_dict['cities']) != 0:
                    for city in new_dict['cities']:
                        if city not in city_ids:
                            new_city = storage.get(City, city)
                            city_ids.append(city)
                            for place in new_city.places:
                                new_place = storage.get(Place, place.id)
                                city_filter.append(new_place.to_dict())
                                places_filter.append(new_place)
                if "amenities" in new_dict.keys() and len(new_dict['amenities']) != 0:
                    places_amenity_filter = []
                    if places_filter != []:
                        for place in places_filter:
                            save_place = place.to_dict()
                            nope = 0
                            for amenity_id in new_dict['amenities']:
                                amen = storage.get(Amenity, amenity_id)
                                if amen not in place.amenities:
                                    nope = 1
                                    break         
                            if nope == 0:
                                places_amenity_filter.append(save_place)
                        return jsonify(places_amenity_filter)
                    else:
                        places = storage.all(Place).values()
                        single_places = []
                        for place in places:
                            save_place = place.to_dict()
                            for place_amenity_id in place.amenities:
                                if amenity_id == place_amenity_id:
                                    single_places.append(save_place)
                        return jsonify(single_places)
                else:
                    all_places = city_filter + states_filter
                    return jsonify(all_places)
        else:
            places = storage.all(Place).values()
            single_places = []
            for place in places:
                single_places.append(place.to_dict())
            return jsonify(single_places)
    abort(400, description="Not a JSON")