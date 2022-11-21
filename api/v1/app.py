#!/usr/bin/python3
"""
variable app instance of flask
it contains method to handle @app.teardown_context
"""
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
import os
from flask_cors import CORS


app = Flask(__name__)
app.register_blueprint(app_views)
cors = CORS(app, resources={"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def teardown(exception):
    """teardown method meant for storage"""
    storage.close()


@app.errorhandler(404)
def error_404(exception):
    """ a handler for 404 errors that returns
    a JSON-formatted 404 status code response"""
    return jsonify(error="Not found"), 404


if __name__ == "__main__":
    app_host = os.getenv('HBNB_API_HOST')
    app_port = os.getenv('HBNB_API_PORT')
    if app_host is None:
        app_host = '0.0.0.0'
    if app_port is None:
        app_port = 5000
    app.run(host=app_host, port=int(app_port), threaded=True)
