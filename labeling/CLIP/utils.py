#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
  A few utilities for CLIP
"""

import shutil
import urllib3
import os
from pytube import YouTube

import cv2
from cv2 import VideoCapture, imwrite

import math

def download_file(url: str, filename: str) -> None:
  """
  Download a file from url to filename

  Args:
    - `url (str)` : url to download from  
    - `filename (str)`: filename to save to

  Returns:
    - `None`

  Raises an exception: if error connecting or downloading
  """
  if os.path.exists(filename):
    print(f"{filename} already exists")
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
  # and recreate it.

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
  print(f"FPS: {fps}")

  success, image = capture.read()
  count = 0

  while success:


    if count % fps == 0:
      imwrite(os.path.join(save_dir, f"{count // fps}.jpg"), image)
    success, image = capture.read()
    count += 1

  return


    

if __name__ == "__main__":

  # test download_file
  url = "https://www.youtube.com/watch?v=_XdD-TQseU4"
  filename = "test.mp4"

  download_file(url, filename)

  extract_frames(filename, "data/test_frames")

