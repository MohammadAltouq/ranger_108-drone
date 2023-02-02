from functools import wraps

import secrets
from flask import request, jsonify, json
from drone_inventory.models import User

import decimal
import requests 

def token_required(our_flask_function):
    @wraps(our_flask_function)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token'].split(' ')[1]
            print(token)

        if not token:
            return jsonify({'message': 'Token is missing'}), 401
        
        try:
            our_user = User.query.filter_by(token = token).first()
            print(our_user)
            if not our_user or our_user.token != token:
                return jsonify({'message:' 'Token is invalid'})
        except:
            owner = User.query.filter_by(token=token).first()
            if token != owner.token and secrets.compare_digest(token, owner.token):
                return jsonify({'message:' 'token is invalid'})
        return our_flask_function(our_user, *args, **kwargs)
    return decorated

def random_joke_generator():

    url = "https://random-stuff-api.p.rapidapi.com/joke/random"

    querystring = {"exclude":"dirty,money"}

    headers = {
        "Authorization": "wSTfjagR2UyF",
        "X-RapidAPI-Key": "SIGN-UP-FOR-KEY",
        "X-RapidAPI-Host": "random-stuff-api.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    data = response.json()
    return data['message']

# class JSONEncoder(json.JSONEncoder):
#     def default(self, obj):
#         if isinstance(obj, decimal.Decimal):
#             return str(obj)
#         return super(JSONEncoder, self).default(obj)
class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            #Convert decimal instances (numerics) into strings
            return str(obj)
        return super(JSONEncoder, self).default(obj)