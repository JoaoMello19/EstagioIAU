import pandas as pd
import os

caminhos = [os.path.join("data", nome) for nome in os.listdir("data")]
print(caminhos[0])
docentes = pd.DataFrame()
for path in caminhos:
    if "docentes" in path:
        aux = pd.read_excel(path)
        # for index, row in aux.iterrows():    
        #     novo_docente = {"Ano Titulação": row['Ano Titulação'],"Categoria" : row['Categoria'],"Instituição de Ensino" : row['IES Nome'],"Nome" : row['Nome Docente'],"Programa" : row['Código do PPG'],"Regime de Trabalho": row['Regime de Trabalho']}
        #     docentes = docentes.append(novo_docente, ignore_index=True)
        del aux['Calendário']
        del aux['Data-Hora do Envio']
        aux  = aux.rename(columns={"Código do PPG": "Programa"})
        docentes = docentes.append(aux, ignore_index=True)
            

docentes.to_csv("docentes.tsv", sep="\t")
print(docentes.head(5))

