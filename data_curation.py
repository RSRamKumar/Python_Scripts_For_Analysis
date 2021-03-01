"""
script for data curation 
patient_id,days,drug
in a single row for each drug
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

sample_list = list()
for index, row in df.iterrows():
    therapy_list = row['THERAPY']
    for ele in therapy_list:
        sample_list.append((row['id'], row['days_n'], ele.rstrip().lstrip()))

#print(sample_list)


drug_df = pd.DataFrame(sample_list,columns=df.columns)

#print(drug_df.tail(15))

drug_df.to_csv('output.csv',index=False)

#https://datatofish.com/list-to-dataframe/

