import json
import requests
from youtubesearchpython import VideosSearch, ResultMode

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

# Read keywords from a file
with open("topics", "r") as topics_file:
    keywords = [line.strip() for line in topics_file]

# Initialize a list to hold all video metadata
videos_metadata = []

# Loop through each keyword
for keyword in keywords:
    # Search for videos using the keyword
    search = VideosSearch(keyword.replace(", ", " "), limit=3)
    results_json = search.result(mode=ResultMode.json)

    try:
        results = json.loads(results_json)
    except json.JSONDecodeError:
        print(f"Error decoding JSON for keyword {keyword}")
        continue

    if results['result']:
        top_results = results['result']

        # Extract and store relevant information for each result
        for result in top_results:
            video_data = {
                'title': result['title'],
                'link': result['link'],
                'topics': keyword,
                'author': result['channel']['name'],
                'duration': result['duration'],
                'publish_date': result['publishedTime'],
                "viewCount": int(result['viewCount']['text'].replace(" views", "").replace(",", "")),
                "description": (result.get('descriptionSnippet') or [{}])[0].get('text', 'No description'),
                "thumbnail": result['thumbnails'][-1]['url'],
            }

            videos_metadata.append(video_data)

            # Make API call
            API_ENDPOINT = "http://localhost:3000/api/videos" # CHANGE API END POINT WHEN READY
            headers = {"Content-Type": "application/json"}

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
                print(f"Failed to send video data for {result['title']}. Status code:", response.status_code)

# Write the collected metadata to a file in JSON format
with open("video_metadata.json", "w") as output_file:
    json.dump(videos_metadata, output_file, indent=4)

print("Check 'video_metadata.json' for the results")

