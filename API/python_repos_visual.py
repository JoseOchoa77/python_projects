# Import necessary libraries
import requests  # For making HTTP requests to APIs
import plotly.express as px  # For creating visualizations

# Make an API call and check the response.
# The URL points to the GitHub API endpoint for searching repositories.
# The query searches for Python repositories with more than 10,000 stars, sorted by stars.
url = "https://api.github.com/search/repositories"
url += "?q=language:python+sort:stars+stars:>10000"

# Define headers to specify the API version.
# This ensures compatibility with the GitHub API.
headers = {"Accept": "application/vnd.github.v3+json"}

# Send a GET request to the API endpoint.
r = requests.get(url, headers=headers)

# Print the status code to ensure the request was successful (200 means OK).
print(f"Status code: {r.status_code}")

# Process the overall results.
# Convert the JSON response to a Python dictionary.
response_dict = r.json()

# Check if the results are complete (not truncated).
print(f"Complete results: {not response_dict['incomplete_results']}")

# Process repository information.
# Extract the list of repositories from the 'items' key in the response.
repo_dicts = response_dict['items']

# Initialize lists to store data for the visualization.
repo_links, stars, hover_texts = [], [], []

# Loop through each repository in the list.
for repo_dict in repo_dicts:
    # Turn repository names into active links.
    # This creates a clickable link for each repository.
    repo_name = repo_dict['name']
    repo_url = repo_dict['html_url']
    repo_link = f"<a href='{repo_url}'>{repo_name}</a>"
    repo_links.append(repo_link)

    # Append the number of stars for each repository.
    stars.append(repo_dict['stargazers_count'])

    # Build hover texts for each repository.
    # Include the owner's username and the repository description.
    owner = repo_dict['owner']['login']
    description = repo_dict['description']
    hover_text = f"{owner}<br />{description}"
    hover_texts.append(hover_text)

# Make the visualization.
# Create a bar chart using Plotly Express.
title = "Most-Starred Python Projects on GitHub"  # Set the chart title.
labels = {'x': 'Repository', 'y': 'Stars'}  # Define axis labels.
fig = px.bar(
    x=repo_links,  # Use repository links for the x-axis.
    y=stars,  # Use the number of stars for the y-axis.
    title=title,  # Set the chart title.
    labels=labels,  # Set axis labels.
    hover_name=hover_texts  # Display hover text for each bar.
)

# Customize the layout of the chart.
fig.update_layout(
    title_font_size=28,  # Set the font size for the title.
    xaxis_title_font_size=20,  # Set the font size for the x-axis label.
    yaxis_title_font_size=20  # Set the font size for the y-axis label.
)

# Customize the appearance of the bars.
fig.update_traces(
    marker_color='SteelBlue',  # Set the bar color to SteelBlue.
    marker_opacity=0.6  # Set the bar opacity to 60%.
)

# Display the chart.
fig.show()
