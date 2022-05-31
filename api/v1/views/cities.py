#!/usr/bin/python3
"""Same as State, create a new view for City objects that
handles all default RESTFul API actions:"""
from models import storage
from api.v1.views import app_views
from flask import jsonify, make_response, request, abort
from models.city import City
from models.state import State


@app_views.route('/cities', methods=['GET'], strict_slashes=False)
def all_cities():
    """ Return all City objects """
    return jsonify(
        [city.to_dict() for city in storage.all(City).values()]
        ), 200


@app_views.route(
    '/states/<state_id>/cities', methods=['GET'], strict_slashes=False
    )
def state_id_cities(state_id):
    """Return all City objects from a State object"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(
        [city.to_dict() for city in state.cities]
        ), 200


@app_views.route(
    '/states/<state_id>/cities', methods=['POST'], strict_slashes=False
    )
def post_state_id_cities(state_id):
    """Returns the new City with the status code 201"""
    date = request.get_json(silent=True)
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    if date is None:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if "name" not in date:
        return make_response(jsonify({"error": "Missing name"}), 400)
    new_city = City(**date)
    new_city.state_id = state_id
    new_city.save()
    return make_response(jsonify(State.to_dict(new_city)), 201)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def cities_id_get(city_id):
    """Returns a City object"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict()), 200


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def cities_id_delete(city_id):
    """Deletes a City object"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def cities_id_put(city_id):
    """Updates a City object"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    date = request.get_json(silent=True)
    if date is None:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    for k, v in date.items():
        setattr(city, k, v)
    city.save()
    return make_response(jsonify(city.to_dict()), 200)
