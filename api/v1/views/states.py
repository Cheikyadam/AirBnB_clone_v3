#!/usr/bin/python3
"""Index page"""
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.state import State
from flask import abort, request
from flask import make_response


@app_views.route('/states/', methods=['GET'])
def get_states():
    """Return all states"""
    states = sorted(list(storage.all("State").values()), key=lambda x: x.name)
    statesdic = [state.to_dict() for state in states]
    return jsonify(statesdic)


@app_views.route('/states/<state_id>', methods=['GET'])
def get_state(state_id):
    """Return a state"""
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'])
def del_state(state_id):
    """delete a state"""
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states/', methods=['POST'])
def post_states():
    """Add a new state"""
    try:
        data = request.get_json()
        if 'name' in data:
            state = State(**data)
            state.save()
            storage.save()
            return make_response(jsonify(state.to_dict()), 201)
        return make_response(jsonify({'error': 'Missing name'}), 400)
    except Exception as e:
        return make_response(jsonify({'error': 'Not a json'}), 400)


@app_views.route('/states/<state_id>', methods=['PUT'])
def put_states(state_id):
    """upd a state"""
    try:
        data = request.get_json()
        state = storage.get(State, state_id)
        if state is None:
            abort(404)
        for key, value in data.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(state, key, value)
        state.save()
        storage.save()
        return make_response(jsonify(state.to_dict()), 200)
    except Exception as e:
        return make_response(jsonify({'error': 'Not a json'}), 400)
