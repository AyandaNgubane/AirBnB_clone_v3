#!/usr/bin/python3
""" city view """
from api.v1.views import app_views
from flask import jsonify, make_response, abort, request
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities', methods=["GET", "POST"],
                 strict_slashes=False)
def retreive_cities(state_id):
    """If method is 'GET',
    Retrieves the list of all City objects of a State:
        GET /api/v1/states/<state_id>/cities
    If method is 'POST', create city
    """
    city_list = []
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if request.method == 'GET'
        for city in state.cities:
            city_list.append(city.to_dict())
        return (jsonify(city_list))
    if request.method == 'POST':
        data = request.get_json()
        if not request.is_json:
            abort(400, description="Not a JSON")
        if 'name' not in request.json:
            abort(400, description="Missing name")
        data['state_id'] = state_id
        city = City(**data)
        city.save()
        return (jsonify(city.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=["GET", "PUT"],
                 strict_slashes=False)
def city_by_id(city_id):
    """If method is 'GET',
    Retrieves a City object: GET /api/v1/cities/<city_id>.
    If method is 'PUT', updates state.
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if request.method == "GET":
        result = city.to_dict()
        return (jsonify(result))
    if request.method == "PUT":
        data = request.get_json()
        if not request.is_json:
            abort(400, description="Not a JSON")
        for key, value in data.items():
            setattr(city, key, value)
        city.save()
        return (jsonify(city.to_dict()), 200)


@app_views.route('/cities/<city_id>', methods=["GET", "DELETE"],
                 strict_slashes=False)
def delete_city(city_id):
    """Deletes city as per id"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    result = make_response(jsonify({}), 200)
    return result
