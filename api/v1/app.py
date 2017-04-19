#!/usr/bin/python3
"""
starts app
"""
from api.v1.views import app_views
from flask import Blueprint
from flask import Flask
from flask import jsonify
from models import storage
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(self):
    """
    closes session
    """
    storage.close()

@app.errorhandler(404)
def not_found(error):
    """
    json 404 page
    """
    return (jsonify({"error": "Not found"}), 404)

if __name__ == "__main__":
    ip_used = getenv("HBNB_API_HOST", "0.0.0.0")
    port_used = getenv("HBNB_API_PORT", "5000")
    app.run(host=ip_used, port=port_used)
