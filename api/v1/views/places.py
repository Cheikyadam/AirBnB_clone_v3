#!/usr/bin/python3
"""Index page"""
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.user import User
from models.place import Place
from flask import abort, request
from flask import make_response


@app_views.route('/cities/<city_id>/places', methods=['GET'])
def get_places(city_id):
    """Return all places of a city"""
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    places = city.places
    placesdic = [place.to_dict() for place in places]
    return jsonify(placesdic)


@app_views.route('/places/<place_id>', methods=['GET'])
def get_place(place_id):
    """Return a place"""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'])
def del_place(place_id):
    """Delcan a place"""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/cities/<city_id>/places', methods=['POST'])
def post_place(city_id):
    """Add a new place"""
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    try:
        data = request.get_json()
        if 'user_id' not in list(data.keys()):
            return make_response(jsonify({'error': 'Missing user_id'}), 400)
        user = storage.get("User", data.get("user_id"))
        if user is None:
            abort(404)
        if 'name' not in list(data.keys()):
            return make_response(jsonify({'error': 'Missing name'}), 400)
        place = Place(**data)
        place.save()
        return make_response(jsonify(place.to_dict()), 201)
    except Exception as e:
        return make_response(jsonify({'error': 'Not a json'}), 400)


@app_views.route('/places/<place_id>', methods=['PUT'])
def put_place(place_id):
    """upd a place"""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    try:
        data = request.get_json()
        lista = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
        for key, value in data.items():
            if key not in lista:
                setattr(place, key, value)
        place.save()
        storage.save()
        return make_response(jsonify(place.to_dict()), 200)
    except Exception as e:
        return make_response(jsonify({'error': 'Not a json'}), 400)
