# Import necessary libraries
import requests  # For making HTTP requests to APIs
import json  # For working with JSON data

# Make an API call, and store the response.
# The URL points to a specific Hacker News article in JSON format.
url = "https://hacker-news.firebaseio.com/v0/item/31353677.json"
r = requests.get(url)  # Send a GET request to the API endpoint
print(f"Status code: {r.status_code}")  # Print the status code to ensure the request was successful

# Explore the structure of the data.
# Convert the JSON response to a Python dictionary.
response_dict = r.json()

# Format the dictionary as a JSON string with indentation for readability.
response_string = json.dumps(response_dict, indent=4)

# Print the formatted JSON string to explore the structure of the data.
print(response_string)
