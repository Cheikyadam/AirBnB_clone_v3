#!/usr/bin/python3
"""Index page"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status')
def func():
    """Return status"""
    return jsonify({'status': 'OK'})
