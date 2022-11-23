#!/usr/bin/python3
"""reviews.py"""

from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.review import Review
from models.user import User
from models.place import Place
from models.city import City


@app_views.route('/places/<string:place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_reviews(place_id=None):
    """Return all Place objects"""
    place_objs = storage.get(Place, place_id)
    if place_objs:
        return jsonify([obj.to_dict() for obj in place_objs.reviews])
    abort(404)


@app_views.route('/reviews/<string:review_id>', methods=['GET'], strict_slashes=False)
def get_review(review_id=None):
    """Return a review using its id"""
    review_obj = storage.get(Review, review_id)
    if review_obj:
        return jsonify(review_obj.to_dict())
    abort(404)


@app_views.route('/reviews/<string:review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id=None):
    """Deletes a review object"""
    review_objs = storage.get(Review, review_id)
    if review_objs:
        storage.delete(review_objs)
        storage.save()
        return jsonify({})
    abort(404)


@app_views.route('/places/<string:place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def review_post(place_id=None):
    """Create place object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if not request.get_json():
        return jsonify(error='Not a JSON'), 400
    content = request.get_json()
    if 'user_id' not in content:
        return jsonify(error='Missing user_id'), 400
    user = storage.get(User, content['user_id'])
    if user is None:
        abort(404)
    if 'text' not in content:
        return jsonify(error='Missing text'), 400
    content['place_id'] = place_id
    review = Review(**content)
    review.save()
    return jsonify(review.to_dict()), 201


@app_views.route('/reviews/<string:review_id>', methods=['PUT'],
                 strict_slashes=False)
def review_put(review_id=None):
    """Update review object"""
    restricted = ['id', "created_at", "updated_at", 'user_id', 'city_id']
    if not request.get_json():
        return jsonify(error='Not a JSON'), 400
    dict_body = request.get_json()
    review_obj = storage.get(Review, review_id)
    if review_obj:
        for key, value in dict_body.items():
            if key not in restricted:
                setattr(review_obj, key, value)
        storage.save()
        return jsonify(review_obj.to_dict()), 200
    else:
        return abort(404)
