import json
from youtubesearchpython import VideosSearch, ResultMode

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
                # Add any other metadata you want here
            }
            videos_metadata.append(video_data)

# Write the collected metadata to a file in JSON format
with open("video_metadata.json", "w") as output_file:
    json.dump(videos_metadata, output_file, indent=4)

print("Check 'video_metadata.json' for the results")
