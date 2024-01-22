import json
from youtubesearchpython import ChannelSearch, ResultMode

# Read channel IDs
with open("channels", "r") as channels_file:
    channel_ids = [line.strip() for line in channels_file]

# Read keyword
with open("topics", "r") as topics_file:
    keywords = [line.strip().split(", ") for line in topics_file]

with open("videos_24w", "w") as output_file:
    # Loop through each channel ID
    for channel_id in channel_ids:
        # Loop through each keyword
        for keyword_info in keywords:
            keyword = keyword_info[0]
            subtopic = keyword_info[1]
            topic = keyword_info[2]

            # Search
            search = ChannelSearch(keyword, channel_id)
            results = search.result(mode=ResultMode.json)
            results_json = search.result(mode=ResultMode.json)
            results = None
      
            try:
                results = json.loads(results_json)
            except json.JSONDecodeError:
                print(f"Error decoding JSON for channel {channel_id} and keyword {keyword}")
                continue
            
            if results['result']:
                
                top_result = results['result'][:3]

                # Extract and write relevant information for each result
                for result in top_result:
                    video_link = f"https://www.youtube.com{result['uri']}"
                    video_title = result['title']
                    output_line = f"{video_link}, {topic}, {subtopic}, {video_title}\n"
                    output_file.write(output_line)

print("Check 'videos_24w' for the results")
