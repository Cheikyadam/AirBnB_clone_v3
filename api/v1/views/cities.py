#!/usr/bin/python3
"""Index page"""
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.city import City
from models.state import State
from flask import abort, request
from flask import make_response


@app_views.route('/states/<state_id>/cities/', methods=['GET'])
def get_cities(state_id):
    """Return all states"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    cities = state.cities
    citiesdic = [city.to_dict() for city in cities]
    return jsonify(citiesdic)


@app_views.route('/cities/<city_id>', methods=['GET'])
def get_city(city_id):
    """Return a city"""
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'])
def del_city(city_id):
    """delete a city"""
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states//<state_id>/cities', methods=['POST'])
def post_cities():
    """Add a city"""
    try:
        data = request.get_json()
        if 'name' in data:
            state = storage.get("State", state_id)
            if state is None:
                abort(404)
            city = City(**data)
            city.state_id = state.id
            city.save()
            storage.save()
            return make_response(jsonify(city.to_dict()), 201)
        return make_response(jsonify({'error': 'Missing name'}), 400)
    except Exception as e:
        return make_response(jsonify({'error': 'Not a json'}), 400)


@app_views.route('/cities/<city_id>', methods=['PUT'])
def put_cities(city_id):
    """upd a city"""
    try:
        data = request.get_json()
        city = storage.get(City, city_id)
        if city is None:
            abort(404)
        for key, value in data.items():
            if key not in ['id', 'state_id', 'created_at', 'updated_at']:
                setattr(city, key, value)
        city.save()
        storage.save()
        return make_response(jsonify(city.to_dict()), 200)
    except Exception as e:
        return make_response(jsonify({'error': 'Not a json'}), 400)
