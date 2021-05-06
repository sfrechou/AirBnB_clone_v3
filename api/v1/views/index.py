#!/usr/bin/python3
"""blueprint"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status')
def show():
    """that returns a JSON status"""
    return jsonify(status='OK')