#!/usr/bin/python3
"""
Amenities API routes
"""

from api.v1.views import app_views
from flask import abort
from flask import jsonify
from flask import request
from models import Amenity
from models import storage


@app_views.route('/amenities', methods=["GET"])
@app_views.route('/amenities/<amenity_id>/', methods=["GET"])
def get_amenities():
    """"
    Retrieves all amenity or a specific amenity w/ id
    """
    if amenity_id is None:
        all_amenity = storage.all("Amenity")
        list_amenity = []
        for k, v in all_amenity.items():
            amenity_json = v.to_json()
            list_amenity.append(amenity_json)
        return jsonify(list_amenity)
    try:
        id_amenity = storage.get("Amenity", amenity_id)
        return jsonify(id_amenity)
    except:
        abort(404)


@app_views.route('/amenities/<amenity_id>/', methods=["POST"])
def post_amenity():
    """
    Post to amenity
    """
    try:
        r = request.get_json()
        if "name" not in r:
            return ("Missing name", 400)
        add_amenity = Amenity(r)
        add_amenity.save()
        return (jsonify(add_amenity.to_json()), 201)
    except:
        return ("Not a json", 400)


@app_views.route('/amenities/<amenity_id>/', methods=["PUT"])
def put_amenity(amenity_id):
    """
    Update amenity
    """
    get_amenity = storage.get("Amenity", amenity_id)
    if get_amenity is None:
        abort(404)
    try:
        r = request.get_json()
        list_amenity = ["id", "created_id", "updated_at"]
        for k, v in r.items():
            if k not in list_amenity:
                setattr(get_amenity, k, v)
        get_amenity.save()
        amenity_json = get_amenity.to_json()
        return (jsonify(amenity_json), 200)
    except:
        abort(404)


@app_views.route('/amenities/<amenity_id>/', methods=["DELETE"])
def delete_amenity(amenity_id):
    """
    Deletes aminity
    """
    del_aminity = storage.get("Amenity", amenity_id)
    if del_aminity is None:
        abort(404)
    try:
        storage.delete(del_aminity)
        storage.save()
        return (jsonify({}), 200)
    except:
        abort(404)
