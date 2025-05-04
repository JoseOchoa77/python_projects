# Import necessary libraries
import requests  # For making HTTP requests to APIs

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

# Convert the response object to a dictionary.
# The JSON response is converted into a Python dictionary for easier processing.
response_dict = r.json()

# Print the total number of repositories that match the query.
print(f"Total repositories: {response_dict['total_count']}")

# Check if the results are complete (not truncated).
# The 'incomplete_results' key indicates whether the results are truncated.
print(f"Complete results: {not response_dict['incomplete_results']}")

# Explore information about the repositories.
# Extract the list of repositories from the 'items' key in the response.
repo_dicts = response_dict['items']
print(f"Repositories returned: {len(repo_dicts)}")  # Print the number of repositories returned.

# Loop through each repository and print selected information.
print("\nSelected information about each repository:")
for repo_dict in repo_dicts:
    # Print details about the repository.
    print("\nSelected information about first repository:")
    print(f"Name: {repo_dict['name']}")  # Repository name
    print(f"Owner: {repo_dict['owner']['login']}")  # Repository owner's username
    print(f"Stars: {repo_dict['stargazers_count']}")  # Number of stars
    print(f"Repository: {repo_dict['html_url']}")  # URL to the repository
    print(f"Created: {repo_dict['created_at']}")  # Creation date
    print(f"Updated: {repo_dict['updated_at']}")  # Last update date
    print(f"Description: {repo_dict['description']}")  # Repository description
