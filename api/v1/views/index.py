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
    stats = {
        "Amenity": "amenities",
        "City": "cities",
        "Place": "places",
        "Review": "reviews",
        "State": "states",
        "User": "users"
    }
    return jsonify({name: storage.count(cls) for cls, name in stats.items()})
