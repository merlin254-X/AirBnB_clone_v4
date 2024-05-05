#!/usr/bin/python3
"""
view for Place objects that handles all
default RESTful API actions in Flask
"""

from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.city import City
from models.place import Place
from models.user import User


# Get all places for a given city
@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_places_by_city(city_id):
    '''Retrieve all Place objects for a given city'''
    city = storage.get(City, city_id)
    if not city:
        abort(404, 'City not found')
    places = city.places
    return jsonify([place.to_dict() for place in places])

# Get a specific place by ID


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place_by_id(place_id):
    '''Retrieve a Place object by ID'''
    place = storage.get(Place, place_id)
    if not place:
        abort(404, 'Place not found')
    return jsonify(place.to_dict())

# Create a new place for a given city


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    '''Create a new Place object for a given city'''
    city = storage.get(City, city_id)
    if not city:
        abort(404, 'City not found')

    data = request.get_json(silent=True)
    if not data:
        abort(400, 'Not a JSON')
    if 'user_id' not in data:
        abort(400, 'Missing user_id')
    if 'name' not in data:
        abort(400, 'Missing name')

    user = storage.get(User, data['user_id'])
    if not user:
        abort(404, 'User not found')

    new_place = Place(name=data['name'], user_id=data['user_id'],
                      city_id=city_id)
    storage.new(new_place)
    storage.save()
    return jsonify(new_place.to_dict()), 201

# Update a specific place by ID


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    '''Update a Place object'''
    place = storage.get(Place, place_id)
    if not place:
        abort(404, 'Place not found')

    data = request.get_json(silent=True)
    if not data:
        abort(400, 'Not a JSON')

    ignore_keys = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(place, key, value)

    place.save()
    return jsonify(place.to_dict()), 200

# Delete a place by ID


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    '''Delete a Place object'''
    place = storage.get(Place, place_id)
    if not place:
        abort(404, 'Place not found')

    storage.delete(place)
    storage.save()
    return jsonify({}), 200
