# The code uses to transfer between the latitude and longitude coordinates and the x and y coordinates is as follows:
# Input: Latitude and Longitude coordinates and starting point
# Output: x and y coordinates

import math

# Earth's radius 
R = 6371000

def ll2xy(lat, lon, start_lat, start_lon):

    # Convert latitude and longitude to radians
    lat_rad = math.radians(lat)
    start_lat_rad = math.radians(start_lat)
    # Calculate differences in coordinates
    delta_lat = lat - start_lat
    delta_lon = lon - start_lon
    # Approximate conversions using average latitude
    x = math.radians(delta_lon) * math.cos((start_lat_rad + lat_rad) / 2) * R
    y = math.radians(delta_lat) * R
    
    return x, y

def xy2ll(x, y, start_lat, start_lon):
    # Convert back to latitude and longitude
    start_lat_rad = math.radians(start_lat)
    lat = y / R + start_lat
    lon = x / (R * math.cos(start_lat_rad)) + start_lon
    
    return lat, lon

def xy2direction(x1, y1, x2, y2):
    # Calculate direction and distance
    delta_x = x2 - x1
    delta_y = y2 - y1
    angle_rad = math.atan2(delta_y, delta_x)
    angle_deg = math.degrees(angle_rad)
    distance = math.sqrt(delta_x**2 + delta_y**2)
    
    angle_deg = 90 - angle_deg  # Convert to compass bearings
    # Adjust angle to compass bearings
    if angle_deg < 0:
        angle_deg += 360
    
    return angle_deg, distance

# Example usage
start_lat, start_lon = 22.33826 , 114.26401
lat, lon =  22.33826, 114.37000

x, y = ll2xy(lat, lon, start_lat, start_lon)
print(f"X, Y Coordinates: {x}, {y}")

back_lat, back_lon = xy2ll(x, y, start_lat, start_lon)
print(f"Back to Lat, Lon: {back_lat}, {back_lon}")

x1, y1 = 0, 0  # Starting point
x2, y2 = x, y  # Destination point
direction, distance = xy2direction(x1, y1, x2, y2)
print(f"Direction: {direction} degrees, Distance: {distance} meters")