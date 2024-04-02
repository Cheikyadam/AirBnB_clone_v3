#!/usr/bin/python3
"""Index page"""
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.city import City
from models.state import State
from flask import abort, request
from flask import make_response


@app_views.route('/amenities', methods=['GET'])
def get_amenities():
    """Return all amnes"""
    amens = storage.all("Amenity").values()
    amensdic = [am.to_dict() for am in amens]
    return jsonify(amensdic)


@app_views.route('/amenities/<amenity_id>', methods=['GET'])
def get_amen(am_id):
    """Return an am"""
    amen = storage.get("Amenity", am_id)
    if amen is None:
        abort(404)
    return jsonify(amen.to_dict())
