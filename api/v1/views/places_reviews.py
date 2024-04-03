#!/usr/bin/python3
"""Index page"""
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.user import User
from models.place import Place
from models.review import Review
from flask import abort, request
from flask import make_response


@app_views.route('/places/<place_id>/reviews', methods=['GET'])
def get_reviews(place_id):
    """Return all reviews of a place"""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    reviews = place.reviews
    reviewsdic = [review.to_dict() for review in reviews]
    return jsonify(reviewsdic)


@app_views.route('/reviews/<review_id>', methods=['GET'])
def get_review(review_id):
    """Return a review"""
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'])
def del_review(review_id):
    """Del a review"""
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)
    storage.delete(review)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/places/<place_id>/reviews', methods=['POST'])
def post_review(place_id):
    """Add a new review"""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    try:
        data = request.get_json()
        if 'user_id' not in list(data.keys()):
            return make_response(jsonify({'error': 'Missing user_id'}), 400)
        user = storage.get("User", data.get("user_id"))
        if user is None:
            abort(404)
        if 'text' not in list(data.keys()):
            return make_response(jsonify({'error': 'Missing text'}), 400)
        review = Review(**data)
        review.save()
        return make_response(jsonify(review.to_dict()), 201)
    except Exception as e:
        return make_response(jsonify({'error': 'Not a json'}), 400)


@app_views.route('/reviews/<review_id>', methods=['PUT'])
def put_review(review_id):
    """upd a review"""
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)
    try:
        data = request.get_json()
        lista = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
        for key, value in list(data.items()):
            if key not in lista:
                setattr(review, key, value)
        review.save()
        storage.save()
        return make_response(jsonify(review.to_dict()), 200)
    except Exception as e:
        return make_response(jsonify({'error': 'Not a json'}), 400)
