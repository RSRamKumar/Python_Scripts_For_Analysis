"""
sample meta data file creation with the json conversion
for each variables like measurements, it is best to include a min-max range. 
If empty elements are present, those are dropped and the range is calculated.

input_file: "id_filled_file_sample.csv"
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

meta_data_file_after_creating: "sample_meta_data.csv"
variable;value;type;datatype;unit_of_measures
patient_id;(1.0,3.0);continuous;float64;
age;(23,45);continuous;int64;
gender;(1,2);continuous;int64;
measurement_1;(1.0,4.0);continuous;float64;
measurement_2;(2.0,6.0);continuous;float64;

"""
import pandas as pd
import numpy as np
df = pd.read_csv("id_filled_file_sample.csv")

#meta_df=df.iloc[:, np.r_[0,2,5:65]]  # to include only certain columns in the file, indices could be provided directly

f = open("sample_meta_data.csv","w")
f.write("{};{};{};{};{}\n".format("variable","value","type","datatype","unit_of_measures"))
for col in df.columns:
    col_val = df[col]
    type = "continuous"  # can be continuous,binary,trinary etc
    na_dropped_list = col_val.dropna().tolist()
    min_val,max_val,data_type= min(na_dropped_list) , max(na_dropped_list), (col_val).dtypes
    f.write("{};({},{});{};{};{}\n".format(col,min_val,max_val,type,data_type,""))
f.close()

## df to json
meta_df = pd.read_csv("sample_meta_data.csv",sep=';',index_col=False )
print(meta_df["value"].head())
meta_df.to_json ("meta_data_json.json", orient='records',indent=5)
