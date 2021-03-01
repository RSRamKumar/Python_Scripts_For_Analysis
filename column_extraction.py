"""
script for extracting certain columns identified by indices  [0,8,9,48:51,56:123]
and fill "NA" in the blank cells.
"""
import pandas as pd
import numpy as np
pd.options.mode.chained_assignment = None  # default='warn'
a_df =  pd.read_excel("filename.xlsx",sheet_name="sheetname")
#print(list(enumerate(a_df.columns)))

b_df=a_df.iloc[:, np.r_[0,8,9,48:51,56:123]]
b_df.fillna("NA",inplace=True) # replacing empty value with NA value
print(b_df.isna().sum())  # printing the empty NaN values for each columns
b_df.to_csv('longitudinal_data.csv',index=False)
