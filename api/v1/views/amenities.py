#!/usr/bin/python3
"""Index page"""
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.amenity import Amenity
from flask import abort, request
from flask import make_response


@app_views.route('/amenities', methods=['GET'])
def get_amenities():
    """Return all amnes"""
    amens = storage.all("Amenity").values()
    amensdic = [am.to_dict() for am in amens]
    return jsonify(amensdic)


@app_views.route('/amenities/<amenity_id>', methods=['GET'])
def get_amen(amenity_id):
    """Return an am"""
    amen = storage.get("Amenity", amenity_id)
    if amen is None:
        abort(404)
    return jsonify(amen.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def del_amen(amenity_id):
    """Delcan am"""
    amen = storage.get("Amenity", amenity_id)
    if amen is None:
        abort(404)
    storage.delete(amen)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/amenities', methods=['POST'])
def post_amens():
    """Add a new amen"""
    try:
        data = request.get_json()
        if 'name' in list(data.keys()):
            amenity = Amenity(**data)
            amenity.save()
            storage.save()
            return make_response(jsonify(amenity.to_dict()), 201)
        return make_response(jsonify({'error': 'Missing name'}), 400)
    except Exception as e:
        return make_response(jsonify({'error': 'Not a json'}), 400)


@app_views.route('/amenities/<amenity_id>', methods=['PUT'])
def put_amens(amenity_id):
    """upd an amen"""
    try:
        data = request.get_json()
        amen = storage.get("Amenty", amenity_id)
        if amen is None:
            abort(404)
        for key, value in data.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(amen, key, value)
        amen.save()
        storage.save()
        return make_response(jsonify(amen.to_dict()), 200)
    except Exception as e:
        return make_response(jsonify({'error': 'Not a json'}), 400)
