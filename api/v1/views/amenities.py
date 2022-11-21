#!/usr/bin/python3
"""view for Amenity objects that handles all default
RESTFul API actions"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models.state import Amenity
from . import storage


@app_views.route('/amenities', methods=["GET"], strict_slashes=False)
def getting_amenities():
    """Retrieves the list of all Amenity objects"""
    my_amenity = []
    for amenity in storage.all(Amenity).values():
        my_amenity.append(amenity.to_dict())
    return jsonify(my_amenity)


@app_views.route('/amenities/<string:amenity_id>', methods=["GET"],
                 strict_slashes=False)
def amenity(amenity_id):
    """ Retrieves an Amenity object """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is not None:
        return jsonify(amenity.to_dict())
    else:
        abort(404)


@app_views.route('/amenities/<string:amenity_id>', methods=["DELETE"],
                 strict_slashes=False)
def delete_amenities(amenity_id):
    """ Deletes an Amenity object """

    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    else:
        storage.delete(amenity)
        storage.save()
        return jsonify({})


@app_views.route('/amenities/', methods=["POST"],
                 strict_slashes=False)
def post_amenities():
    """ creates an amenity  """

    content = request.get_json()
    if not content:
        return jsonify(error="Not a JSON"), 400
    if 'name' not in content:
        return jsonify(error="Missing name"), 400

    new_amenity = Amenity(**content)
    new_amenity.save()
    return jsonify(new_amenity.to_dict()), 201


@app_views.route('/amenities/<string:amenity_id>', methods=["PUT"],
                 strict_slashes=False)
def update_amenities(amenity_id):
    """Updates an Amenity object"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    if not request.get_json():
        return jsonify(error='Not a JSON'), 400
    for attr, val in request.get_json().items():
        if attr not in ['id', 'created_at', 'updated_at']:
            setattr(amenity, attr, val)
    amenity.save()
    return jsonify(amenity.to_dict())

