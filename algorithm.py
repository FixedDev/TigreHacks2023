import math
import random
import csv
import numpy as np
import folium


class Point:
    def __init__(self, longitude: int, latitude: int):
        self.longitude = longitude
        self.latitude = latitude


class Shape:
    def is_in(self, point: Point):
        pass


def calculate_distance(lat1, lon1, lat2, lon2):
    """
    Calculate the distance between two coordinates using the Haversine formula.
    """
    radius = 6371  # Radius of the Earth in kilometers
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = radius * c
    return distance


def read_existing_coordinates(file_path):
    """
    Read existing coordinates from a CSV file.
    """
    existing_coordinates = []
    with open(file_path, 'r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # Skip the header line
        for row in csv_reader:
            lat, lon = map(float, row)
            existing_coordinates.append((lat, lon))
    return existing_coordinates


def generate_new_coordinates(existing_coordinates, num_points, min_distance):
    """
    Generate new coordinates near existing coordinates, satisfying the minimum distance constraint.
    """
    lat_min, lat_max = 25.5700, 25.8700
    lon_min, lon_max = -100.5200, -100.1000

    # Create a grid of points within the specified range
    lat_grid = np.linspace(lat_min, lat_max, num=100)
    lon_grid = np.linspace(lon_min, lon_max, num=100)
    grid_points = [(lat, lon) for lat in lat_grid for lon in lon_grid]

    new_coordinates = []

    while len(new_coordinates) < num_points and grid_points:
        # Randomly select a point from the grid
        index = random.randint(0, len(grid_points) - 1)
        lat, lon = grid_points[index]
        grid_points.pop(index)  # Remove the selected point from the grid

        is_valid = True

        # Check if the new coordinate satisfies the minimum distance constraint
        for coord in existing_coordinates:
            distance = calculate_distance(lat, lon, coord[0], coord[1])
            if distance < min_distance:
                is_valid = False
                break

        if is_valid:
            new_coordinates.append((lat, lon))
            existing_coordinates.append((lat, lon))  # Update existing coordinates with new ones

    return new_coordinates


# File path for the CSV with existing coordinates
csv_file_path = 'coordinates.csv'

# Read existing coordinates from the CSV file
existing_coordinates = read_existing_coordinates(csv_file_path)

# Generate new coordinates
num_points = 100
min_distance = 0.5  # Minimum distance in kilometers
new_coordinates = generate_new_coordinates(existing_coordinates, num_points, min_distance)

# Create a map centered on Monterrey
monterrey_map = folium.Map(location=[25.6866, -100.3161], zoom_start=12)

# Add existing coordinates to the map
for coord in existing_coordinates:
    folium.Marker(location=[coord[0], coord[1]], icon=folium.Icon(color='blue')).add_to(monterrey_map)

# Add new coordinates to the map
for coord in new_coordinates:
    folium.Marker(location=[coord[0], coord[1]], icon=folium.Icon(color='green')).add_to(monterrey_map)

# Save the map as an HTML file
monterrey_map.save('monterrey_coordinates_map.html')
