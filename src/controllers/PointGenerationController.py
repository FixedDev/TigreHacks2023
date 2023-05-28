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
    def isIn(self, point: Point):
        pass


class RectangularShape(Shape):
    def __init__(self, point1: Point, point2: Point):
        self.point1 = point1 if point1 > point2 else point2
        self.point2 = point2 if self.point1 == point1 else point1

    def isIn(self, point: Point):
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

    def isIn(self, point: Point):
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


def generate_new_coordinates(existing_coordinates: list[Point], num_points, min_distance, polygon_shape: Shape,
                             exclusion_zones: list[Shape]):
    """
    Generate new coordinates near existing coordinates, satisfying the minimum distance constraint and within the polygon shape.
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
        point = grid_points.pop(index)  # Remove the selected point from the grid

        is_valid = True

        # Check if the new coordinate satisfies the minimum distance constraint and is within the polygon shape
        for coord in existing_coordinates:
            distance = point.distance(coord)
            if distance < min_distance or not polygon_shape.isIn(point):
                is_valid = False
                break

        for zone in exclusion_zones:
            if zone.isIn(point):
                is_valid = False
                break

        if is_valid:
            new_coordinates.append(point)
            existing_coordinates.append(point)  # Update existing coordinates with new ones

    return new_coordinates


def createGridFromCsv(grid_shape: Shape, file_name: str, exclusion_zones=None):
    # Read existing coordinates from the CSV file
    existing_coordinates = read_existing_coordinates(file_name)

    if exclusion_zones is None:
        exclusion_zones = []

    return Grid(grid_shape, existing_coordinates, exclusion_zones)


class Grid:
    existing_coordinates: list[Point]
    generated_coordinates: list[Point]
    exclusion_zones: list[Shape]

    def __init__(self, grid_shape, existing_coordinates, exclusion_zones=None):
        self.shape = grid_shape
        self.existing_coordinates = existing_coordinates
        self.generated_coordinates = []
        self.points = 10
        self.distance = 1

        if exclusion_zones is None:
            exclusion_zones = []

        self.exclusion_zones = exclusion_zones

        self.__delete_outer_points()

    def add_point(self, point):
        for shape in self.exclusion_zones:
            if shape.isIn(point):
                return

        self.generated_coordinates.append(point)

    def __delete_outer_points(self):
        filtered = []

        for each in self.existing_coordinates:
            valid = True
            for shape in self.exclusion_zones:
                if shape.isIn(each):
                    valid = False
                    continue

            if self.shape.isIn(each) and valid:
                filtered.append(each)


        self.existing_coordinates = filtered

    def generatePoints(self):
        self.generated_coordinates = generate_new_coordinates(self.existing_coordinates, self.points, self.distance,
                                                              self.shape, self.exclusion_zones)


if __name__ == "__main__":
    # Define the vertices of the polygon that delimits the area
    polygon_vertices = [
        Point(25.766208153153272, -100.43999454010485),
        Point(25.635699380648006, -100.31497695176746),
        Point(25.685473638951752, -100.23876307237285),
        Point(25.743350522005148, -100.32698029875674),
        Point(25.790365318994212, -100.38332270726161)
    ]

    # Create a polygonal shape with the vertices
    polygon_shape = PolygonalShape(polygon_vertices)

    exclusion_zones = [
        PolygonalShape([
            Point(25.734548719536118, -100.32551269833463),
            Point(25.737766466019934, -100.28685011744324),
            Point(25.69668633929878, -100.30008784891619),
            Point(25.707099694757446, -100.33244674814051)
        ])
    ]

    grid = createGridFromCsv(polygon_shape, 'coordinates.csv', exclusion_zones)
    grid.points = 1000
    grid.distance = 0.5

    grid.generatePoints()

    # Create a map centered on Monterrey
    monterrey_map = folium.Map(location=[25.6866, -100.3161], zoom_start=12)

    # Add existing coordinates to the map
    for coord in grid.existing_coordinates:
        folium.Marker(location=[coord.latitude, coord.longitude], icon=folium.Icon(color='blue')).add_to(
            monterrey_map)

    # Add new coordinates within the polygon to the map
    for coord in grid.generated_coordinates:
        folium.Marker(location=[coord.latitude, coord.longitude], icon=folium.Icon(color='green')).add_to(monterrey_map)

    # Save the map as an HTML file
    monterrey_map.save('monterrey_coordinates_map.html')

    # Create a map for the new coordinates only
    new_coordinates_map = folium.Map(location=[25.6866, -100.3161], zoom_start=12)

    # Add new coordinates within the polygon to the map
    for coord in grid.generated_coordinates:
        folium.Marker(location=[coord.latitude, coord.longitude], icon=folium.Icon(color='green')).add_to(
            new_coordinates_map)

    # Save the map with new coordinates as an HTML file
    new_coordinates_map.save('new_coordinates_map.html')
