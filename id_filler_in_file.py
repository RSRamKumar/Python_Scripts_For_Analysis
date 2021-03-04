"""
The input file contains the patient id only for the first row and it has to be
extended till it sees the next patient id.
input: sample_data.csv
patient_id,age,gender
1,23,1
,23,1
,23,1
2,25,2
,25,2
,25,2
,25,2
,25,2

output: id_filled_file_sample.csv
patient_id,age,gender
1.0,23,1
1.0,23,1
1.0,23,1
2.0,25,2
2.0,25,2
2.0,25,2
2.0,25,2
2.0,25,2

"""

import pandas as pd

df = pd.read_csv("sample_data.csv")

patient_id_index = df[df['patient_id'].notnull()].index.tolist() # prints the indexes where ids are present

id_present_index = [] # indexes where patient ids are present (should be equal to patient_id_index after run)
id_not_present_index = [] # indexes where patient ids are absent
for index, row in df.iterrows():
    if index in patient_id_index:
        id_present_index.append(index)  # if index present put in the list "present"
    if index not in patient_id_index:
        id_not_present_index.append(index) # if index absent put in the list "not present"
        # operation for filling patient id based on previously present ids
        df.at[index, "patient_id"] = df.iloc[id_present_index[-1]].patient_id

print(len(id_not_present_index)+len(id_present_index) == df.shape[0])
assert patient_id_index == id_present_index
df.to_csv("id_filled_file_sample.csv",index=False)

#https://stackoverflow.com/questions/23330654/update-a-dataframe-in-pandas-while-iterating-row-by-row
