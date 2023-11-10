#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
  Video downloader
"""

import os
from pytube import YouTube

def download_video(url: str, filename: str) -> None:
  """
    Download a video from url to outfile.

    Args:
      - `url (str)` : URL of video (not ID!!)
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
  
  if not stream:
    print(f"Error: No stream found for {url}")
    raise Exception(f"No stream found for {url}")
  

  stream.download(filename=filename)
  print(f"Downloaded {filename} from {url}")
