#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
  Module for extracting frames from videos
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

def extract_frames(file: str, save_dir: str):
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
    
  os.makedirs(save_dir)

  capture = VideoCapture(file)

  # get video fps
  fps = round(capture.get(cv2.CAP_PROP_FPS))

  success, image = capture.read()
  count = 0
  
  print("Extracting frames... ")

  while success:
    if count % fps == 0:
      imwrite(os.path.join(save_dir, f"{count // fps}.jpg"), image)
    
    success, image = capture.read()
    count += 1

  print(f"{count} frames extracted from {file}")
