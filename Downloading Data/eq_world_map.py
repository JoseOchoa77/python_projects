# Import necessary libraries
from pathlib import Path  # For working with file paths
import json  # For working with JSON data
import plotly.express as px  # For creating visualizations

# Define the path to the earthquake data file
# This specifies the location of the GeoJSON file using an absolute path.
path = Path('/Users/joseochoa/Desktop/Python Coding Class/Projects/Downloading Data/eq_data/eq_data_30_day_m1.geojson')

# Read the contents of the GeoJSON file
# The file is read as a string and then converted to a Python dictionary using `json.loads`.
contents = path.read_text(encoding='utf-8')
all_eq_data = json.loads(contents)

# Extract earthquake data from the GeoJSON file
# The 'features' key contains a list of dictionaries, each representing an earthquake.
all_eq_dicts = all_eq_data['features']

# Initialize lists to store earthquake data
# These lists will hold magnitudes, longitudes, latitudes, and titles for each earthquake.
mags, lons, lats, eq_titles = [], [], [], []

# Loop through each earthquake dictionary in the dataset
# Extract the magnitude, longitude, latitude, and title for each earthquake.
for eq_dict in all_eq_dicts:
    mag = eq_dict['properties']['mag']  # Extract the magnitude of the earthquake.
    lon = eq_dict['geometry']['coordinates'][0]  # Extract the longitude.
    lat = eq_dict['geometry']['coordinates'][1]  # Extract the latitude.
    eq_title = eq_dict['properties']['title']  # Extract the title of the earthquake.
    mags.append(mag)  # Append the magnitude to the `mags` list.
    lons.append(lon)  # Append the longitude to the `lons` list.
    lats.append(lat)  # Append the latitude to the `lats` list.
    eq_titles.append(eq_title)  # Append the title to the `eq_titles` list.

# Create a scatter plot of the earthquake data on a world map
# Use Plotly Express to create a scatter_geo plot with the extracted data.
title = 'Global Earthquakes'  # Set the title of the plot.
fig = px.scatter_geo(
    lat=lats,  # Latitude values for the earthquakes.
    lon=lons,  # Longitude values for the earthquakes.
    size=mags,  # Magnitudes determine the size of the markers.
    title=title,  # Title of the plot.
    color=mags,  # Magnitudes determine the color of the markers.
    color_continuous_scale='Viridis',  # Use the 'Viridis' color scale.
    labels={'color': 'Magnitude'},  # Label for the color scale.
    projection='natural earth',  # Use the 'natural earth' projection for the map.
    hover_name=eq_titles,  # Display the earthquake title when hovering over a marker.
)

# Display the plot
fig.show()
