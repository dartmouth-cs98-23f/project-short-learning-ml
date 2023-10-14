# Simple Transcript-Based Content Labeling

This method uses content from hack-a-thing-2 that leveraged the YouTube and OpenAI APIs to label YouTube videos based on video title. I did not attempt at transcript generation yet but this did an ok job for an oversimplified sample set of videos.

- `scraper.ipynb` uses the YouTube API to scrape video titles
- `ChannelData.csv` contains the output of the scraper
- `getSubject.py` takes `ChannelData.csv` as input and uses the OpenAI API to label the videos by only 4 subject categories
- `Classification.csv` contains the labeled data