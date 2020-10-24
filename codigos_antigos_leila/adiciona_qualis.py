import pandas as pd

periodicos = pd.read_csv("periodicos.tsv", sep='\t')

qualis = pd.read_csv("data/qualis-2017-2018.tsv", sep='\t')

qualis_dict={}

for index, row in qualis.iterrows():
    qualis_dict[row['ISSN']] = row['ESTRATO']

periodicos.insert(loc=0, column="Qualis", value="NA")
    
for index, row in periodicos.iterrows():
    issn = row['ISSN / Título do periódico'][0:9]
    if issn in qualis_dict:
        periodicos.at[index, 'Qualis'] = qualis_dict[issn]
        
periodicos.to_csv("periodicos.tsv", sep="\t", index=False)    
    
