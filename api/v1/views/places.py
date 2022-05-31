#!/usr/bin/python3
"""Create a new view for Place object that handles
all default RESTFul API actions"""
from models import storage
from api.v1.views import app_views
from flask import jsonify, make_response, request, abort
from models.place import Place
from models.city import City
from models.user import User


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def place_id(place_id):
    """ Return a Place object """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict()), 200


@app_views.route(
    '/cities/<city_id>/places', methods=['GET'], strict_slashes=False
    )
def places_city_id(city_id):
    """ Return a Place object """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    places = [place.to_dict() for place in city.places]
    return jsonify(places), 200


@app_views.route(
    '/places/<place_id>', methods=['DELETE'], strict_slashes=False
    )
def place_delete(place_id):
    """Delete a Place object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route(
    '/cities/<city_id>/places', methods=['POST'], strict_slashes=False
    )
def place_post(city_id):
    """Creates a Place: POST /api/v1/cities/<city_id>/places"""
    date = request.get_json(silent=True)
    if date is None:
        return jsonify({"error": "Not a JSON"}), 400
    if "user_id" not in date:
        return jsonify({"Missing": "user_id"}), 400
    user = storage.get(User, date["user_id"])
    if user is None:
        abort(404)
    if "name" not in date:
        return jsonify({"Missing": "name"}), 400
    date["city_id"] = city_id
    new_user = Place(**date)
    new_user.save()
    return make_response(jsonify(new_user.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def place_put(place_id):
    """Updates a Place: PUT /api/v1/places/<place_id>"""
    attr = ["id", "user_id", "city_id", "created_at", "updated_at"]
    date = request.get_json(silent=True)
    if date is None:
        return jsonify({"error": "Not a JSON"}), 400
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    for key, value in date.items():
        if key not in attr:
            setattr(place, key, value)
    storage.save()
    return make_response(jsonify(place.to_dict()), 200)
