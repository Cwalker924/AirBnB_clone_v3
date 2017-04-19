#!/usr/bin/python3
"""

"""
from api.v1.views import app_views
from flask import abort
from flask import jsonify
from models import storage


@app_views.route('/status')
def views():
    """
    Status route
    """
    return jsonify({"status": "OK"})


@app_views.route('/stats')
def stats():
    """
    Returns no of objects in each class
    """
    model_list = {"amenities": "Amenity",
                  "cities": "City",
                  "places": "Place",
                  "reviews": "Review",
                  "states": "State",
                  "users": "User"}
    model_dict = {}
    try:
        for k, v in model_list.items():
            model_dict[k] = storage.count(v)
        return (jsonify(model_dict))
    except:
        abort(404)
