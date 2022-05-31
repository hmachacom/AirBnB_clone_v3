#!/usr/bin/python3
"""Create a new view for User object that handles
all default RESTFul API actions"""
from models import storage
from api.v1.views import app_views
from flask import jsonify, make_response, request, abort
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def all_user():
    """ Return all User objects """
    return jsonify(
        [user.to_dict() for user in storage.all(User).values()]
        ), 200


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def user_id(user_id):
    """ Return a User object """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict()), 200


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def user_delete(user_id):
    """Delete a User object"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def user_post():
    """Create a new User object"""
    date = request.get_json(silent=True)
    if date is None:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if "email" not in date:
        return ({"Missing": "email"}), 400
    new_user = User(**date)
    new_user.save()
    return make_response(jsonify(new_user.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def user_put(user_id):
    """Updates a User object: PUT """
    date = request.get_json(silent=True)
    if date is None:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    for key, value in date.items():
        setattr(user, key, value)
    user.save()
    return make_response(jsonify(user.to_dict()), 200)
