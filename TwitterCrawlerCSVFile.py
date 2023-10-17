import requests
import csv
from datetime import datetime
import configparser

config = configparser.ConfigParser()
config.read('config.ini')


# Replace with your Twitter API v2 Bearer Token
bearer_token = config['twitterAPI']['bearer_token']

# Define the Twitter username of the user you want to search tweets from
username = "elonmusk" # You can replace elonmusk with any user name you want to scrape

# Define the search query to find tweets about "SpaceX" from the specified user
search_query = f"from:{username} SpaceX" # You can replace SpaceX with any keyword you want to search

# Set the Twitter API v2 endpoint for recent tweet search
url = "https://api.twitter.com/2/tweets/search/recent"

# Define query parameters to include additional fields
params = {
    "query": search_query,
    "max_results": 100,  # Specify the number of results per response
    "tweet.fields": "created_at,text,public_metrics,referenced_tweets",  # Include additional fields
}

# Set the request headers with the Bearer Token
headers = {
    "Authorization": f"Bearer {bearer_token}",
}

# Send a GET request to the endpoint
response = requests.get(url, params=params, headers=headers)
if response.status_code == 200:
    data = response.json()

    # Define a list of tweet data to be written to a CSV file
    tweet_data = []

    for tweet in data["data"]:
        timestamp = datetime.strptime(tweet["created_at"], "%Y-%m-%dT%H:%M:%S.%fZ")
        username = username
        tweet_content = tweet["text"]
        retweets = tweet["public_metrics"]["retweet_count"]
        likes = tweet["public_metrics"]["like_count"]
        replies = tweet["public_metrics"]["reply_count"]

        # Append the tweet data to the list
        tweet_data.append([timestamp, username, tweet_content, retweets, likes, replies])

    # Define the CSV filename
    csv_filename = "tweets.csv"

    # Write the tweet data to a CSV file
    with open(csv_filename, mode='w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        # Write the header row
        writer.writerow(["Timestamp", "Username", "Tweet Content", "Retweets", "Likes", "Replies"])
        # Write the tweet data
        writer.writerows(tweet_data)

    print(f"Collected {len(tweet_data)} tweets and saved to {csv_filename}")
else:
    print(f"Request returned an error: {response.status_code} {response.text}")