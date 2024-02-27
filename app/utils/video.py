import os
import re
import json
from dotenv import load_dotenv
from yt_dlp import YoutubeDL
from pathlib import Path
from pymongo import MongoClient


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
        if os.path.exists(filename.replace('.part', '')):
            print(f"Skipping download for {filename}, already exists")
            return

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
    load_dotenv()
    mongo_uri = os.getenv('MONGODB_URI')
    client = MongoClient(mongo_uri)
    db = client['preTechnigalaClean_db']
    collection = db['video_metadata']
        
    for video in collection.find():
        video_id = str(video['_id'])
        url = video['youtubeURL'].replace("https://www.youtube.comhttps://www.youtube.com", "https://www.youtube.com")
        title = video['title'].replace(' ', '_')
        author = video['uploader'].replace(' ', '_')
        topics = ''.join(str(id) for id in video['topicId'])

        home_dir = os.path.expanduser('~')
        data_dir = os.path.join(home_dir, 'Videos', f"{video_id}")
        filename = os.path.join(data_dir, "video.mp4")

        # print("datadir: ", data_dir)
        # print("filename: ", filename)

        if not Path(filename).is_file():
            # Ensure the data/videos directory exists
            ensure_dir(data_dir)
            download_video(url, filename)
        else:
            # print(data_dir)
            print(f"Skipping download for {data_dir}, already exists")

        # download_video(url, filename)

if __name__ == "__main__":
    file_path = "video_metadata_test.json"  # Adjust this to the actual path of your JSON file
    download_videos_from_json(file_path)
