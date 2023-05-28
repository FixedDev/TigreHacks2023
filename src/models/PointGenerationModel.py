import math

from folium import Polygon


def pointFromDb(document):
    return Point(document["latitude"], document["longitude"])


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

    def forDb(self):
        return {"latitude": self.latitude, "longitude": self.longitude}


def shapeFromDb(document):
    if len(document) < 3:
        return RectangularShape(pointFromDb(document[0]), pointFromDb(document[1]))
    else:
        return PolygonalShape([pointFromDb(doc) for doc in document])


class Shape:
    def isIn(self, point: Point):
        pass

    def forDb(self):
        pass


class RectangularShape(Shape):
    def __init__(self, point1: Point, point2: Point):
        self.point1 = point1 if point1 > point2 else point2
        self.point2 = point2 if self.point1 == point1 else point1

    def isIn(self, point: Point):
        return self.point1 >= point >= self.point2

    def forDb(self):
        return [self.point1.forDb(), self.point2.forDb()]


class PolygonalShape(Shape):
    def __init__(self, points: list[Point]):
        self.points = points

        if len(points) < 3:
            raise ValueError("A polygonal shape should have at least 3 vertexes")

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

    def forDb(self):
        return [point.forDb() for point in self.points]

