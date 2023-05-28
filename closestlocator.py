import csv
import math


def calculate_distance(coord1, coord2):
    x1, y1 = coord1
    x2, y2 = coord2
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def find_closest_coordinate(target_coord, coordinate_list):
    closest_coord = None
    closest_distance = float('inf')

    for coord in coordinate_list:
        distance = calculate_distance(target_coord, coord)
        if distance < closest_distance:
            closest_coord = coord
            closest_distance = distance

    return closest_coord


# Example usage
target_coord = (25.718450347161042, -100.31411141412518)  # Replace with your target coordinate

with open('output.csv', 'r') as file:
    reader = csv.reader(file)
    next(reader)  # Skip the header row
    coordinate_list = [tuple(map(float, row)) for row in reader]

closest_coordinate = find_closest_coordinate(target_coord, coordinate_list)
print("Closest coordinate:", closest_coordinate)
