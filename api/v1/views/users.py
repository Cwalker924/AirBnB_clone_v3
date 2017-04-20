#!/usr/bin/python3
"""
User API routes
"""
from api.v1.views import app_views
from flask import abort
from flask import jsonify
from flask import request
from models import User
from models import storage


@app_views.route('/users', methods=["GET"], strict_slashes=False)
@app_views.route('/users/<users_id>', methods=["GET"], strict_slashes=False)
def get_users(users_id=None):
    """
    Retrieves all users obj or specified user w/ id
    """
    if user_id is None:
        users = storage.all("User")
        users = [v.to_json() for k, v in users.items()]
        return (jsonify(users))
    spec_user = storage.get("Users", users_id)
    if spec_user is None:
        abort(404)
    return (jsonify(spec.user.to_json()))


@app_views.route('/users', methods=["POST"], strict_slashes=False)
def post_users():
    """
    Post to users
    """
    r = reqest.get_json()
    if not r:
        return ("Not a JSON", 400)
    if "password" not in r:
        return ("Missing password", 400)
    if "email" not in r:
        return ("Missing email", 400)
    add_user = User(email=r.get("email"),
                    password=r.get("password"),
                    first_name=r.get("first_name"),
                    last_name=r.get("last_name"))
    storage.new(add_user)
    storage.save()
    return (jsonify(add_user.to_json()), 201)


@app_views.route('/users/<users_id>/', methods=["PUT"], strict_slashes=False)
def put_users(users_id):
    """
    Update users
    """
    user = storage.get("User", users_id)
    if user is None:
        abort(404)
    r = request.get_json()
    if not r:
        return ("Not a JSON", 400)
    my_list = ["id", "created_at", "updated_at", "email"]
    for k, v in r.items():
        if k not in my_list:
            setattr(user, k, v)
    user.save()
    return (jsonify(user.to_json), 200)


@app_views.route('/users/<users_id>/', methods=["DELETE"],
                 strict_slashes=False)
def delete_users(users_id):
    """
    Deletes users
    """
    user = storage.get("User", users_id)
    if user is None:
        return (abort(404))
    storage.delete(user)
    return (jsonify({}), 200)
