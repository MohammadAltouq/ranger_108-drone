from flask import Blueprint, render_template, request, redirect,url_for
from flask_login import login_required, current_user
from drone_inventory.forms import DroneForm
from drone_inventory.models import Drone, db
# from drone_inventory.helpers import random_joke_generator

site = Blueprint('site', __name__ , template_folder = 'site_templates')


"""
Note that in the above code, some arguemnts are apecified when creating the 
Blueprint object, The first argument, 'site', is the Blueprint's name, This is used
by Flask's routing mechanism. The second argumenet, __name__,  is the Blueprint's import name,
which Flask uses to locate the Blueprint's resources
"""

@site.route('/')
def home():
    return render_template('index.html')
@site.route('/profile', methods =['GET', 'POST'])
@login_required
def profile():
    my_drone = DroneForm()
    try:
        if request.method == 'POST' and my_drone.validate_on_submit():
            name = my_drone.name.data
            description = my_drone.description.data
            price = my_drone.price.data
            camera_quality = my_drone.camera_quality.data
            flight_time = my_drone.flight_time.data
            max_speed = my_drone.max_speed.data
            dimensions = my_drone.dimensions.data
            weight = my_drone.weight.data
            cost_of_production = my_drone.cost_of_production.data
            series = my_drone.series.data
            user_token = current_user.token

            drone = Drone(name, description, price, camera_quality, flight_time, max_speed, dimensions, weight, cost_of_production, series, user_token)

            db.session.add(drone)
            db.session.commit()

            return redirect(url_for('site.profile'))
    
    except:
        raise Exception('Drone not created, please check your form and try again!')
    user_token = current_user.token

    drones = Drone.query.filter_by(user_token = user_token)
    

    return render_template('profile.html', form = my_drone, drones = drones)
