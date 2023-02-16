#!/usr/bin/python3
""" New view for Place that handles all default RESTful API actions"""
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
import json
from models import storage, storage_t
from models.place import Place
from models.city import City
from models.user import User
from models.amenity import Amenity


@app_views.route('/places/<place_id>/amenities', methods=['GET'])
def amenity_list(place_id):
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    if request.method == 'GET' and storage_t == 'db':
        return jsonify([amenity.to_dict() for amenity in place.amenities])

    elif request.method == 'GET' and storage_t != 'db':
        return jsonify(place.amenity_ids)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE', 'POST'])
def amenity_id(place_id, amenity_id):
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)

    if amenity not in place.amenities:
        abort(404)

    if request.method == 'DELETE':
        if storage_t == 'db':
            place.amenities.remove(amenity)

        elif storage_t != 'db':
            place.amenity_ids.remove(amenity.id)

        return make_response(jsonify({}), 200)

    elif request.method == 'POST':
        if storage_t == 'db':
            if amenity in places.amenities:
                return make_response(jsonify(amenity.to_dict()), 200)
            else:
                place_link = place_amenity('place_id'=place_id,
                                           'amenity_id'=amenity_id)
                place_link.amenity = Amenity(name=amenity.name)
                place.amenities.append(place_link)
                place.save()
            return make_response(jsonify(amenity.to_dict()), 200)
        else:
            place.amenity_ids.append(amenity_id)
            return make_response(jsonify(amenity.to_dict()), 200)
