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
from transformers import pipeline
from transformers import AutoModelForSequenceClassification, AutoTokenizer

import utils

class BART:

  def __init__(self, multi_label: bool = False):

    self.tokenizer = AutoTokenizer.from_pretrained('facebook/bart-large-mnli')
    self.model = AutoModelForSequenceClassification.from_pretrained('facebook/bart-large-mnli')
    # self.model = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
    
    # self.model.config.add_cross_attention = True
  
    self.decodes = 0
    self.trim_frames = True

    self.categories = [
          "machine learning"        # computer science
        , "computer graphics"       # computer science
        , "web development"         # computer science

        , "algebra"                 # mathematics
        , "calculus"                # mathematics
        , "statistics"              # mathematics

        , "economics"               # economics
        , "marketing"               # economics
        , "commerce"                # economics

        , "kinematics"              # physics
        , "electromagnetism"        # physics
        , "thermodynamics"          # physics

        , "geology"                 # geography
        , "cartography"             # geography
        , "meteorology"             # geography

        , "genetics"                # biology
        , "biochemistry"            # biology
        , "ecology"                 # biology
      ]
    
    self.multi_label = multi_label

  def __call__(self, premise: str, categories: List[str]) -> float:
    """
      Returns the similarity score between the text and image.

      Args:
        - `text (str)`: text to compare
        - `image (Image.Image)`: image to compare

      Returns:
        - `float`: similarity score
    """

    categories = []

    for category in self.categories:
      tokens = self.tokenizer.encode(premise, category, return_tensors='pt')
      logits = self.model(tokens)[0]

      logits = logits[:, [0, 2]]
      probs = logits.softmax(dim=1)
      res = probs[:,1]
      categories.append(res.item())

    self.decodes += 1
    if self.decodes % 10 == 0:
      print(f"Decodes: {self.decodes}")
    return categories
  
  def process(self, id: str):

    data = utils.load_data(id)

    # retain transcript only
    data = data[["second", "transcript" ]]

    # keep every five seconds
    data = data[data["second"] % 5 == 0]

    if self.trim_frames: data = data[:60] # focus on first 2 minutes

    runner = lambda x: self(x, self.categories)

    scores = data["transcript"].apply(runner)
    for i in range(len(self.categories)):
      data[self.categories[i]] = scores.apply(lambda x: x[i])

    # get top 3 categories
    top_3 = data[self.categories].apply(lambda x: list(reversed(np.argsort(x)[-3:].tolist())), axis=1)
    data["categories"] = top_3.apply(lambda x: [self.categories[i] for i in x])
    # set second as index
    data.set_index("second", inplace=True)
    data = data[["categories", "transcript"] + self.categories]

    data.to_csv(f"data/output/{id}.csv")
    return data


if __name__ == "__main__":
  model = BART()

  # maybe do something more interesting?
