#!/usr/bin/python3
""" place view """
from api.v1.views import app_views
from flask import jsonify, make_response, abort, request
from models import storage
from models.base_model import BaseModel
from models.place import Place
from models.city import City
from models.user import User


@app_views.route('/cities/<city_id>/places', methods=["GET", "POST"],
                 strict_slashes=False)
def retreive_places(city_id):
    """If method is 'GET',
    Retrieves the list of all Place objects of a City:
        GET /api/v1/cities/<city_id>/places
    If method is 'POST', create place
    """
    place_list = []
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if request.method == "GET":
        for place in city.places:
            place_list.append(place.to_dict())
        return (jsonify(place_list))
    if request.method == "POST":
        data = request.get_json()
        if not request.is_json:
            abort(400, description="Not a JSON")
        if 'user_id' not in request.json:
            abort(400, description="Missing user_id")
        user_id = data['user_id']
        user = storage.get(User, user_id)
        if User is None:
            abort(404)
        if 'name' not in request.json:
            abort(400, description="Missing name")
        data['city_id'] = city_id
        place = Place(**data)
        place.save()
        return (jsonify(place.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=["GET", "PUT", "DELETE"],
                 strict_slashes=False)
def place_by_id(city_id):
    """If method is 'GET',
    Retrieves a Place object: GET /api/v1/places/<place_id>.
    If method is 'PUT', updates place.
    if method is 'DELETE', deletes place.
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if request.method == "GET":
        result = place.to_dict()
        return (jsonify(result))
    if request.method == "PUT":
        data = request.get_json()
        if not request.is_json:
            abort(400, description="Not a JSON")
        for key, value in data.items():
            setattr(place, key, value)
        place.save()
        return (jsonify(place.to_dict()), 200)
    if request.method == "DELETE":
        storage.delete(place)
        storage.save()
        result = make_response(jsonify({}), 200)
        return result
