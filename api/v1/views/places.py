#!/usr/bin/python3
"""
Place API routes
"""
from api.v1.views import app_views
from flask import abort
from flask import jsonify
from flask import request
from models import Place
from models import storage


@app_views.route('/cities/<cities_id>/places', methods=["GET"],
                 strict_slashes=False)
def get_places_city(cities_id=None):
    """
    Retrieves all place obj in a given city
    """
    city = storage.get("City", cities_id)
    places = storage.all("Place")
    if city is None:
        abort(404)

    list_city = []
    places = [v.to_json() for k, v in places.items()]
    for i in places:
        if cities_id == i["cities_id"]:
            list_city.append(i)
    return (jsonify(list_city))


@app_views.route('/places/<places_id>', methods=["GET"], strict_slashes=False)
def get_places(places_id=None):
    """
    Get places
    """
    place = storage.get("Place", places_id)
    if place is None:
        abort(404)
    return (jsonify(place.to_json()))


@app_views.route('/cities/<city_id>/places', methods=["POST"],
                 strict_slashes=False)
def post_places(city_id):
    """
    Post to places
    """
    city = storage.get("City", city_id)
    r = request.get_json()
    users = storage.get("User", r.get("user_id"))
    if city is None:
        abort(404)
    if not r:
        return ("Not a JSON", 400)
    if "user_id" not in r:
        return ("Missing user_id", 400)
    if "name" not in r:
        return ("Missing name", 400)
    if users is None:
        abort(404)

    r["city_id"] = city_id
    add_place = Place(r)
    storage.new(add_place)
    storage.save()
    place_tojson = storage.get("Place", add_place.id).to_json()
    return (jsonify(place_tojson), 201)


@app_views.route('/places/<places_id>', methods=["PUT"], strict_slashes=False)
def put_place(places_id):
    """
    Update places
    """
    r = request.get_json()
    places = storage.get("Place", places_id)
    if r is None:
        return ("Not a JSON", 400)
    if places is None:
        abort(404)

    list_place = ["id", "user_id", "city_id", "created_at", "updated_at"]
    for k, v in r.items():
        if k not in list_place:
            setattr(places, k, v)
    places.save()
    places_tojson = places.to_json()
    return (jsonify(places_tojson), 200)


@app_views.route('/places/<places_id>', methods=["DELETE"],
                 strict_slashes=False)
def delete_place(places_id):
    """
    Deletes place
    """
    place = storage.get("Place", places_id)
    if place is None:
        abort(404)
    storage.delete(place)
    return (jsonify({}))
