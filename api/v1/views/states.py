#!/usr/bin/python3
"""Create a new view for State objects that handles all
default RESTFul API actions:"""
from models import storage
from api.v1.views import app_views
from flask import jsonify, make_response, request, abort
from models.state import State
from models.base_model import BaseModel


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def all_states():
    """ Return all State objects """
    return jsonify(
        {"states": [state.to_dict() for state in storage.all(State).values()]}
        )


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """ Return a State object """
    state = storage.get(State, state_id)
    if state is None:
        return make_response(jsonify({"error": "Not found"}), 404)
    return jsonify(state.to_dict())


@app_views.route(
    '/states/<state_id>', methods=['DELETE'], strict_slashes=False
    )
def delete_state(state_id):
    """ Delete a State object """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def post_state():
    """ Create a new State object """
    date = request.get_json()
    if date is None:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if "name" not in date:
        return "Missing name", 400
    new_state = State(**date)
    storage.new(new_state)
    storage.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def put_state(state_id):
    """Updates a State object: PUT"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    date = request.get_json()
    if date is None:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    for k, v in date.items():
        if k not in ["id", "created_at", "updated_at"]:
            setattr(state, k, v)
    storage.save()
    return jsonify(state.to_dict()), 200
