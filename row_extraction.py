"""
Script for extracting certain rows based on condition. Here it is 
extraction of records of day = 1.

input : sample_data.csv
patient_id,age,gender,days,measurement_1,measurement_2
1,23,1,1,2,4
,23,1,2,3,5
,23,1,3,,3
2,25,2,1,1,4
,25,2,2,2,
,25,2,3,4,4
,25,2,4,,2
,25,2,5,1,6
3,45,1,1,1,4

output: output.csv
patient_id  age  gender  days  measurement_1  measurement_2
 1.0         23       1     1            2.0            4.0
 2.0         25       2     1            1.0            4.0
 3.0         45       1     1            1.0            4.0
"""

import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'

df = pd.read_csv("sample_data.csv")

#new_df= (df.loc[df['days_n'] == 1.0][required_list_of_column_names_list])  # can subset a required column alone
new_df= (df.loc[df['days'] == 1.0])                                         # extracting the first day rows alone
new_df.fillna("NA",inplace=True)                                            # replacing empty value with NA value
print(new_df)
#print(new_df.isna().sum())  # printing the empty NaN values for each columns
new_df.to_csv('output.csv',index=False)
