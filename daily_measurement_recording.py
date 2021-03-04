"""
For each patient, multiple day records of measurements are given. 
The script extracts the first and last day measure of a certain variable.
In this script, measurement_1 is taken for the first and last days and can 
be modified according to the scenario.

input: id_filled_file_sample.csv
patient_id,age,gender,measurement_1,measurement_2
1.0,23,1,2.0,4.0
1.0,23,1,3.0,5.0
1.0,23,1,,3.0
2.0,25,2,1.0,4.0
2.0,25,2,2.0,
2.0,25,2,4.0,4.0
2.0,25,2,,2.0
2.0,25,2,1.0,6.0
3,45,1,1,4

output: sample_data_curation_output.csv

patient_id,age,gender,measurement_1,measurement_2
1.0,23.0,1.0,2.0,nan
2.0,25.0,2.0,1.0,1.0
3.0,45.0,1.0,1.0,4.0
"""

import pandas as pd
from collections import defaultdict

df = pd.read_csv("id_filled_file_sample.csv")
def_dict = defaultdict(list)
for index, row in df.iterrows():
    def_dict[row["patient_id"]].append(list(row))
    
#print( (def_dict[1]))  # given a patient id, prints all the day records
#output:[[1.0, 23.0, 1.0, 2.0, 4.0], [1.0, 23.0, 1.0, 3.0, 5.0], [1.0, 23.0, 1.0, nan, 3.0]]
#print([i for i in def_dict if len(def_dict[i])==1]) #   patients with 1 day
#output:[3.0]

# writing to a csv file
f = open("sample_data_curation_output.csv","w")
f.write("{},{},{},{},{}\n".format("patient_id","age","gender","measurement_1","measurement_2"))
for ele in def_dict:
    if len(def_dict[ele])>1:
        patient_details_day_1,*_,patient_details_day_last = def_dict[ele]
        f.write("{},{},{},{},{}\n".format(patient_details_day_1[0],   # patient id
                                          patient_details_day_1[1],   # age
                                          patient_details_day_1[2],   # gender
                                          patient_details_day_1[3],   # measurement 1 - day 1
                                          patient_details_day_last[-2])) # measurement 1 - day last
    if len(def_dict[ele])==1:
        patient_details_day_1_day_last,*_ = def_dict[ele]
        f.write("{},{},{},{},{}\n".format(patient_details_day_1_day_last[0], # patient id
                                          patient_details_day_1_day_last[1], # age
                                          patient_details_day_1_day_last[2], # gender
                                          patient_details_day_1_day_last[3], # measurement 1 day 1
                                          patient_details_day_1_day_last[4])) # measurement 1 - day last

