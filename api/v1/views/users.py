#!/usr/bin/python3
"""Index page"""
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.user import User
from flask import abort, request
from flask import make_response


@app_views.route('/users', methods=['GET'])
def get_users():
    """Return all users"""
    users = storage.all("User").values()
    usersdic = [user.to_dict() for user in users]
    return jsonify(usersdic)


@app_views.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    """Return a user"""
    user = storage.get("User", user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'])
def del_user(user_id):
    """Delcan a user"""
    user = storage.get("User", user_id)
    if user is None:
        abort(404)
    storage.delete(user)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/users', methods=['POST'])
def post_user():
    """Add a new user"""
    try:
        data = request.get_json()
        if 'email' not in data:
            return make_response(jsonify({'error': 'Missing email'}), 400)
        if 'password' not in data:
            return make_response(jsonify({'error': 'Missing password'}), 400)
        user = User(**data)
        user.save()
        return make_response(jsonify(user.to_dict()), 201)
    except Exception as e:
        return make_response(jsonify({'error': 'Not a json'}), 400)


@app_views.route('/users/<user_id>', methods=['PUT'])
def put_user(user_id):
    """upd a user"""
    try:
        data = request.get_json()
        user = storage.get("User", user_id)
        if user is None:
            abort(404)
        for key, value in data.items():
            if key not in ['id', 'email', 'created_at', 'updated_at']:
                setattr(user, key, value)
        user.save()
        storage.save()
        return make_response(jsonify(user.to_dict()), 200)
    except Exception as e:
        return make_response(jsonify({'error': 'Not a json'}), 400)
