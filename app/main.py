#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
  FastAPI wrapper for model.
"""

from fastapi import FastAPI
from typing import Optional, Dict

from inference import model_fn, input_fn, predict_fn

# init model
models = model_fn()
print("models loaded!")

app = FastAPI()

@app.get("/")
def read_root():
  return {"message": "Hello from Discite ML API!"}

@app.get("/split")
async def split_video( video_id: Optional[str] = None, video_url: Optional[str] = None) -> Dict[str, str]:
  """
    Split a video into frames and extract transcript.
    
    Args:
      - `video_id (str)`: youtube video id
      - `video_url (str)`: youtube video url
      
    Returns:
      - `Dict[str, str]`: message
  """
  print(f"{video_id = }")
  print(f"{video_url = }")
  input = input_fn({ "video_id": video_id or "", "video_url": video_url or "" })
  
  if not input:
    return {"message": "No video_id or video_url provided"}
  
  # run inference
  result = predict_fn(input, models)
  
  
  return result


