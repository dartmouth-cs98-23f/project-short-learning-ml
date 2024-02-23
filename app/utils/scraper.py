import json
import requests
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta
from pymongo import MongoClient
from youtubesearchpython import VideosSearch, ResultMode

# This scraper takes an input from the 'topicstosearch' file, which is formatted as the indicies of each topic to scrape videos from on their own line
# It then cross references with the 'alltopics.json' file to find the keywords to use to complete the search
# 

def convert_duration_to_seconds(duration_str):
    parts = duration_str.split(":")
    if len(parts) == 3:
        # Format is HH:MM:SS
        hours, minutes, seconds = map(int, parts)
        total_seconds = hours * 3600 + minutes * 60 + seconds
    elif len(parts) == 2:
        # Format is MM:SS
        minutes, seconds = map(int, parts)
        total_seconds = minutes * 60 + seconds
    else:
        # Assuming the format is just seconds (SS) for completeness
        total_seconds = int(parts[0])
    
    return total_seconds

# Used to convert Youtube's "_ years/months/days ago" format to a ISO formatted date
def convert_to_date(years_ago):
    # Extract the number
    value = years_ago.split()[0]
    if value == "Streamed":
        value = int(years_ago.split()[1])
        period = years_ago.split()[2]
    else:
        period = years_ago.split()[1]
        value = int(value)
    
    # Create a date object
    if period == "years" or period == "year":
        date = datetime(datetime.now().year-value, datetime.now().month, datetime.now().day)
    elif period == "months" or period == "month":
        if value>=datetime.now().month:
            date = datetime(datetime.now().year-1, datetime.now().month-value+12, datetime.now().day)
        else:
            date = datetime(datetime.now().year, datetime.now().month-value, datetime.now().day)
    elif period == "days" or period == "day":
        if value>=datetime.now().day:
            date = datetime(datetime.now().year, datetime.now().month-1, datetime.now().day+30-value)
        else:
            date = datetime(datetime.now().year, datetime.now().month, datetime.now().day-value)
    else:
        date = datetime(datetime.now().year, datetime.now().month, datetime.now().day)

    return date.isoformat()

# Scraping function that scrapes 'count' videos of each topic that corresponds to id
def scrape(ids: list, count: int):

    # Create topics dictionary from a file
    with open("alltopics.json", "r") as topics_file:
        topics = json.load(topics_file)

    # Initialize list to hold topics we are searching for 
    search_topics = []

    # Iterate through keys and ensure they match with a topic
    for id in ids:
        if id in topics:
            search_topics.append([id, topics[id]])

    # Initialize a list to hold all video metadata
    videos_metadata = []

    # Setup MongoDB connection
    load_dotenv()
    mongo_uri = os.getenv('MONGODB_URI')
    client = MongoClient(mongo_uri)
    db = client['scraper']
    collection = db['video_metadata']

    # Loop through each keyword
    for [topicId, keyword] in search_topics:
        # Search for videos using the keyword, the limit is how many videos we will save for this topic
        search = VideosSearch(keyword.replace(", ", " "), limit=10)
        results_json = search.result(mode=ResultMode.json)

        try:
            results = json.loads(results_json)
        except json.JSONDecodeError:
            print(f"Error decoding JSON for keyword {keyword}")
            continue

        if results['result']:
            top_results = results['result']

            # Counting variable to reach 'count' videos per subject
            videos_uploaded = 0            

            # Extract and store relevant information for each result
            for result in top_results:
                if videos_uploaded >= count:
                    break
                duration = convert_duration_to_seconds(result['duration'])
                if duration > 3600:
                    continue
                description_snippet = result.get('descriptionSnippet', [])
                if description_snippet:
                    description = ''.join([snippet.get('text', '') for snippet in description_snippet])
                else:
                    description = ""
                video_data = {
                    'title': result['title'],
                    "description": description[:-4] + '...',
                    'youtubeURL': result['link'],
                    'uploadDate': convert_to_date(result['publishedTime']),
                    'uploader': result['channel']['name'],
                    'duration': duration,
                    "thumbnailURL": result['thumbnails'][-1]['url'],
                    'topicId': topicId,
                    'clips': [],
                    'views': [],
                    'likes': [],
                    'dislikes': []
                }
                
                videos_metadata.append(video_data)

                # upload result to MongoDB
                upload_result = collection.insert_one(video_data)
                if upload_result:
                    print(f"Uploaded {result['title']} to MongoDB")
                # convert id from upload to string so it can be converted to json
                video_data['_id'] = str(upload_result.inserted_id)
                videos_uploaded += 1

        """  # Make API call
            API_ENDPOINT = "http://localhost:3000/api/videos" # CHANGE API END POINT WHEN READY
            headers = {"Content-Type": "application/json",
                    "Authorization": token}
            if secret_key:
                print(token)

            API_video_data = {
                "title": result['title'],
                "youtubeURL": result['link'],
                "duration": convert_duration_to_seconds(result['duration']),
                "description": (result.get('descriptionSnippet') or [{}])[0].get('text', 'No description'),
                "thumbnailURL": result['thumbnails'][-1]['url'],
            }
            response = requests.put(API_ENDPOINT, json=API_video_data, headers=headers)

            if response.status_code == 200:
                print(f"Video data successfully sent to the API for {result['title']}.")
            else:
                print(f"Failed to send video data for {result['title']}. Status code:", response.status_code) """

    # Write the collected metadata to a file in JSON format
    with open("video_metadata.json", "w") as output_file:
        json.dump(videos_metadata, output_file, indent=4)

    print("Check 'video_metadata.json' for the results")

# Determine which topics to search for based on toSearch file
with open("topicstosearch", "r") as to_search:
    search_keys = []
    for line in to_search:
        key = line.strip()
        search_keys.append(key)
    scrape(search_keys, 5)