"""
input:
id,days,col_a,col_b,col_c,col_d,col_e
1,4,1,4,4,6,6
2,1,1,NA,2,2,1
1,1,2,3,4,5,5
output:
id,days,col_a,col_b,col_c,col_d,col_e
1,4,1,4,4,6,6
1,1,2,3,4,5,5
"""
import pandas as pd
import numpy as np
pd.options.mode.chained_assignment = None  # default='warn'
input_df =  pd.read_excel("input.xlsx",sheet_name="name")
print(list(enumerate(input_df.columns)))

data_df=input_df.iloc[:, np.r_[0,8,125:130]]  # splicing required columns
#print(data_df.shape)
#print(data_df.head(20))
#print(data_df.dtypes)

data_df.fillna("NA",inplace=True)
#print(data_df.isna().sum())
f=open("output.csv","w")
f.write("{},{},{},{},{},{},{}\n".format('id','days_n','col_a','col_b','col_c',
                                          'col_d',
                                          'col_e'))
for index, row in imaging_data_df.iterrows():
      df_dict=row.to_dict()
    # print(index,[type(i) for i in df_dict.values() if i])
    # print(index,[i for i in df_dict.values()])
    # print("*" * 50)
    if isinstance(row["col_a"],float)  or \
        isinstance(row["col_b"],float) or \
        isinstance(row["col_c"], float) or \
        isinstance(row["col_d"], float) or \
        isinstance(row["col_e"], float):
        f.write("{},{},{},{},{},{},{}\n".format(row['id'], row['days_n'],
                                          row['col_a'],
                                          row['col_b'],
                                          row['col_c'],
                                          row['col_d'],
                                          row['col_e']))

        
# conversion of csv file into a json file
metadata_df = pd.read_csv("meta_data_filled.csv")
metadata_df.to_json ("meta_data.json", orient='records',indent=4)
