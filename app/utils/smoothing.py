#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
  A few utilities for CLIP and BART
"""

import pandas as pd

def tfidf(df: pd.DataFrame, /, start_column=0) -> pd.DataFrame:
  """
    TDIDF (Term Frequency Inverse Document Frequency) is often used as a way
    of mitigating the effect of common words in a corpus.
    
    For example, if we have a corpus of 100 documents, and the word "the" appears
    in 99 of them, then the word "the" is not very useful for distinguishing
    between documents.
    
    Since we want to use keywords in specific subdomains of computer science,
    it is likely that certain keywords will appear across many time periods in a video
    (for example, "JOIN" or "SELECT" in SQL).
    We don't want to throw such keywords out entirely since they are relevant to the subject,
    but we need a way to measure how "useful" a keyword's presence in a specific time period is.
    
    This function computes tf-idf for a given input dataframe.
    
    This does the following:
    
    1. Divides each cell by the sum of the column (if nonzero),
       so values that appear across all rows are weighted less.
       it ignores the rows before the start column (int index),
       if provided.
       
    2. Normalizes so each row adds up to 1,
       so values do not vanish or explode.
       
    Parameters
    ----------
    df: pd.DataFrame
      The dataframe to compute tf-idf on.
      NOTE: We create a copy of this dataframe, so the original is not modified.
      
    start_column: int (optional)
      The column (index) to start tf-idf on.
      This is useful to avoid computing on the first few columns which may be row labels.
      
    Returns
    -------
    A new dataframe with tf-idf applied.
    
    Example
    -------
    >>> df = pd.DataFrame([
    ...   [1, 1, 1],
    ...   [0, 0, 0],
    ...   [3, 2, 0]
    ... ], columns=["a", "b", "c"])
    >>> tfidf(df) # notice how the first column is re-weighted based on uniqueness
    ...             a         b         c
    ...   0  0.157895  0.210526  0.631579
    ...   1  0.000000  0.000000  0.000000
    ...   2  0.529412  0.470588  0.000000
  """
  
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
