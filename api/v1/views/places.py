#!/usr/bin/python3
"""view for Place objects that handles all default
RESTFul API actions"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.city import City
from models import storage
from models.user import User
from models.place import Place


@app_views.route('/cities/<string:city_id>/places', methods=["GET"],
                 strict_slashes=False)
def getting_places(city_id):
    """Retrieves the list of all places object of a city"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    places = []
    for place in city.places:
        places.append(place.to_dict())
    return jsonify(places)


@app_views.route('/places/<string:place_id>', methods=["GET"],
                 strict_slashes=False)
def place(place_id):
    """ Retrieves a Place object """
    my_place = storage.get(Place, place_id)
    if my_place is not None:
        return jsonify(my_place.to_dict())
    else:
        abort(404)


@app_views.route('/places/<string:place_id>', methods=["DELETE"],
                 strict_slashes=False)
def delete_place(place_id):
    """ Deletes a place object """
    my_place = storage.get(Place, place_id)
    if my_place is None:
        abort(404)
    else:
        storage.delete(my_place)
        storage.save()
        return jsonify({})


@app_views.route('/cities/<string:city_id>/places', methods=["POST"],
                 strict_slashes=False)
def post_place(city_id):
    """ creates a place """

    content = request.get_json()
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if not content:
        return jsonify(error="Not a JSON"), 400
    if 'user_id' not in content:
        return jsonify(error="Missing user_id"), 400
    if 'name' not in content:
        return jsonify(error="Missing name"), 400
    user = storage.get(User, content['user_id'])
    if user is None:
        abort(404)
    content['city_id'] = city_id
    new_place = place(**content)
    new_place.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<string:place_id>', methods=["PUT"],
                 strict_slashes=False)
def update_place(place_id):
    """Updates a place object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if not request.get_json():
        return jsonify(error='Not a JSON'), 400
    for attr, val in request.get_json().items():
        if attr not in ['id', 'user_id', 'city_id', 'created_at',
                        'updated_at']:
            setattr(place, attr, val)
    place.save()
    return jsonify(place.to_dict())
