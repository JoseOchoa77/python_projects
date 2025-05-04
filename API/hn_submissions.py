from operator import itemgetter  # For sorting dictionaries by a specific key
import requests  # For making HTTP requests to APIs

# Make an API call to get the top stories on Hacker News.
# The URL points to the top stories endpoint, which returns a list of submission IDs.
url = 'https://hacker-news.firebaseio.com/v0/topstories.json'
r = requests.get(url)  # Send a GET request to the API endpoint
print(f"Status code: {r.status_code}")  # Print the status code to ensure the request was successful

# Process the list of submission IDs returned by the API.
# The response is a JSON array of IDs, which we convert to a Python list.
submission_ids = r.json()

# Initialize a list to store information about each submission.
submission_dicts = []

# Loop through the first 30 submission IDs.
# For each ID, make a new API call to get details about the submission.
for submission_id in submission_ids[:30]:
    # Construct the URL for the specific submission.
    url = f"https://hacker-news.firebaseio.com/v0/item/{submission_id}.json"
    r = requests.get(url)  # Send a GET request to the API endpoint
    print(f"id: {submission_id}\tstatus: {r.status_code}")  # Print the ID and status code for debugging
    response_dict = r.json()  # Convert the JSON response to a Python dictionary
    
    # Build a dictionary for each article.
    # Use the `.get()` method to safely access keys and provide default values if keys are missing.
    submission_dict = {
        'title': response_dict.get('title', 'No title'),  # Get the title or use 'No title' if missing
        'hn_link': f"https://news.ycombinator.com/item?id={submission_id}",  # Construct the discussion link
        'comments': response_dict.get('descendants', 0),  # Get the number of comments or default to 0
    }
    submission_dicts.append(submission_dict)  # Add the dictionary to the list

# Sort the list of submissions by the number of comments in descending order.
# Use `itemgetter` to specify the 'comments' key for sorting.
submission_dicts = sorted(submission_dicts, key=itemgetter('comments'), reverse=True)

# Print the top submissions.
# Loop through the sorted list and print the title, discussion link, and number of comments for each submission.
for submission_dict in submission_dicts:
    print(f"\nTitle: {submission_dict['title']}")  # Print the title of the submission
    print(f"Discussion link: {submission_dict['hn_link']}")  # Print the discussion link
    print(f"Comments: {submission_dict['comments']}")  # Print the number of comments
