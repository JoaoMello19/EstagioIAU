import pandas as pd
import os

caminhos = [os.path.join("dados_arquitetura_2018/docentes", nome) for nome in os.listdir("dados_arquitetura_2018/docentes")]
docentes = pd.DataFrame()

for path in caminhos:
    if "docentes" in path and "$" not in path:
        print(path)
        aux = pd.read_excel(path)
        programa = path[48:61]
        print(programa)
        aux.insert(0, "Programa", programa, True)
        
        del aux['Motivo do Afastamento']
        del aux['Data de Ínicio']
        del aux['Data de Fim']
        del aux['Instituição de Ensino Superior do Afastamento']
        aux = aux.drop_duplicates()
        aux = aux.reset_index(drop=True)
        
                
        docentes = docentes.append(aux, ignore_index=True)

docentes.to_csv("docentes.tsv", sep="\t", index=False, encoding='cp1252')

        

