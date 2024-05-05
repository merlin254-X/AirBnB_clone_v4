#!/usr/bin/python3
'''View for State objects with RESTful API endpoints'''

from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.state import State

# Retrieve all State objects


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    '''Retrieve all State objects'''
    states = storage.all(State).values()
    return jsonify([state.to_dict() for state in states])

# Retrieve a specific State object by ID


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state_by_id(state_id):
    '''Retrieve a State object by ID'''
    state = storage.get(State, state_id)
    if not state:
        abort(404, 'State not found')
    return jsonify(state.to_dict())

# Create a new State object


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    '''Create a new State object'''
    data = request.get_json(silent=True)
    if not data:
        abort(400, 'Not a JSON')
    if 'name' not in data:
        abort(400, 'Missing name')
    new_state = State(name=data['name'])
    storage.new(new_state)
    storage.save()
    return jsonify(new_state.to_dict()), 201

# Update a specific State object by ID


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    '''Update a State object'''
    data = request.get_json(silent=True)
    if not data:
        abort(400, 'Not a JSON')
    state = storage.get(State, state_id)
    if not state:
        abort(404, 'State not found')
    ignore_keys = ['id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(state, key, value)
    state.save()
    return jsonify(state.to_dict()), 200

# Delete a State object by ID


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    '''Delete a State object'''
    state = storage.get(State, state_id)
    if not state:
        abort(404, 'State not found')
    storage.delete(state)
    storage.save()
    return jsonify({}), 200
