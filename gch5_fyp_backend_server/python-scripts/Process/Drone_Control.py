# This file contains the function to Simulate the drone movement and the rssi value of the drone
from shared_state import current_drone_location
import time

# This function is used to calculate the distance between two points
def distance(point1, point2):
    return ((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2) ** 0.5

# This function is used to simulate the drone movement
def fly_to_point(point):
    speed = 30  # Speed in m/s
    update_interval = 0.1  # Update interval in seconds
    while True:
        distance_to_travel = distance(current_drone_location, point)
        if distance_to_travel <= 0.01:  # Assume arrival when the distance is very small
            break
        
        fraction_to_move = min(1, speed * update_interval / distance_to_travel)
        current_drone_location[0] += (point[0] - current_drone_location[0]) * fraction_to_move
        current_drone_location[1] += (point[1] - current_drone_location[1]) * fraction_to_move

        time.sleep(update_interval)
