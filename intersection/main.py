#!/usr/bin/env python

import os
import sys
import random
from math import sqrt

if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("Please declare environment variable 'SUMO_HOME'")
import traci
from plexe import Plexe, ACC, CACC

# some basic configuration taken according to research paper, can vary
VEHICLE_LENGTH = 4
DISTANCE = 6
LANE_NUM = 12
PLATOON_SIZE = 1
SPEED = 16.6
ADD_PLATOON_PRO = 0.3
ADD_PLATOON_STEP = 600
MAX_ACCEL = 2.6
STOP_LINE = 15.0

# defined 11 routes in rou.xml. for each, there can be certain conflict routes, defined that here to manage it.
conflict_matrix = {
    0: [],
    1: [4, 8, 10, 11],
    2: [4, 5, 7, 11],
    3: [],
    4: [1, 2, 7, 11],
    5: [2, 7, 8, 10],
    6: [],
    7: [2, 4, 5, 10],
    8: [1, 5, 10, 11],
    9: [],
    10: [1, 5, 7, 8],
    11: [1, 2, 4, 8]
}
# using plexe to add vehicles and tune platooning parameters
def add_single_platoon(plexe, step, lane):
    for i in range(PLATOON_SIZE):
        vid = f"v.{step/ADD_PLATOON_STEP}.{lane}.{i}"
        routeID = f"route_{lane}"
        traci.vehicle.add(vid, routeID, departPos=str(100-i*(VEHICLE_LENGTH+DISTANCE)),
                          departSpeed=str(5), departLane=str(lane%3), typeID="vtypeauto")
        plexe.set_path_cacc_parameters(vid, DISTANCE, 2, 1, 0.5)
        plexe.set_cc_desired_speed(vid, SPEED)
        plexe.set_acc_headway_time(vid, 1.5)
        plexe.use_controller_acceleration(vid, False)
        plexe.set_fixed_lane(vid, lane%3, False)
        traci.vehicle.setSpeedMode(vid, 0)
        if i == 0:
            plexe.set_active_controller(vid, ACC)
            traci.vehicle.setColor(vid, (255, 255, 255, 255))
        else:
            plexe.set_active_controller(vid, CACC)
            traci.vehicle.setColor(vid, (200, 200, 0, 255))

def add_platoons(plexe, step):
    for lane in range(LANE_NUM):
        if random.random() < ADD_PLATOON_PRO:
            add_single_platoon(plexe, step, lane)

# orignial paper had v2i communication and this is implemented with minimal communication
def communicate(plexe, topology):
    # Placeholder for a simplified communicate function
    pass
mian function which adds platoons at specific intervals
def main():
    sumo_cmd = ['sumo-gui', '--duration-log.statistics', '--tripinfo-output', 'my_output_file.xml',
                '-c', 'cfg/intersection.sumo.cfg']
    traci.start(sumo_cmd)
    plexe = Plexe()
    traci.addStepListener(plexe)

    step = 0
    topology = {}

    while step < 360000:
        traci.simulationStep()

        if step % ADD_PLATOON_STEP == 0:
            add_platoons(plexe, step)

        step += 1

        if step % 10 == 1:
            communicate(plexe, topology)  # Placeholder for the communicate function

    traci.close()

if __name__ == "__main__":
    main()
