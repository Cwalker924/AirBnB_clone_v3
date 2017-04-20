#!/usr/bin/python3
"""
Places and Reviews API routes
"""
from api.v1.views import app_views
from flask import abort
from flask import jsonify
from flask import request
from models import Place
from models import Review
from models import storage


@app_views.route('/places/<places_id>/reviews', methods=["GET"],
                 strict_slashes=False)
def get_review_places(places_id=None):
    """
    Retrieves place obj review w/ a given id
    """
    place = storage.get("Place", places_id)
    review = storage.all("Review")
    if place is None:
        abort(404)
    list_review = []
    spec_review = [v.to_json() for k, v in review.items()]
    for reviews in spec_review:
        if places_id == reviews["places_id"]:
            list_review.append(review)
    return (jsonify(list_review))


@app_views.route('/reviews/<review_id>', methods=["GET"],
                 strict_slashes=False)
def get_review(review_id=None):
    """
    Get reviews
    """
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)
    review_tojson = review.to_json()
    return (jsonify(review_tojson))


@app_views.route('/places/<places_id>/reviews', methods=["POST"],
                 strict_slashes=False)
def post_review(places_id):
    """
    Post to places
    """
    place = storage.get("Place", places_id)
    r = request.get_json()
    user = storage.get("User", r.get("user_id"))
    if place is None:
        abort(404)
    if user is None:
        abort(404)
    if not r:
        return ("Not a JSON", 400)
    if "user_id" not in r:
        return ("Missing user_id", 400)
    if "text" not in r:
        return ("Missing text", 400)
    r["places_id"] = places_id
    add_review = Review(r)
    storage.new(add_review)
    storage.save()
    review_tojson = storage.get("Review", add_review.id).to_json()
    return (jsonify(review_tojson), 201)


@app_views.route('/reviews/<review_id>', methods=["PUT"], strict_slashes=False)
def put_review(review_id):
    """
    Update review
    """
    r = request.get_json()
    review = storage.get("Review", review_id)
    if r is None:
        return ("Not a JSON", 400)
    if review is None:
        abort(404)
    list_review = ["id", "user_id", "created_at", "updated_at"]
    for k, v in r.items():
        if k not in list_review:
            setattr(review, k, v)
    review.save()
    review_tojson = review.to_json()
    return (jsonify(review_tojson), 200)


@app_views.route('/reviews/<review_id>', methods=["DELETE"],
                 strict_slashes=False)
def delete_review(review_id):
    """
    Deletes review
    """
    review = storage.get("Review", review_id)
    if review is None:
        return (abort(404))
    storage.delete(review)
    return (jsonify({}), 200)
