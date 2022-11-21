#!/usr/bin/python3
"""view for State objects that handles all default 
RESTFul API actions"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State

@app_views.route('/states', methods=["GET"], strict_slashes=False)
def getting_state():
    """Retrieves the list of all State objects"""
    my_states = []
    for state in storage.all("State").values():
        my_states.append(state.to_dict())
    return jsonify(my_states)


@app_views.route('/states/<string: states_id>', methods=["GET"], strict_slashes=False)
def state(state_id):
    """ Retrieves a State object """
    my_states = storage.get("State", state_id)
    if my_states is not None:
        return jsonify(my_states.to_dict())
    abort(404)

@app_views.route('/state/<string:state_id>', methods=["DELETE"], strict_slashes=False)
def delete_states(state_id):
    """ Deletes a State object """

    my_state = storage.get("State", state_id)
    if my_state is None:
        abort(404)
    storage.delete(my_state)
    storage.save()
    return jsonify({})

@app_views.route('/states', methods=["POST"], strict_slashes=False)
def post_states():
    """ creates a state """

    content = request.get_json()
    if content is None:
        return jsonify({"error": "Not a JSON"}), 400
    name = content.get("name")
    if name is None:
        return jsonify({"error": "Missing name"}), 400

    new_state = State(**content)
    new_state.save()

    return jsonify(new_state.to_dict()), 201

@app_views.route('/state/<string: state_id>', methods=["PUT"], strict_slashes=False)
def update_states(state_id):
    """Updates a State object"""
    
    content = request.get_json()
    if content is None:
        return jsonify({"error": "Not a JSON"}), 400
    
    my_state = storage.get("State", state_id)
    if my_state is None:
        abort(404)

    not_allowed = ["id", "created_at", "updated_at"]
    for key, value in content.items():
        if key not in not_allowed:
            setattr(my_state, key, value)
    
    my_state.save()
    return jsonify(my_state.to_dict)
