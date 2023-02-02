from flask import Blueprint, request, jsonify
from drone_inventory.helpers import token_required, random_joke_generator
from drone_inventory.models import db, Drone, drone_schema, drones_schema


api = Blueprint('api', __name__, url_prefix = '/api')

# @api.route('getdata', methods= ['GET'])
@api.route('/getdata')
@token_required 
def getdata(our_user):
    return{'some': 'value'}

#creat drone endpoint

@api.route('/drones', methods = ['POST'])
@token_required
def create_drone(our_user):
    name = request.json['name']
    description = request.json['description']
    price = request.json['price']
    camera_quality = request.json['camera_quality']
    flight_time = request.json['flight_time']
    max_speed = request.json['max_speed']
    dimensions = request.json['dimensions']
    weight = request.json['weight']
    cost_of_production = request.json['cost_of_production']
    series = request.json['series']
    random_joke = random_joke_generator()
    user_token = our_user.token

    print(f"user Token: {our_user.token})")

    drone = Drone(name, description, price, camera_quality, flight_time, max_speed, dimensions, weight, cost_of_production, series, random_joke, user_token = user_token)

    db.session.add(drone)
    db.session.commit()

    response = drone_schema.dump(drone)
    return jsonify(response)
@api.route('/drones/<id>', methods = ['GET'])
@token_required
def get_drone(our_user, id):
    owner = our_user.token
    if owner == our_user.token:
        drone = Drone.query.get(id)
        response = drone_schema.dump(drone)
        return jsonify(response)
    else:
        return jsonify({'message' : 'balid id Required'}), 401
    
@api.route('/drones/<id>' , methods = ['PUT', 'POST'])
@token_required
def update_drone(our_user, id):
    drone = Drone.query.get(id)
    drone.description = request.json['description']
    drone.price = request.json['price']
    drone.camera_quality = request.json['camera_quality']
    drone.flight_time = request.json['flight_time']
    drone.max_speed = request.json['max_speed']
    drone.dimensions = request.json['dimensions']
    drone.weight = request.json['weight']
    drone.cost_of_production = request.json['cost_of_production']
    drone.series = request.json['series']
    drone.user_token = our_user.token

    db.session.commit()
    response = drone_schema.dump(drone)
    return jsonify(response)

# RETRIEVE ALL DRONEs ENDPOINT
@api.route('/drones', methods = ['GET'])
@token_required
def get_drones(current_user_token):
    owner = current_user_token.token
    drones = Drone.query.filter_by(user_token = owner).all()
    response = drones_schema.dump(drones)
    return jsonify(response)

@api.route('/drones/<id>', methods = ['DELETE'])
@token_required
def delete_drones(our_user, id):
    drone = Drone.query.get(id)
    db.session.delete(drone)
    db.session.commit()

    response = drone_schema.dump(drone)
    return jsonify(response)