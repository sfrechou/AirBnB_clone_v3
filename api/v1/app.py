#!/usr/bin/python3
"""Script that starts a Flask web application"""
from flask import Flask
from models import storage
from api.v1.views import app_views
from os import getenv
from flask import jsonify

app = Flask(
    __name__,
)
app.register_blueprint(app_views)


@app.errorhandler(404)
def not_found(error):
    """Handles 404 error"""
    return jsonify({'error': 'Not found'})

@app.teardown_appcontext
def teardown_db(exception):
    """Remove the current SQLAlchemy Session"""
    storage.close()

if __name__ == "__main__":
    if getenv('HBNB_API_HOST'):
        host = getenv('HBNB_API_HOST')
    else:
        host = '0.0.0.0'
    if getenv('HBNB_API_PORT'):
        port = getenv('HBNB_API_PORT')
    else:
        port = '5000'
    app.run(host=host, port=port, threaded=True)
