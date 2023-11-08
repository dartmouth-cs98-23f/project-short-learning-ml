#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
  Inference module for AWS Deployment.
"""

from pandas import DataFrame
from clip import CLIP
from bart import BART

from typing import Optional, Dict

from utils import process_video
import asyncio

def model_fn():
  """
    Load the model for inference
  """
  
  return {
      "clip": CLIP()
    , "bart": BART()
  }

def input_fn(req, request_type) -> Optional[Dict[str, str]]:
  if request_type != "application/json":
    return None
  
  if "body" not in req:
    return None
  
  body = req["body"]
  
  id = body.get("id", None)
  url = body.get("url", None)
  
  assert id or url, "Must provide either id or url"
  
  if url and not id:
    id: str = url.split(".com/watch?v=")[1]
    id = id.split("&")[0]
    
  return { "id": id }

def predict_fn(parsed_req, models):
  """
    Run inference on the model
  """
  
  if not parsed_req or "id" not in parsed_req:
    return None

  data = process_video(parsed_req["id"])
  print(f"{data['transcript'] = }")
  
  # make sure models has clip and bart
  assert "clip" in models and "bart" in models, "Models must have clip and bart"
  
  clip: CLIP = models["clip"]
  bart: BART = models["bart"]
  
  # can I run these in parallel?????
  bart_results = bart.inference(data["transcript"])
  print(f"bart done!")
  print(f"{bart_results = }")
  clip_results = clip.inference(data["frames"])
  print(f"clip done!")
  
  return {
      "clip": clip_results.to_json()
    , "bart": bart_results.to_json()
  }

def test():
  """
    Test the inference module
  """
  
  print(f"loading models...")
  models = model_fn()
  
  print(f"parsing request...")
  
  parsed_req = input_fn({
      "body": {
          "url": "https://www.youtube.com/watch?v=k7RM-ot2NWY&list=PLZHQObOWTQDPD3MizzM2xVFitgF8hE_ab&index=2"
      }
  }, "application/json")
  

  print(f"running inference...")
  
  results = predict_fn(parsed_req, models)
  
  print(f"done!")
  
  print(results)
  
if __name__ == "__main__":
  test()
