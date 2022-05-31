#!/usr/bin/python3
"""Create a new view for Amenity objects that handles
all default RESTFul API actions:"""
from models import storage
from api.v1.views import app_views
from flask import jsonify, make_response, request, abort
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def all_amenity():
    """ Return all Amenity objects """
    return jsonify(
        [city.to_dict() for city in storage.all(Amenity).values()]
        ), 200


@app_views.route(
    '/amenities/<amenity_id>', methods=['GET'], strict_slashes=False
    )
def amenity_id(amenity_id):
    """ Return a Amenity object """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        return make_response(jsonify({"error": "Not found"}), 404)
    return jsonify(amenity.to_dict()), 200


@app_views.route(
    '/amenities/<amenity_id>', methods=['DELETE'], strict_slashes=False
    )
def amenity_delete(amenity_id):
    """Delete a Amenity object"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def amenity_post():
    """Create a new Amenity object"""
    date = request.get_json(silent=True)
    if date is None:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if "name" not in date:
        return jsonify(({"Missing": "name"}), 400)
    new_amenity = Amenity(**date)
    storage.new(new_amenity)
    storage.save()
    return make_response(jsonify(new_amenity.to_dict()), 201)


@app_views.route(
    '/amenities/<amenity_id>', methods=['PUT'], strict_slashes=False
    )
def amenity_put(amenity_id):
    """Updates a Amenity object: PUT """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    date = request.get_json(silent=True)
    if date is None:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    for key, value in date.items():
        setattr(amenity, key, value)
    storage.save()
    return make_response(jsonify(amenity.to_dict()), 200)
