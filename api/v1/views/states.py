#!/usr/bin/python3
""" state view """
from api.v1.views import app_views
from flask import jsonify, make_response, abort, request
from models import storage
from models.base_model import BaseModel
from models.state import State


@app_views.route('/states', methods=["GET", "POST"], strict_slashes=False)
def retreive_states():
    """If method is 'GET',
    Retrieves the list of all State objects: GET /api/v1/states.
    If method is 'POST', creates state
    """
    if request.method == "GET":
        state_list = []
        states = storage.all(State).values()
        for state in states:
            state_list.append(state.to_dict())
        return (jsonify(state_list))
    if request.method == "POST":
        data = request.get_json()
        if not request.is_json:
            abort(400, description="Not a JSON")
        if 'name' not in request.json:
            abort(400, description="Missing name")
        state = State(**data)
        state.save()
        return (jsonify(state.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=["GET", "PUT", "DELETE"],
                 strict_slashes=False)
def state_by_id(state_id):
    """If method is 'GET',
    Retrieves a State object: GET /api/v1/states/<state_id>.
    If method is 'PUT', updates state.
    if method is 'DELETE', deletes state.
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if request.method == "GET":
        result = state.to_dict()
        return (jsonify(result))
    if request.method == "PUT":
        print("test\n")
        data = request.get_json()
        if not request.is_json:
            abort(400, description="Not a JSON")
        for key, value in data.items():
            setattr(state, key, value)
        state.save()
        return (jsonify(state.to_dict()), 200)
    if request.method == "DELETE":
        storage.delete(state)
        storage.save()
        result = make_response(jsonify({}), 200)
        return result
