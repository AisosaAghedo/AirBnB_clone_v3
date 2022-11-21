#!/usr/bin/python3
"""view for City objects that handles all default
RESTFul API actions"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from . import City
from . import storage
from . import State


@app_views.route('/states/<string:state_id>/cities', methods=["GET"],
                 strict_slashes=False)
def getting_cities(state_id):
    """Retrieves the list of all City object of a State"""
    new_city = []
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    for city in state.cities():
        new_city.append(city.to_dict())
    return jsonify(new_city)


@app_views.route('/cities/<string:city_id>', methods=["GET"],
                 strict_slashes=False)
def city(city_id):
    """ Retrieves a City object """
    my_city = storage.get(City, city_id)
    if my_city is not None:
        return jsonify(my_city.to_dict())
    else:
        abort(404)


@app_views.route('/cities/<string:city_id>', methods=["DELETE"],
                 strict_slashes=False)
def delete_city(city_id):
    """ Deletes a City object """

    my_city = storage.get(City, city_id)
    if my_city is None:
        abort(404)
    else:
        storage.delete(my_city)
        storage.save()
        return jsonify({})


@app_views.route('/states/<string:state_id>/cities', methods=["POST"],
                 strict_slashes=False)
def post_city(state_id):
    """ creates a city """

    content = request.get_json()
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if not content:
        return jsonify(error="Not a JSON"), 400
    if 'name' not in content:
        return jsonify(error="Missing name"), 400

    content['state_id'] = state_id
    new_city = City(**content)
    new_city.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<string:city_id>', methods=["PUT"],
                 strict_slashes=False)
def update_city(city_id):
    """Updates a City object"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if not request.get_json():
        return jsonify(error='Not a JSON'), 400
    for attr, val in request.get_json().items():
        if attr not in ['id', 'state_id' 'created_at', 'updated_at']:
            setattr(city, attr, val)
    city.save()
    return jsonify(city.to_dict())
