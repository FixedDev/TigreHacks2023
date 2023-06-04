from bs4 import BeautifulSoup
import csv

def html_to_csv(html_file, csv_file):
    with open(html_file, 'r') as f:
        html_content = f.read()

    # Parse the HTML file
    soup = BeautifulSoup(html_content, 'html.parser')

    # Extract the coordinates
    coordinates = soup.find_all('coordinate')

    # Create a dict to store the coordinates
    coordinates_dict = {}
    for coordinate in coordinates:
        latitude = coordinate['latitude']
        longitude = coordinate['longitude']
        coordinates_dict[latitude] = longitude

    # Write the coordinates to the CSV file
    with open(csv_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Latitude', 'Longitude'])  # Write header
        for latitude, longitude in coordinates_dict.items():
            writer.writerow([latitude, longitude])

    print(f"Coordinates extracted from {html_file} and saved to {csv_file}.")

# Usage example
html_file = 'new_coordinates_map.html'  # Path to your HTML file
csv_file = 'output.csv'  # Path to output CSV file

html_to_csv(html_file, csv_file)

