"""
The input file contains a list of drugs (separated by comma) used in a each patient.
The script converts the single row record into a multi line record by taking its identifiers too. 
input:
id,days,therapy
01,5,abc,daa,cab
02,6,kat,gat

output:
01,5,abc
01,5,daa
01,5,cab
02,6,kat
02,6,gat
"""


import pandas as pd
import numpy as np

df = pd.read_csv("file.csv")

df['THERAPY'] = df['THERAPY'].apply(lambda a: a.split(',') ) # str to list conversion

sample_list = list()                                         #  a list to hold (id,day,drug name) as a tuple
for index, row in df.iterrows():
    therapy_list = row['THERAPY']
    for ele in therapy_list:
        sample_list.append((row['id'], row['days_n'], ele.rstrip().lstrip()))

drug_df = pd.DataFrame(sample_list,columns=df.columns)
 
drug_df.to_csv('output.csv',index=False)

#https://datatofish.com/list-to-dataframe/
