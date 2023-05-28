import random
import csv
import folium
import pymongo
from bson import ObjectId
from geopandas import *

from src.models.PointGenerationModel import *

from src.controllers.db.DatabaseAccessController import JsonConnectionData, MongoConnectionHandle


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

    return Grid(grid_shape, existing_coordinates, exclusion_zones=exclusion_zones)


def gridFromDb(document):
    grid = Grid(
        shapeFromDb(document["shape"]),
        [(pointFromDb(doc)) for doc in document["existing"]],
        ObjectId(document["_id"]),
        [(shapeFromDb(doc)) for doc in document["exclusion_zones"]]
    )

    grid.generated_coordinates = [(pointFromDb(doc)) for doc in document["generated"]]
    grid.points = document["points"]
    grid.distance = document["distance"]

    return grid


class Grid:
    existing_coordinates: list[Point]
    generated_coordinates: list[Point]
    exclusion_zones: list[Shape]

    def __init__(self, grid_shape, existing_coordinates, id=ObjectId(), exclusion_zones=None):
        self.__id = id
        self.shape = grid_shape
        self.existing_coordinates = existing_coordinates
        self.generated_coordinates = []
        self.points = 10
        self.distance = 1

        if exclusion_zones is None:
            exclusion_zones = []

        self.exclusion_zones = exclusion_zones

        self.__delete_outer_points()

    def id(self):
        return self.__id

    def add_point(self, point, force=False):
        if not force:
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
        complete_coordinates = self.existing_coordinates.copy()
        complete_coordinates.extend(self.generated_coordinates)

        new_coordinates = generate_new_coordinates(complete_coordinates,
                                                   self.points, self.distance,
                                                   self.shape, self.exclusion_zones)

        self.generated_coordinates.extend(new_coordinates)

    def forDb(self):
        return {"_id": self.__id,
                "generated": [(coord.forDb()) for coord in self.generated_coordinates],
                "existing": [(coord.forDb()) for coord in self.existing_coordinates],
                "shape": self.shape.forDb(),
                "exclusion_zones": [(zone.forDb()) for zone in self.exclusion_zones],
                "points": self.points,
                "distance": self.distance}


class GridAccessManager:
    db_access_object: pymongo.collection

    def __init__(self, db_access_object: pymongo.collection):
        self.db_access_object = db_access_object

    def findFirst(self):
        document = self.db_access_object.find_one()

        if document is None:
            return None

        grid = gridFromDb(document)
        return grid

    def search(self, filter):
        document = self.db_access_object.find_one(filter)

        if document is None:
            return None

        grid = gridFromDb(document)
        return grid

    def searchById(self, id):
        return self.search({"_id": id})

    def update(self, grid: Grid):
        self.db_access_object.replace_one(filter={"_id": grid.id()}, replacement=grid.forDb(), upsert=True)


if __name__ == "__main__":
    with open("db.json", mode='r') as file_handle:
        connection_data = JsonConnectionData(file_handle)
        connection = MongoConnectionHandle(data=connection_data)
        connection.connection().get_database("test").command("ping")

        grid_access = GridAccessManager(connection.connection().get_database("dbtest").get_collection("grid"))

        original_grid = grid_access.findFirst()

        if original_grid is None:
            print("Generating grid")
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
            original_grid = grid

            grid_access.update(grid)

        # original_grid.exclusion_zones = []
        original_grid.generatePoints()

        # Create a map centered on Monterrey
        monterrey_map = folium.Map(location=[25.6866, -100.3161], zoom_start=12)

        # Add existing coordinates to the map
        for coord in original_grid.existing_coordinates:
            folium.Marker(location=[coord.latitude, coord.longitude], icon=folium.Icon(color='blue')).add_to(
                monterrey_map)

        # Add new coordinates within the polygon to the map
        for coord in original_grid.generated_coordinates:
            folium.Marker(location=[coord.latitude, coord.longitude], icon=folium.Icon(color='green')).add_to(
                monterrey_map)

        # Save the map as an HTML file
        monterrey_map.save('monterrey_coordinates_map.html')

        # Create a map for the new coordinates only
        new_coordinates_map = folium.Map(location=[25.6866, -100.3161], zoom_start=12)

        # Add new coordinates within the polygon to the map
        for coord in original_grid.generated_coordinates:
            folium.Marker(location=[coord.latitude, coord.longitude], icon=folium.Icon(color='green')).add_to(
                new_coordinates_map)

        # Save the map with new coordinates as an HTML file
        new_coordinates_map.save('new_coordinates_map.html')
