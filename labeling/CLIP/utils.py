#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
  A few utilities for CLIP
"""

import shutil
import urllib3
import os
from pytube import YouTube
from youtube_transcript_api import YouTubeTranscriptApi

import pandas as pd
from pandas import DataFrame

import cv2
from cv2 import VideoCapture, imwrite

from typing import Optional
from PIL import Image

def download_video(url: str, filename: str) -> None:
  """
    Download a video from url to outfile.

    Args:
      - `url (str)` : url of video
      - `outfile (str)`: filename to save to

    Returns:
      - `None`

    Raises an exception: if error connecting or downloading
  """
  if os.path.exists(filename):
    print(f"Video {filename} already downloaded")
    return

  try:
    link = YouTube(url)

  except Exception as e:
    print(f"Error Connecting: {e}")
    raise e
  
  stream = link.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()

  try:
    stream.download(filename=filename)
    print(f"Downloaded {filename} from {url}")
    return
  
  except Exception as e:
    print(f"Error Downloading: {e}")
    raise e
  
def download_transcript(id: str, filename: str) -> None:
  try:
    transcript = YouTubeTranscriptApi.get_transcript(id)
    with open(filename, "w") as f:
      f.write("start,duration,text\n")
      for line in transcript:
        # print(f"{line['start']} {line['duration']} {line['text']}")

        stripped = line['text'].strip(" \n'\"")
        stripped = stripped.replace('\n', ' ')

        f.write(f"{line['start']},{line['duration']},\"{stripped}\"\n")
    
    print(f"Downloaded transcript for {id} to {filename}")
    return
  
  except Exception as e:
    print(f"Error Downloading: {e}")
    raise e

def extract_frames(file: str, save_dir: str) -> None:
  """
  Extract frames from a video file

  Args:
    - `file (str)` : file to extract frames from
    - `save_dir (str)`: directory to save frames to

  Returns:
    - `None`

  Raises an exception: if error extracting frames
  """
  
  # if save_dir exists, delete it
  if os.path.exists(save_dir):
    shutil.rmtree(save_dir)

  try:
    os.makedirs(save_dir)

  except FileExistsError(""):
    pass
  
  if not os.path.exists(save_dir):

    raise Exception(f"Error creating {save_dir}")
  
  capture = VideoCapture(file)

  # get video fps
  fps = round(capture.get(cv2.CAP_PROP_FPS))
  print(f"Video {file} has FPS: {fps}")

  success, image = capture.read()
  count = 0

  while success:
    
    if count % fps == 0:
      imwrite(os.path.join(save_dir, f"{count // fps}.jpg"), image)
    
    success, image = capture.read()
    count += 1

  print(f"{count} frames extracted from {file}")

  return

def process_video(id: str) -> None:
  """
  Download a youtube video and extract frames and transcript.

  Args:
    - `id (str)` : video id to download

  Returns:
    - `None`

  Raises an exception: if error connecting or downloading
  """

  url = f"https://www.youtube.com/watch?v={id}"

  # download video
  download_video(url, f"data/videos/{id}.mp4")

  """
    Transcript stuff, ignore for now.
  """
  # download_transcript(id, f"data/transcripts/{id}.csv")

  # extract frames
  extract_frames(f"data/videos/{id}.mp4", f"data/frames/{id}")

  return

def load_datapoint(id: str, frame: int) -> Optional[dict]:
  """
  Load a *single*datapoint from the dataset.

  Args:
    - `id (str)` : video id
    - `frame (int)`: frame number

  Returns:
    - `Optional[dict]`: datapoint if it exists, else None
  """

  # check if frame exists
  frame_path = f"data/frames/{id}/{frame}.jpg"
  if not os.path.exists(frame_path):
    return None
  
  """
    Transcript stuff, ignore for now.
  """
  # transcript_values = transcript[transcript['start'].between(frame - 5, frame + 5)]
  # if transcript_values.empty:
  #   text = ""
  # else:
  #   # concatenate the results
  #   text = " ".join(transcript_values['text'].values)

  return {
    "frame": frame,
    "image": Image.open(frame_path),
  }

def load_data(id: str) -> DataFrame:
  """
  Load the data for a video id.

  Args:
    - `id (str)` : video id

  Returns:
    - `DataFrame`: dataframe of data
  """

  # if frames directory does not exist, process video to download and extract frames
  if not os.path.exists(f"data/frames/{id}"):
    process_video(id)

  frames = os.listdir(f"data/frames/{id}")

  datapoints = [ load_datapoint(id, i) for i in range(len(frames)) ]
  filter(lambda x: x is not None, datapoints)
  
  df = DataFrame(datapoints)
  df.set_index("frame", inplace=True)
  return df


if __name__ == "__main__":

  # test download_file
  # url = "https://www.youtube.com/watch?v=_XdD-TQseU4"
  id = "_XdD-TQseU4"
  # filename = "test.mp4"

  # process_video(id)

  # extract_frames(filename, "data/test_frames")

  # transcript_df = pd.read_csv(f"data/transcripts/{id}.csv", sep=',', encoding="utf-8")
  # print(transcript_df.head(30))

  # test load_datapoint
  # datapoint = load_datapoint(id, 20, transcript_df)
  data = load_data(id)
  print(f"{data.head(10)}")

