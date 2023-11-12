#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
  Inference module for AWS Deployment.
"""

from pandas import DataFrame
from typing import Optional, Dict
import os

try:
  from clip import CLIP
  from bart import BART
  from utils import process_video
except ImportError:
  from .clip import CLIP
  from .bart import BART
  from .utils import process_video
import asyncio

def model_fn():
  """
    Load the model for inference
  """
  
  return {
      "clip": CLIP()
    , "bart": BART()
  }

def input_fn(req: Dict[str, str]) -> Optional[str]:
  
  # if "id" not in req and "url" not in req:
  #   return None
  
  
  video_id = req.get("video_id", "")
  video_url = req.get("video_url", "")
  
  if not (video_id or video_url):
    return ""
  
  elif not video_id:
    
    video_id: str = video_url.split(".com/watch?v=")[1]
    video_id = video_id.split("&")[0]
    print(f"video_id: {video_id}")
    
  return video_id

def predict_fn(video_id, models) -> Dict[str, str]:
  """
    Run inference on the model
  """

  data = process_video(video_id)
  
  # make sure models has clip and bart
  assert "clip" in models and "bart" in models, "Models must have clip and bart"
  
  clip: CLIP = models["clip"]
  bart: BART = models["bart"]
  
  if not os.path.exists("data/output"):
    os.mkdir("data/output")

  # can I run these in parallel?????
  bart_results: DataFrame = bart.inference(data["transcript"])
  
  # create output dir if nonexistent
  bart_results.to_csv(f"data/output/{video_id}_bart.csv")
  
  print(f"bart done!")
  clip_results: DataFrame = clip.inference(data["frames"])
  clip_results.to_csv(f"data/output/{video_id}_clip.csv")
  print(f"clip done!")
  
  return {
      "clip": clip_results.to_json()
    , "bart": bart_results.to_json()
  }
  
__all__ = ["model_fn", "input_fn", "predict_fn"]

def test():
  """
    Test the inference module
  """
  
  print(f"loading models...")
  models = model_fn()
  
  print(f"parsing request...")
  
  # parsed_req = input_fn({
  #     "body": {
  #         "url": "https://www.youtube.com/watch?v=k7RM-ot2NWY&list=PLZHQObOWTQDPD3MizzM2xVFitgF8hE_ab&index=2"
  #     }
  # }, "application/json")
  

  # print(f"running inference...")
  
  # results = predict_fn(parsed_req, models)
  
  # print(f"done!")
  
  # print(results)
  
if __name__ == "__main__":
  test()
