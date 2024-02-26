#!/usr/bin/python3
""" Flask Application """

from models import storage
from api.v1.views import app_views
from flask import Flask, render_template, make_response, jsonify
from os import environ
from flask_cors import CORS

app = Flask(__name__)
app.register_blueprint(app_views, url_prefix="/api/v1")
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def close_storage(exception):
    """ Close Storage """
    storage.close()


@app.errorhandler(400)
def handle_400_error(e):
    """Handle 400 error"""
    message = jsonify({"error": e.description})
    return make_response(message, 400)


@app.errorhandler(404)
def not_found(error):
    """Handles 404 not found errors"""
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    host = environ.get('HBNB_API_HOST')
    port = environ.get('HBNB_API_PORT')
    if not host:
        host = '0.0.0.0'
    if not port:
        port = '5000'
    app.run(host=host, port=port, threaded=True)
