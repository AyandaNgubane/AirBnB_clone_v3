#!/usr/bin/python3
""" user view """
from api.v1.views import app_views
from flask import jsonify, make_response, abort, request
from models import storage
from models.base_model import BaseModel
from models.user import User


@app_views.route('/users', methods=["GET", "POST"], strict_slashes=False)
def retreive_users():
    """If method is 'GET',
    Retrieves the list of all User objects: GET /api/v1/users.
    If method is 'POST', creates user
    """
    if request.method == "GET":
        user_list = []
        users = storage.all(User).values()
        for user in users:
            user_list.append(user.to_dict())
        return (jsonify(user_list))
    if request.method == "POST":
        data = request.get_json()
        if not request.is_json:
            abort(400, description="Not a JSON")
        if 'name' not in request.json:
            abort(400, description="Missing name")
        user = User(**data)
        user.save()
        return (jsonify(user.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=["GET", "PUT", "DELETE"],
                 strict_slashes=False)
def user_by_id(user_id):
    """If method is 'GET',
    Retrieves a USER object: GET /api/v1/users/<user_id>.
    If method is 'PUT', updates user.
    If method is 'DELETE', deletes user
    """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    if request.method == "GET":
        result = user.to_dict()
        return (jsonify(result))
    if request.method == "PUT":
        data = request.get_json()
        if not request.is_json:
            abort(400, description="Not a JSON")
        for key, value in data.items():
            setattr(user, key, value)
        user.save()
        return (jsonify(user.to_dict()), 200)
    if request.method == "DELETE":
        storage.delete(user)
        storage.save()
        result = make_response(jsonify({}), 200)
        return result
