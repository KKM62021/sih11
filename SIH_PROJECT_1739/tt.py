import suncalc
from datetime import datetime

# Define the latitude, longitude, and date/time
y =int(input("enter year: "))
m = int(input("enter month: "))
d = int(input("enter date: "))
latitude = 23.0225
longitude = 72.5714
date_time = datetime(y, m, d, 13, 0)  # YYYY, MM, DD, HH, MM

# Get the sun position
sun_position = suncalc.get_position(date_time, latitude, longitude)

# Convert from radians to degrees
sun_azimuth = sun_position['azimuth'] * (180 / 3.14159)  # Azimuth in degrees
sun_elevation = sun_position['altitude'] * (180 / 3.14159)  # Altitude (elevation) in degrees

# Adjust azimuth to make 0 = north, 90 = east, 180 = south, 270 = west
sun_azimuth = (sun_azimuth + 180) % 360

print(f"Sun Azimuth: {sun_azimuth:.2f} degrees")
print(f"Sun Elevation: {sun_elevation:.2f} degrees")