#!/usr/bin/env python

import glob
import os
import sys

try:
    sys.path.append(glob.glob('../carla/dist/carla-*%d.%d-%s.egg' % (
        sys.version_info.major,
        sys.version_info.minor,
        'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
except IndexError:
    pass

import carla

# Connect to CARLA simulator
client = carla.Client('localhost', 2000)
client.set_timeout(20.0)


try:
    # Load Tesla blueprint
    blueprints = client.get_world().get_blueprint_library().filter('model3')
    
    if not blueprints:
        raise RuntimeError("Tesla blueprint not found in CARLA")

    # Choose a spawn location
    spawn_point = carla.Transform(carla.Location(x=100, y=200, z=50), carla.Rotation(pitch=0, yaw=0, roll=0))

    # Spawn Tesla vehicle
    tesla_vehicle = client.get_world().spawn_actor(blueprints[0], spawn_point)

    # Calculate desired speed for 20 meters ahead 
    distance_to_cover = 20.0  # meters
    desired_speed = distance_to_cover / 5.0  # Adjust the divisor for desired time of travel

    # Control the Tesla vehicle
    control = carla.VehicleControl()
    control.throttle = 0.5 
    tesla_vehicle.apply_control(control)

    # Monitor the vehicle's position to determine when it has covered the desired distance
    initial_location = tesla_vehicle.get_location()
    current_location = initial_location
    while current_location.distance(initial_location) < distance_to_cover:
        current_location = tesla_vehicle.get_location()

    # Stop the vehicle
    control.throttle = 0.0
    tesla_vehicle.apply_control(control)

finally:
    # Cleanup
    if 'tesla_vehicle' in locals():
        tesla_vehicle.destroy()

# Disconnect from CARLA
client.disconnect()
