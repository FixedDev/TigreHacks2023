import math
import random
import csv
import numpy as np
import folium
from folium import Polygon
from geopandas import *

class Point:
    def __init__(self, latitude: float, longitude: float):
        self.longitude = longitude
        self.latitude = latitude

    def __ge__(self, other):
        return other.longitude > self.longitude and other.latitude > self.latitude

    # scalar product
    def __mul__(self, other):
        return other.longitude * self.longitude + other.latitude * self.latitude

    def __eq__(self, other):
        return other.longitude == self.longitude and other.longitude == self.longitude

    def distance(self, other):
        """
          Calculate the distance between two coordinates using the Haversine formula.
          """
        radius = 6371  # Radius of the Earth in kilometers
        dlat = math.radians(other.latitude - self.latitude)
        dlon = math.radians(other.longitude - self.longitude)

        a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(self.latitude)) * math.cos(
            math.radians(other.latitude)) * math.sin(
            dlon / 2) ** 2

        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        distance = radius * c

        return distance


class Shape:
    def is_in(self, point: Point):
        pass


class RectangularShape(Shape):
    def __init__(self, point1: Point, point2: Point):
        self.point1 = point1 if point1 > point2 else point2
        self.point2 = point2 if self.point1 == point1 else point1

    def is_in(self, point: Point):
        return self.point1 >= point >= self.point2


class PolygonalShape(Shape):
    def __init__(self, points: list[Point]):
        self.points = points

    def fix(self):
        rectangle_polygon_geometry = self.asPolygon()

        for i in range(0, len(rectangle_polygon_geometry.get_bounds()) - 1):
            self.points[i] = Point(rectangle_polygon_geometry.get_bounds()[i][0],
                                   rectangle_polygon_geometry.get_bounds()[i][1])

    def asPolygon(self):
        points = [(point.latitude, point.longitude) for point in self.points]
        points.append((self.points[0].latitude, self.points[0].longitude))

        return Polygon(points)

    def is_in(self, point: Point):
        sides = len(self.points)
        j = sides - 1
        point_status = False

        for i in range(0, sides):
            if self.points[i].latitude < point.latitude <= self.points[j].latitude or \
                    self.points[j].latitude < point.latitude <= self.points[i].latitude:
                if self.points[i].longitude + (point.latitude - self.points[i].latitude) / (
                        self.points[j].latitude - self.points[i].latitude) * (
                        self.points[j].longitude - self.points[i].longitude) < point.longitude:
                    point_status = not point_status

            j = i

        return point_status


class FourPRectangularShape(PolygonalShape):
    def __init__(self, points: list[Point]):
        super().__init__(points)


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
            existing_coordinates.append(Point(lat, lon))
    return existing_coordinates


def generate_new_coordinates(existing_coordinates: list[Point], num_points, min_distance):
    """
    Generate new coordinates near existing coordinates, satisfying the minimum distance constraint.
    """
    min_point = Point(latitude=25.5700, longitude=-100.5200)
    max_point = Point(latitude=25.8700, longitude=-100.100)

    # Create a grid of points within the specified range
    lat_grid = np.linspace(min_point.latitude, max_point.latitude, num=100)
    lon_grid = np.linspace(min_point.longitude, max_point.longitude, num=100)

    grid_points: list[Point] = [Point(lat, lon) for lat in lat_grid for lon in lon_grid]

    new_coordinates: list[Point] = []

    while len(new_coordinates) < num_points and grid_points:
        # Randomly select a point from the grid
        index = random.randint(0, len(grid_points) - 1)
        point = grid_points[index]
        grid_points.pop(index)  # Remove the selected point from the grid

        is_valid = True

        # Check if the new coordinate satisfies the minimum distance constraint
        for coord in existing_coordinates:
            distance = point.distance(coord)
            if distance < min_distance:
                is_valid = False
                break

        if is_valid:
            new_coordinates.append(point)
            existing_coordinates.append(point)  # Update existing coordinates with new ones

    return new_coordinates


# File path for the CSV with existing coordinates
csv_file_path = 'coordinates.csv'

# Read existing coordinates from the CSV file
existing_coordinates = read_existing_coordinates(csv_file_path)

# Generate new coordinates
num_points = 1000
min_distance = .5  # Minimum distance in kilometers
new_coordinates = generate_new_coordinates(existing_coordinates, num_points, min_distance)

# Create a map centered on Monterrey
monterrey_map = folium.Map(location=[25.6866, -100.3161], zoom_start=12)

# Add existing coordinates to the map
for coord in existing_coordinates:
    folium.Marker(location=[coord.latitude, coord.longitude], icon=folium.Icon(color='blue')).add_to(monterrey_map)

# Add new coordinates to the map
for coord in new_coordinates:
    folium.Marker(location=[coord.latitude, coord.longitude], icon=folium.Icon(color='green')).add_to(monterrey_map)

rectangle.asPolygon().add_to(monterrey_map)

# Save the map as an HTML file
monterrey_map.save('monterrey_coordinates_map.html')

# Create a map for the new coordinates only
new_coordinates_map = folium.Map(location=[25.6866, -100.3161], zoom_start=12)

# Add new coordinates to the map
for coord in new_coordinates:
    folium.Marker(location=[coord.latitude, coord.longitude], icon=folium.Icon(color='green')).add_to(
        new_coordinates_map)

# Save the map with new coordinates as an HTML file
new_coordinates_map.save('new_coordinates_map.html')
