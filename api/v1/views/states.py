#!/usr/bin/python3
"""view for State objects that handles all default
RESTFul API actions"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models.state import State
from . import storage


@app_views.route('/states', methods=["GET"], strict_slashes=False)
def getting_state():
    """Retrieves the list of all State objects"""
    my_states = []
    for state in storage.all(State).values():
        my_states.append(state.to_dict())
    return jsonify(my_states)


@app_views.route('/states/<string:state_id>', methods=["GET"],
                 strict_slashes=False)
def state(state_id):
    """ Retrieves a State object """
    my_states = storage.get(State, state_id)
    if my_states is not None:
        return jsonify(my_states.to_dict())
    else:
        abort(404)


@app_views.route('/states/<string:state_id>', methods=["DELETE"],
                 strict_slashes=False)
def delete_states(state_id):
    """ Deletes a State object """

    my_state = storage.get(State, state_id)
    if my_state is None:
        abort(404)
    else:
        storage.delete(my_state)
        storage.save()
        return jsonify({})


@app_views.route('/states/', methods=["POST"],
                 strict_slashes=False)
def post_states():
    """ creates a state """

    content = request.get_json()
    if not content:
        return jsonify(error="Not a JSON"), 400
    if 'name' not in content:
        return jsonify(error="Missing name"), 400

    new_state = State(**content)
    new_state.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<string:state_id>', methods=["PUT"],
                 strict_slashes=False)
def update_states(state_id):
    """Updates a State object"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if not request.get_json():
        return jsonify(error='Not a JSON'), 400
    for attr, val in request.get_json().items():
        if attr not in ['id', 'created_at', 'updated_at']:
            setattr(state, attr, val)
    state.save()
    return jsonify(state.to_dict())
