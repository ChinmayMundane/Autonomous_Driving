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
    world = client.get_world()
    map = world.get_map()
    spawn_points = map.get_spawn_points()

    # Choose a spawn location
    spawn_point = carla.Transform(carla.Location(x=100, y=200, z=50), carla.Rotation(pitch=0, yaw=0, roll=0))

    tesla_vehicle = None
    max_retries = 5  # Adjust the number of retries as needed
    tesla_vehicle = client.get_world().try_spawn_actor(blueprints[0], spawn_points[0])

    # Attempt to spawn the Tesla vehicle with collision checks
    # for _ in range(max_retries):
    #     tesla_vehicle = client.get_world().try_spawn_actor(blueprints[0], spawn_point)
    #     if tesla_vehicle:
    #         break
    spect = world.get_spectator()
    spect.set_transform(tesla_vehicle.get_transform())
    # Control the Tesla vehicle (example: full throttle)
    control = carla.VehicleControl()
    control.throttle = 1.0
    tesla_vehicle.apply_control(control)

    # Define the time to run the simulation (adjust as needed)
    simulation_time = 10.0  # seconds
    current_time = 0.0
    
    while current_time < simulation_time:
        client.get_world().tick()
        current_time += 1.0 / 60.0  # Assuming a 60Hz simulation rate

finally:
    # Cleanup
    if tesla_vehicle is not None:
        tesla_vehicle.destroy()

# Disconnect from CARLA
client.disconnect()
