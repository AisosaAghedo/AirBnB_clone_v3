#!/usr/bin/python3
"""view for User objects that handles all default
RESTFul API actions"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.user import User
from . import storage
@app_views.route('/users', methods=["GET"], strict_slashes=False)
def getting_users():
    """Retrieves the list of all User objects"""
    users = []
    for user in storage.all(User).values():
        users.append(user.to_dict())
    return jsonify(users)
@app_views.route('/users/<string:user_id>', methods=["GET"],
                 strict_slashes=False)
def user(user_id):
    """ Retrieves a User object """
    user = storage.get(User, user_id)
    if user is not None:
        return jsonify(user.to_dict())
    else:
        abort(404)
@app_views.route('/users/<string:user_id>', methods=["DELETE"],
                 strict_slashes=False)
def delete_users(user_id):
    """ Deletes a user object """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    else:
        storage.delete(user)
        storage.save()
        return jsonify({})
@app_views.route('/users/', methods=["POST"],
                 strict_slashes=False)
def post_users():
    """ creates a user  """
    content = request.get_json()
    if not content:
        return jsonify(error="Not a JSON"), 400
    if 'email' not in content:
        return jsonify(error="Missing email"), 400
    if 'password' not in content:
        return jsonify(error="Missing password"), 400

    new_user = User(**content)
    new_user.save()
@@ -68,9 +70,7 @@ def update_users(user_id):
    if not request.get_json():
        return jsonify(error='Not a JSON'), 400
    for attr, val in request.get_json().items():
        if attr not in ['id', 'created_at', 'updated_at']:
        if attr not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(user, attr, val)
    user.save()
    return jsonify(user.to_dict())
