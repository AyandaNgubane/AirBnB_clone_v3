#!/usr/bin/python3
"""First file"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status')
def status():
    """Returns status"""
    return jsonify({"status": "OK"})


@app_views.route('/stats')
def total_objects():
    """ Retrieves the number of each objects by type """
    classes = [Amenity, City, Place, Review, State, User]
    cls_names = ["amenities", "cities", "places", "reviews", "states", "users"]

    all_objs = {}
    for i in range(len(classes)):
        all_objs[cls_names[i]] = storage.count(classes[i])

    return jsonify(all_objs)
