#!/usr/bin/env python
# adding neccessary modules to run the script 
import glob
import os
import sys
import time


try:
    sys.path.append(glob.glob('../carla/dist/carla-*%d.%d-%s.egg' % (
        sys.version_info.major,
        sys.version_info.minor,
        'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
except IndexError:
    pass


import carla
import pygame

def get_world():
    # Connect to the Carla server
    client = carla.Client('localhost', 2000)
    client.set_timeout(10.0)

    # Get the Carla world
    world = client.get_world()
    return world

def spawn_vehicle(world):
    # Get the blueprint for a vehicle
    blueprint_library = world.get_blueprint_library()
    vehicle_bp = blueprint_library.filter('vehicle.*')[0]

    # Choose a spawn location (adjust as needed)
    spawn_location = carla.Transform(carla.Location(x=50, y=0, z=1), carla.Rotation())

    # Spawn the vehicle
    vehicle = world.try_spawn_actor(vehicle_bp, spawn_location)

    if vehicle is not None:
        print(f"Vehicle spawned with ID: {vehicle.id}")
    else:
        print("Failed to spawn a vehicle.")

    return vehicle

def setup_spectator(world, vehicle):
    # Set up the spectator camera on the vehicle
    spect = world.get_spectator()
    spect.set_transform(vehicle.get_transform())

def get_waypoint_at_location(world, location):
    # Get the closest waypoint to the specified location
    waypoint = world.get_map().get_waypoint(location)
    return waypoint

def main():
    # Get the Carla world
    world = get_world()

    # Spawn a vehicle
    vehicle = spawn_vehicle(world)

    if vehicle:
        # Set up the spectator camera on the vehicle
        setup_spectator(world, vehicle)

        try:
            # Initialize pygame for manual control
            pygame.init()
            clock = pygame.time.Clock()

            while True:
                clock.tick_busy_loop(60)

                # Get the location of the vehicle
                vehicle_location = vehicle.get_location()

                # Get the waypoint at the vehicle's location
                waypoint = get_waypoint_at_location(world, vehicle_location)

                if waypoint:
                    # Print the waypoint ID and location
                    print(f"Waypoint ID: {waypoint.id}, Location: {waypoint.transform.location}")
                else:
                    print("No waypoint found at the vehicle's location.")

                # Process keyboard events for manual control
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_UP:
                            vehicle.apply_control(carla.VehicleControl(throttle=1.0))
                        elif event.key == pygame.K_DOWN:
                            vehicle.apply_control(carla.VehicleControl(reverse=True, throttle=1.0))
                        elif event.key == pygame.K_LEFT:
                            vehicle.apply_control(carla.VehicleControl(steer=-1.0))
                        elif event.key == pygame.K_RIGHT:
                            vehicle.apply_control(carla.VehicleControl(steer=1.0))
                    elif event.type == pygame.KEYUP:
                        if event.key in [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]:
                            vehicle.apply_control(carla.VehicleControl())

        finally:
            # Destroy the vehicle actor when exiting the script
            if vehicle:
                vehicle.destroy()

if __name__ == '__main__':
    main()


