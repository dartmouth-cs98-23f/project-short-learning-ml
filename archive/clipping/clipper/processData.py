import os
from pprint import pprint 
from sklearn.preprocessing import LabelEncoder
import ast
import pandas as pd

os.chdir(os.path.abspath(os.path.dirname(__file__)))

data_file = 'AhW3jlg7NQw_bart.csv'
data_dir = '../../../app/data/output/'
file_path = data_dir+data_file

df = pd.read_csv(file_path)

# convert the string representation of results to a list
df['list_categories'] = df['categories'].apply(ast.literal_eval)

# get most likely label from each list
df['label'] = df['list_categories'].apply(lambda x: x[0] if x else None)

# initialize the LabelEncoder
label_encoder = LabelEncoder()

# fit and transform the label to a numerical value
numerical_data = label_encoder.fit_transform(df['label'])

df['label_value'] = numerical_data
print(df)