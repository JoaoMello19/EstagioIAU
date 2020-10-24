import pandas as pd
import os

caminhos = [os.path.join("data", nome) for nome in os.listdir("data")]
print(caminhos[0])
programas = pd.DataFrame(columns=["Instituição de Ensino","Programa","Sigla", "Tem Doutorado"])
for path in caminhos:
    if "programas" in path:
        aux = pd.read_excel(path)
        for index, row in aux.iterrows():
            verifica = programas.index[(programas['Programa'] == row['Código do PPG'])]
            if len(verifica) == 0:
                novo_prog = {"Sigla":row['IES Sigla'], "Instituição de Ensino": row['IES Nome'], "Programa": row['Código do PPG'], "Tem Doutorado": "NÃO"}
                programas = programas.append(novo_prog, ignore_index=True)
            elif row['Nível do Curso'] == 'Doutorado':
                programas['Tem Doutorado'].iloc[verifica[0]] =  'SIM'
            

programas.to_csv("progs.tsv", sep="\t")
print(programas.head(5))

