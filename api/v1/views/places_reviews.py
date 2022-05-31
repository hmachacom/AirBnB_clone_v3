#!/usr/bin/python3
"""Create a new view for Place object that handles
all default RESTFul API actions"""
from models import storage
from api.v1.views import app_views
from flask import jsonify, make_response, request, abort
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route(
    '/places/<place_id>/reviews', methods=['GET'], strict_slashes=False
    )
def all_reviews(place_id):
    """ Return a Place object """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    reviews = [review.to_dict() for review in place.reviews]
    return jsonify(reviews), 200


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def all_review(review_id):
    """ retorna un objeto review """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route(
    '/reviews/<review_id>', methods=['DELETE'], strict_slashes=False
    )
def reviews_delete(review_id):
    """Delete a Place object"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    storage.delete(review)
    storage.save()
    return jsonify({}), 200


@app_views.route(
    '/places/<place_id>/reviews', methods=['POST'], strict_slashes=False
    )
def reviews_post(place_id):
    """ Create a new review for a place """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    date = request.get_json()
    if date is None:
        abort(400, "Not a JSON")
    if "user_id" not in date:
        abort(400, "Missing user_id")
    if "text" not in date:
        abort(400, "Missing text")
    user = storage.get(User, date['user_id'])
    if user is None:
        abort(404)
    date['place_id'] = place_id
    review = Review(**date)
    storage.save()
    return jsonify(review.to_dict()), 201


@app_views.route(
    '/reviews/<review_id>', methods=['PUT'], strict_slashes=False
    )
def reviwes_put(review_id):
    """ Update a review """
    attr = ["id", "user_id", "place_id", "created_at", "updated_at"]
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    date = request.get_json()
    if date is None:
        abort(400, "Not a JSON")
    for key, value in date.items():
        if key not in attr:
            setattr(review, key, value)
    storage.save()
    return jsonify(review.to_dict()), 200
