"""
input:
patient_id,days,drug_a,drug_b,drug_c,drug_d,drug_e
1,1,1,0,1,0,1
...
2,6,1,1,1,1,1
output:
1,1,drug_a
1,1,drug_c
1,1,drug_e
2,6,drug_a
2,6,drug_b
2,6,drug_c
2,6,drug_d
2,6,drug_e
"""

import pandas as pd

df = pd.read_excel("filename.xlsx",sheet_name="sheet1")


cols=["id","days_n", "drug_a","drug_b","drug_c","drug_d","drug_e"]
drug_df= (df.loc[df['days'] == 1.0][cols])   # filtering only for day 1 
#print(drug_df) 

 
sample_list = list()
for index, row in drug_df.iterrows():
    sample_list.append(( row['id'],{"drug_a":row['drug_a'],
                         "drug_b":row['drug_b'],
                         "drug_c":row['drug_c'],
                         "drug_d" :row['drug_d'],
                         "drug_e": row['drug_e'] }))
 

f = open("output.csv","w")
f.write("{},{},{}\n".format("id","days_n","drugs"))
for a,b in sample_list:
    if b["drug_a"]!=0:
        f.write("{},{},{}\n".format(a,1,"drug_a"))
    if b["drug_b"]!=0:
        f.write("{},{},{}\n".format(a,1,"drug_b"))
    if b["drug_c"]!=0:
        f.write("{},{},{}\n".format(a,1,"drug_c"))
    if b["drug_d"]!=0:
        f.write("{},{},{}\n".format(a,1,"drug_d"))
    if b["drug_e"]!=0:
        f.write("{},{},{}\n".format(a,1,"drug_e"))
     
