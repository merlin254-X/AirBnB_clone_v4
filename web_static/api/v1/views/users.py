#!/usr/bin/python3
"""RESTful API for managing User objects"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.user import User

# Get all users


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    '''Retrieve all User objects'''
    users = storage.all(User).values()
    return jsonify([user.to_dict() for user in users])

# Get a specific user by ID


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user_by_id(user_id):
    '''Retrieve a User object by ID'''
    user = storage.get(User, user_id)
    if not user:
        abort(404, 'User not found')
    return jsonify(user.to_dict())

# Create a new user


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    '''Create a new User object'''
    data = request.get_json(silent=True)
    if not data:
        abort(400, 'Not a JSON')
    if 'email' not in data:
        abort(400, 'Missing email')
    if 'password' not in data:
        abort(400, 'Missing password')
    new_user = User(email=data['email'], password=data['password'])
    storage.new(new_user)
    storage.save()
    return jsonify(new_user.to_dict()), 201

# Update a specific user by ID


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    '''Update a User object'''
    data = request.get_json(silent=True)
    if not data:
        abort(400, 'Not a JSON')
    user = storage.get(User, user_id)
    if not user:
        abort(404, 'User not found')
    ignore_keys = ['id', 'email', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(user, key, value)
    user.save()
    return jsonify(user.to_dict()), 200

# Delete a user by ID


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    '''Delete a User object'''
    user = storage.get(User, user_id)
    if not user:
        abort(404, 'User not found')
    storage.delete(user)
    storage.save()
    return jsonify({}), 200
