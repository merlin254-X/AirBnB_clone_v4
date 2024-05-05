#!/usr/bin/python3
"""iew for Review objects with all default RESTful API actions"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.review import Review
from models.user import User

# Get all reviews for a specific place


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_reviews_for_place(place_id):
    '''Retrieve all Review objects for a given place'''
    place = storage.get(Place, place_id)
    if not place:
        abort(404, 'Place not found')
    reviews = place.reviews
    return jsonify([review.to_dict() for review in reviews])

# Get a specific review by ID


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_review_by_id(review_id):
    '''Retrieve a Review object by ID'''
    review = storage.get(Review, review_id)
    if not review:
        abort(404, 'Review not found')
    return jsonify(review.to_dict())

# Delete a specific review by ID


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    '''Delete a Review object by ID'''
    review = storage.get(Review, review_id)
    if not review:
        abort(404, 'Review not found')
    storage.delete(review)
    storage.save()
    return jsonify({}), 200

# Create a new review for a specific place


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    '''Create a new Review object for a given place'''
    place = storage.get(Place, place_id)
    if not place:
        abort(404, 'Place not found')

    data = request.get_json(silent=True)
    if not data:
        abort(400, 'Not a JSON')
    if 'user_id' not in data:
        abort(400, 'Missing user_id')
    if 'text' not in data:
        abort(400, 'Missing text')

    user = storage.get(User, data['user_id'])
    if not user:
        abort(404, 'User not found')

    new_review = Review(user_id=data['user_id'],
                        place_id=place_id, text=data['text'])
    storage.new(new_review)
    storage.save()
    return jsonify(new_review.to_dict()), 201

# Update a review by ID


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    '''Update a Review object by ID'''
    review = storage.get(Review, review_id)
    if not review:
        abort(404, 'Review not found')

    data = request.get_json(silent=True)
    if not data:
        abort(400, 'Not a JSON')

    ignore_keys = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(review, key, value)

    review.save()
    return jsonify(review.to_dict()), 200
