#!/usr/bin/python3
'''api status'''
import models
from models import storage
from models.base_model import BaseModel
from flask import jsonify
from api.v1.views import app_views


@app_views.route('/status', strict_slashes=False)
def returnstuff():
    '''return stuff'''
    return jsonify(status='OK')


@app_views.route('/stats', strict_slashes=False)
def get_stats():
    """Returns a JSON object with the count of different data models."""
    counts = {
        'states': State,
        'users': User,
        'amenities': Amenity,
        'cities': City,
        'places': Place,
        'reviews': Review
    }
    # Update each entry with the count from the database
    for key in counts:
        counts[key] = storage.count(counts[key])
    return jsonify(counts)
