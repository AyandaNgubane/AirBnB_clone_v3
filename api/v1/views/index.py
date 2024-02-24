#!/usr/bin/python3
"""First file"""
from api.v1.views import app_views
from flask import jsonify
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models import storage


@app_views.route('/status')
def status():
    """Returns status"""
    return jsonify({"status": "OK"})


@app_views.route('/stats')
def total_objects():
    """ Retrieves the number of each objects by type """
    classes = [Amenity, City, Place, Review, State, User]
    cls_names = ["amenities", "cities", "places", "reviews", "states", "users"]

    tot_objs = {}
    for i in range(len(classes)):
        tot_objs[cls_names[i]] = storage.count(classes[i])

    return jsonify(tot_objs)
