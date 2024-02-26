#!/usr/bin/python3
""" amenity view """
from api.v1.views import app_views
from flask import jsonify, make_response, abort, request
from models import storage
from models.base_model import BaseModel
from models.amenity import Amenity


@app_views.route('/amenities', methods=["GET", "POST"],
                 strict_slashes=False)
def retreive_amenities():
    """If method is 'GET',
    Retrieves the list of all Amenity objects: GET /api/v1/amenities
    If method is 'POST', create amenity
    """
    amenity_list = []
    amenities = storage.all(Amenity).values()
    if request.method == "GET":
        for amenity in amenities:
            amenity_list.append(amenity.to_dict())
        return (jsonify(amenity_list))
    if request.method == "POST":
        data = request.get_json()
        if not request.is_json:
            abort(400, description="Not a JSON")
        if 'name' not in request.json:
            abort(400, description="Missing name")
        amenity = Amenity(**data)
        amenity.save()
        return (jsonify(amenity.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>', methods=["GET", "PUT", "DELETE"],
                 strict_slashes=False)
def amenity_by_id(amenity_id):
    """If method is 'GET',
    Retrieves a Amenity object: GET /api/v1/amenities/<amenity_id>.
    If method is 'PUT', updates amenity.
    if method is 'DELETE', deletes amenity.
    """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    if request.method == "GET":
        result = amenity.to_dict()
        return (jsonify(result))
    if request.method == "PUT":
        data = request.get_json()
        if not request.is_json:
            abort(400, description="Not a JSON")
        for key, value in data.items():
            setattr(amenity, key, value)
        amenity.save()
        return (jsonify(amenity.to_dict()), 200)
    if request.method == "DELETE":
        storage.delete(amenity)
        storage.save()
        result = make_response(jsonify({}), 200)
        return result
