# The code uses to transfer between the latitude and longitude coordinates and the x and y coordinates is as follows:
import math

# Earth's radius 
R = 6371000

# Input: Latitude and longitude of point, latitude and longitude of starting point
# Output: x and y coordinates of the point
def ll2xy(lon, lat, start_lon, start_lat):
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

# Input: x and y coordinates of point, latitude and longitude of starting point
# Output: Latitude and longitude of the point
def xy2ll(x, y, start_lon, start_lat):
    # Convert back to latitude and longitude
    start_lat_rad = math.radians(start_lat)
    lat = y / R + start_lat
    lon = x / (R * math.cos(start_lat_rad)) + start_lon
    return lon, lat

# NOT USED NOW
# Input: x and y coordinates of starting point, x and y coordinates of destination point
# Output: Direction and distance from starting point to destination point
def xy2direction(x1, y1, x2, y2):
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

# # Example usage
# start_lon, start_lat = 114.268, 22.337 
# lon, lat =  114.269, 22.33826

# x, y = ll2xy(lon, lat, start_lon, start_lat)
# print(f"X, Y Coordinates: {x}, {y}")

# back_lon, back_lat = xy2ll(x, y, start_lon, start_lat)
# print(f"Back to Lontitude: {back_lon}, Back to Latitude: {back_lon}")

# # x1, y1 = 0, 0  # Starting point
# # x2, y2 = x, y  # Destination point
# # direction, distance = xy2direction(x1, y1, x2, y2)
# # print(f"Direction: {direction} degrees, Distance: {distance} meters")

# x3, y3 = 50, 50  # Another point
# lon3 , lat3 = xy2ll(x3, y3, start_lon, start_lat)
# print(f"Lat, Lon of (50, 50): {lon3}, {lat3}")
