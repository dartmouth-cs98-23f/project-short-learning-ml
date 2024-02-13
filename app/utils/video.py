import os
import json
from yt_dlp import YoutubeDL

def ensure_dir(directory):
    """Ensure that a directory exists. If it doesn't, create it."""
    if not os.path.exists(directory):
        os.makedirs(directory)

def download_video(url: str, filename: str) -> None:
    """
    Download a video from url to filename.

    Args:
      - `url (str)`: URL of the video (not ID!!)
      - `filename (str)`: filename to save to, including path

    Returns:
      - `None`

    Raises an exception: if error connecting or downloading
    """

    try:
        ydl_opts = {
            'format': 'best[ext=mp4]/best',  # Explicitly specify the best format (single file)
            'outtmpl': filename,
        }

        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            print(f"Downloaded {filename} from {url}")
    except Exception as e:
        print(f"Error connecting: {e}")
        raise e

def download_videos_from_json(file_path: str) -> None:
    """
    Download videos based on metadata contained in a JSON file.

    Args:
      - `file_path (str)`: Path to the JSON file containing video metadata

    Returns:
      - `None`
    """
    with open(file_path, 'r') as file:
        videos = json.load(file)
        
        # Ensure the data/videos directory exists
        data_dir = os.path.join('data', 'videos')
        ensure_dir(data_dir)
        
        for video in videos:
            url = video['link'].replace("https://www.youtube.comhttps://www.youtube.com", "https://www.youtube.com")
            title = video['title'].replace(' ', '_')
            author = video['author'].replace(' ', '_')
            topics = video['topics'].replace(', ', '_')
            filename = os.path.join(data_dir, f"{topics}_{title}_{author}.mp4")
            download_video(url, filename)

if __name__ == "__main__":
    file_path = "video_metadata.json"  # Adjust this to the actual path of your JSON file
    download_videos_from_json(file_path)
