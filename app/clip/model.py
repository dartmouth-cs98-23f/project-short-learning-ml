#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
  CLIP Model for Labeling.

  This wrapper around the CLIP model exposes a more friendly API
  for interacting with the model and auto-downloading the necessary.
"""

from typing import List

from PIL import Image
import numpy as np
from transformers import CLIPProcessor
from transformers import AutoModel
from pandas import DataFrame

class CLIP:

  def __init__(self, debug: bool = True):
    
    """
      - "openai/clip-vit-base-patch32"
        - smaller model, but less accuracy
      - "openai/clip-vit-large-patch14"
        - bigger model, but better accuracy
    """
    self.model = AutoModel.from_pretrained("openai/clip-vit-base-patch32")
    self.processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
    
    self.model.config.add_cross_attention = True
  
    self.decodes = 0
    self.trim_frames = False
    self.debug = debug

    self.categories = [
        #   "machine learning"        # computer science
        # , "computer graphics"       # computer science
        # , "web development"         # computer science

        # , "algebra"                 # mathematics
        # , "calculus"                # mathematics
        # , "statistics"              # mathematics

        # , "economics"               # economics
        # , "marketing"               # economics
        # , "commerce"                # economics

        # , "kinematics"              # physics
        # , "electromagnetism"        # physics
        # , "thermodynamics"          # physics

        # , "geology"                 # geography
        # , "cartography"             # geography
        # , "meteorology"             # geography

        # , "genetics"                # biology
        # , "biochemistry"            # biology
        # , "ecology"                 # biology
          "walls"
        , "ceiling"
        , "flooring"
        , "windows"
        , "furniture"
        , "lighting"
        , "decor"
        , "design"
      ]
    
  
    self.model.config.num_labels = len(self.categories)

  def __call__(self, labels: List[str], image: Image.Image):
    """
      Returns the similarity score between the text and image.

      Args:
        - `text (str)`: text to compare
        - `image (Image.Image)`: image to compare

      Returns:
        - `float`: similarity score
    """

    inputs = self.processor(text=labels, images=image, return_tensors="pt", padding=True)
    outputs = self.model(**inputs)
    
    logits_per_image = outputs.logits_per_image
    probs = logits_per_image.softmax(dim=1).detach().numpy()

    if self.debug:

      self.decodes += 1
      if self.decodes % 10 == 0:
        print(f"CLIP decodes: {self.decodes}")
    
    return probs
  
  def inference(self, frames: DataFrame):

    data = frames.copy()

    if self.trim_frames: data = data[:120] # focus on first 2 minutes

    runner = lambda x: self(self.categories, x)[0]

    extract_max = lambda x: [self.categories[i] for i in np.argsort(x)[-3:][::-1]]

    softmax_values = data["image"].apply(runner)

    # set category to the top 3 softmax values
    data["categories"] = softmax_values.apply(extract_max)

    # this is not needed, we can eventually drop it.
    # I just wanted to visualize the actual softmax values
    # for i in range(len(self.categories)):
    #   category = self.categories[i]
    #   data[category] = softmax_values.apply(lambda x: x[i])

    # save to csv the results (minus the image column)
    data = data.drop(columns=["image"])
    # data.to_csv(f"data/output/{id}.csv")
    return data
  

if __name__ == "__main__":

  model = CLIP()

  # maybe do something more interesting?
