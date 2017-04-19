#!/usr/bin/python3
"""
States API routes
"""
from api.v1.views import app_views
from flask import abort
from flask import jsonify
from flask import request
from models import State
from models import storage


@app_views.route('/states', methods=["GET"], strict_slashes=False)
def get_states():
    """
    Retrieves all state obj
    """
    states = storage.all("State")
    states = [v.to_json() for k, v in states.items()]
    return (jsonify(states))

@app_views.route('/states/<states_id>', methods=["GET"], strict_slashes=False)
def get_state(states_id):
    """"
    Retrieves specific states w/ id
    """
    if states_id is None:
        abort(404)
    state = storage.get("State", states_id)
    if state is None:
        abort(404)
    return (jsonify(state.to_json()))

@app_views.route('/states/<states_id>', methods=["POST"], strict_slashes=False)
def post_states():
    """
    Post to states
    """
    state = request.get_json()
    if not state:
        return ("Not a JSON", 400)
    if state.get("name") is None:
        return (abort(400, "Missing name"))
    add_state = State(state)
    add_state.save()
    state_tojson = storage.get("State", add_state.id).to_json()
    return (jsonify(state_tojson))

@app_views.route('/states/<states_id>/', methods=["PUT"], strict_slashes=False)
def put_states(states_id):
    """
    Update states
    """
    r = request.get_json()
    if r is None:
        abort(400)
    state = storage.get("State", states_id)
    if state is None:
        abort(404)
    for k, v in r.items():
        if k != "id" and k != "created_at" and k != "updated_at":
            setattr(state, k, v)
    state.save()
    state_tojson = state.to_json()
    return (jsonify(state_tojson), 200)

@app_views.route('/states/<states_id>/', methods=["DELETE"], strict_slashes=False)
def delete_states(states_id):
    """
    Deletes states
    """
    state = storage.get("State", states_id)
    if state is None:
        abort(404)
    storage.delete(state)
    return (jsonify({}), 200)
