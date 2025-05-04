# Import necessary libraries
from pathlib import Path  # For working with file paths
import csv  # For reading CSV files
from datetime import datetime  # For working with date and time data
import matplotlib.pyplot as plt  # For creating visualizations

# Define the path to the CSV file
# This specifies the location of the weather data file using a relative path.
path = Path('/Users/joseochoa/Desktop/Python Coding Class/Projects/Downloading Data/weather_data/sitka_weather_2021_simple.csv')

# Read the contents of the file and split it into lines
# Each line represents a row in the CSV file.
lines = path.read_text().splitlines()

# Create a CSV reader object to parse the lines
# This allows us to process the file as a CSV.
reader = csv.reader(lines)

# Extract the header row from the CSV file
# The header row contains the column names, which describe the data in each column.
header_row = next(reader)

# Extract dates, high temperatures, and low temperatures from the CSV file
# Loop through the remaining rows in the CSV file.
# Convert the date in the 3rd column (index 2) to a datetime object.
# Convert the high temperature in the 5th column (index 4) and low temperature in the 6th column (index 5) to integers.
# Append the extracted data to the `dates`, `highs`, and `lows` lists.
dates, highs, lows = [], [], []
for row in reader:
    current_date = datetime.strptime(row[2], '%Y-%m-%d')  # Parse the date string into a datetime object.
    high = int(row[4])  # Convert the high temperature value to an integer.
    low = int(row[5])  # Convert the low temperature value to an integer.
    dates.append(current_date)  # Append the date to the `dates` list.
    highs.append(high)  # Append the high temperature to the `highs` list.
    lows.append(low)  # Append the low temperature to the `lows` list.

# Plot the high and low temperatures
# Use the seaborn style for better aesthetics.
plt.style.use('seaborn-v0_8')
fig, ax = plt.subplots()

# Plot the high temperatures in red and low temperatures in blue
# Use alpha for transparency to make the lines easier to read.
ax.plot(dates, highs, color='red', alpha=0.5, label='Highs')  # Plot high temperatures with a red line.
ax.plot(dates, lows, color='blue', alpha=0.5, label='Lows')  # Plot low temperatures with a blue line.

# Fill the area between the high and low temperatures
# Use a light blue color with transparency for better visualization.
ax.fill_between(dates, highs, lows, facecolor='blue', alpha=0.1)

# Format the plot
# Add a title, x-axis label, and y-axis label for better readability.
ax.set_title("Daily High and Low Temperatures, 2021", fontsize=24)  # Set the title of the plot.
ax.set_xlabel('', fontsize=16)  # Leave the x-axis label blank.
fig.autofmt_xdate()  # Automatically format the x-axis dates for better readability.
ax.set_ylabel("Temperature (F)", fontsize=16)  # Label the y-axis with "Temperature (F)".
ax.tick_params(labelsize=16)  # Customize the tick parameters for better readability.

# Add a legend to differentiate between high and low temperatures
ax.legend(fontsize=16)

# Display the plot
plt.show()
