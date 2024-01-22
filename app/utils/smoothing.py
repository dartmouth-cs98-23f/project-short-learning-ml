#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
  A few utilities for CLIP and BART
"""

import pandas as pd

def tfidf(df: pd.DataFrame, /, start_column=0) -> pd.DataFrame:
  
  #? copy everything after the start column, inclusive
  df = df.iloc[:, start_column:].copy()

  #? compute sums for each column (keyword)
  sums = df.sum(axis=0)
  
  #? divide each cell by the sum of the column (if nonzero)
  for col in df.columns:
    if sums[col] != 0:
      df[col] = df[col] / sums[col]
      
  #? normalize so each row adds up to 1
  df = df.div(df.sum(axis=1), axis=0)
  
  #? replace NaNs with 0s
  df = df.fillna(0)
  
  return  df


### TESTS ###
def test():
  df = pd.DataFrame([
    [1, 1, 1],
    [0, 0, 0],
    [3, 2, 0]
  ], columns=["a", "b", "c"])
  
  print(df)
  print(tfidf(df))
  
if __name__ == "__main__":
  test()
