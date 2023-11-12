#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
  A few utilities for CLIP and BART
"""

import os
import shutil

import pandas as pd
from PIL import Image
from pandas import DataFrame

# if running inside utils module
try:
  from frames import extract_frames
  from video import download_video
  from transcript import download_transcript
  
# if running outside utils module
except ImportError:
  from .frames import extract_frames
  from .video import download_video
  from .transcript import download_transcript

from typing import Dict

def init_directories() -> None:
  # create data directories if they don't exist
  if not os.path.exists("data"):
    os.mkdir("data")
    
  if not os.path.exists("data/videos"):
    os.mkdir("data/videos")
    
  if not os.path.exists("data/frames"):
    os.mkdir("data/frames")
    
  if not os.path.exists("data/transcripts"):
    os.mkdir("data/transcripts")
    
def remove_directories() -> None:
  if os.path.exists("data"):
    shutil.rmtree("data")


def process_video(id: str, filename: str) -> Dict[str, DataFrame]:
  """
  Download a youtube video and extract frames and transcript.

  Args:
    - `id (str)` : video id to download

  Returns:
    - `None`

  Raises an exception: if error connecting or downloading
  """
  
  init_directories()

  url = f"https://www.youtube.com/watch?v={id}"
  
  # download video if it does not exist yet.
  if not os.path.exists(f"data/videos/{filename}.mp4"):
    download_video(url, f"data/videos/{filename}.mp4")
    extract_frames(f"data/videos/{filename}.mp4", f"data/frames/{filename}"),

  # download transcript if it does not exist yet.
  if not os.path.exists(f"data/transcripts/{filename}.csv"):
    download_transcript(id, f"data/transcripts/{filename}.csv")

  data =  load_data(filename)
  
  # remove_directories()
  return data


def load_data(filename: str) -> Dict[str, DataFrame]:
  """
  Load the data for a video id.

  Args:
    - `id (str)` : video id

  Returns:
    - `DataFrame`: dataframe of data
  """

  frames = os.listdir(f"data/frames/{filename}")

  transcript_df = pd.read_csv(f"data/transcripts/{filename}.csv", sep=',', encoding="utf-8")
  transcript_df["second"] = transcript_df["second"].apply(lambda x: int(x))
  
  frames_df = DataFrame([
    {
      "second": i,
      "image": Image.open(f"data/frames/{filename}/{i}.jpg"),
    }
    for i in range(len(frames))
  ])

  return {
    "transcript": transcript_df,
    "frames": frames_df
  }
  
def main() -> None:
  file_path = "videos_23f"
  with open(file_path, 'r') as file:
    for line in file:
      url, topic, subtopic, title = line.strip().split(', ')
      id = url.split('=')[-1]
      topic = topic.replace(' ', '')
      subtopic = subtopic.replace(' ', '')
      title = title.replace(' ', '_')
      process_video(id, f"playlist_{topic}_{subtopic}_{title}")

if __name__ == "__main__":
  main()

