#!/usr/bin/python3
"""Create a new view for Place object that handles
all default RESTFul API actions"""
from models import storage
from api.v1.views import app_views
from flask import jsonify, make_response, request, abort
from models.place import Place
from models.city import City
from models.user import User


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


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def all_place(place_id):
    """ retorna un objeto place """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


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
    "/cities/<city_id>/places", methods=["POST"], strict_slashes=False
    )
def crearP(city_id):
    """ Crea un nuevo objeto ciudad """
    citi = storage.get(City, city_id)
    if citi is None:
        abort(404)
    datos = request.get_json()
    if datos is None:
        abort(400, "Not a JSON")
    if "user_id" not in datos:
        abort(400, "Missing user_id")
    usu = storage.get(User, datos['user_id'])
    if usu is None:
        abort(404)
    if "name" not in datos:
        abort(400, "Missing name")
    datos["city_id"] = city_id
    nuevo = Place(**datos)
    nuevo.save()
    return make_response(jsonify(nuevo.to_dict()), 201)


@app_views.route("/places/<place_id>", methods=["PUT"], strict_slashes=False)
def putP(place_id):
    """ actualiza el objeto ciudad """
    av = ["id", "user_id", "city_id", "created_at", "updated_at"]
    lugar = storage.get(Place, place_id)
    if lugar is None:
        abort(404)

    datos = request.get_json(silent=True)
    if datos is None:
        abort(400, "Not a JSON")
    for clave, valor in datos.items():
        if clave not in av:
            setattr(lugar, clave, valor)
    storage.save()
    return make_response(jsonify(lugar.to_dict()), 200)
