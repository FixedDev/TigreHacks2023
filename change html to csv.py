from bs4 import BeautifulSoup
import re
import csv

def html_to_csv(html_file, csv_file):
    with open(html_file, 'r') as f:
        html_content = f.read()

    # Extract coordinates using regex
    coordinates = re.findall(r'\[(.*?)\]', html_content)

    # Split coordinates and remove whitespace
    coordinates = [coord.split(',') for coord in coordinates]
    coordinates = [[lat.strip(), lon.strip()] for lat, lon in coordinates]

    # Write coordinates to CSV file
    with open(csv_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Latitude', 'Longitude'])  # Write header
        writer.writerows(coordinates)

    print(f"Coordinates extracted from {html_file} and saved to {csv_file}.")

# Usage example
html_file = 'new_coordinates_map.html'  # Path to your HTML file
csv_file = 'output.csv'  # Path to output CSV file

html_to_csv(html_file, csv_file)
