#!/usr/bin/python3
"""
City API routes
"""
from api.v1.views import app_views
from flask import abort
from flask import jsonify
from flask import request
from models import City
from models import storage


@app_views.route('/states/<state_id>/cities', methods=["GET"],
                 strict_slashes=False)
def get_cities():
    """
    Retrieves all city obj from specific state
    """

    if state_id is None:
        abort(404)
    states = storage.get("State", state_id)
    if states is None:
        abort(404)

    list_city = []
    cities = storage.all("City")
    for k, v in cities.items():
        if v.state_id == state_id:
            list_city.append(v.to_json())
    return (jsonify(list_city))


@app_views.route('/cities/<cities_id>', methods=["GET"], strict_slashes=False)
def get_city(cities_id):
    """"
    Retrieves specific city w/ id
    """
    if cities_id is None:
        abort(404)
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    return (jsonify(city.to_json()))


@app_views.route('/states/<states_id>/cities', methods=["POST"],
                 strict_slashes=False)
def post_city():
    """
    Post to city
    """
    r = request.get_json()
    if not r:
        return ("Not a JSON", 400)
    if r.get("name") is None:
        return ("Missing name", 400)
    if storage.get("State", state_id) is None:
        abort(404)

    r["state_id"] = state_id
    add_city = City(r)
    storage.new(add_city)
    stroage.save()
    new_city = storage.get("City", add_city.id)
    return (jsonify(new_city.to_json()), 201)


@app_views.route('/cities/<cities_id>/', methods=["PUT"], strict_slashes=False)
def put_cities(cities_id):
    """
    Update city
    """
    cities = storage.get("City", cities_id)
    r = request.get_json()
    if cities is None:
        abort(404)
    if r is None:
        return ("Not a JSON", abort(400))

    cities.name = r.get("name", cities.name)
    cities.save()
    return (jsonify(cities.to_json()))


@app_views.route('/cities/<cities_id>/', methods=["DELETE"],
                 strict_slashes=False)
def delete_city(cities_id):
    """
    Deletes cities
    """
    cities = storage.get("City", cities_id)
    if cities is None:
        abort(404)
    storage.delete(cities)
    return (jsonify({}), 200)
