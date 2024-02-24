#!/usr/bin/python3
"""API endpoint"""
from models.state import State
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request


@app_views.route('/states')
def retrieve_states():
    """Retrieves the list of all State objects: GET /api/v1/states"""
    all_states = storage.all(State).values()
    list_states = []
    for state in all_states:
        list_states.append(state.to_dict())
    return jsonify(list_states)


@app_views.route('/states/<state_id>', methods=['GET', 'PUT', 'DELETE'])
def state_by_id(state_id):
    """Retrieves a State object: GET /api/v1/states/<state_id>
    If method is 'DELETE', deletes state
    If method is 'PUT', updates a state
    """
    if request.method == 'GET':
        state = storage.get(State, state_id)

        if not state:
            abort(404)

        return jsonify(state.to_dict())

    if request.method == 'PUT':
        state = storage.get(State, state_id)
        if not state:
            abort(404)

        data = request.get_json()
        if not data:
            abort(400, description="Not a JSON")

        ignore = ['id', 'created_at', 'updated_at']

        for key, value in data.items():
            if key not in ignore:
                setattr(state, key, value)
        storage.save()

        return make_response(jsonify(state.to_dict()), 200)

    if request.method == 'DELETE':
        state = storage.get(State, state_id)
        if not state:
            abort(404)

        storage.delete(state)
        storage.save()

        return make_response(jsonify({}), 200)


@app_views.route('/states', methods=['POST'])
def create_state():
    """Creates a State"""
    data = request.get_json()

    if not data:
        abort(400, description="Not a JSON")

    if 'name' not in data:
        abort(400, description="Missing name")

    state = State(**data)
    state.save()
    return make_response(jsonify(state.to_dict()), 201)
