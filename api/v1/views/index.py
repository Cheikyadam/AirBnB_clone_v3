#!/usr/bin/python3
"""Index page"""
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status')
def func():
    """Return status"""
    return jsonify({'status': 'OK'})


@app_views.route('/stats')
def stat():
    """Return stats"""
    modstats = {}
    modstats['amenities'] = storage.count("Amenity")
    modstats['cities'] = storage.count("City")
    modstats['places'] = storage.count("Place")
    modstats['reviews'] = storage.count("Review")
    modstats['states'] = storage.count("State")
    modstats['users'] = storage.count("User")
    return jsonify(modstats)
