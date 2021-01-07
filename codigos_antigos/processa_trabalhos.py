import pandas as pd
import os

caminhos = [os.path.join("dados_arquitetura_2013/trabalhos", nome) for nome in os.listdir("dados_arquitetura_2013/trabalhos")]
trabalhos = pd.DataFrame()

for path in caminhos:
    if "trabalhos" in path and "$" not in path:
        print(path)
        aux = pd.read_csv(path,encoding='latin-1', quotechar = '"', sep='\t')
        programa = path[50:63]
        print(programa)
        aux.insert(0, "Programa", programa, True)
        
        del aux['Banca']
        del aux['Categoria']
        del aux['Resumo']
        del aux['Abstract']
        aux = aux.drop_duplicates()
        aux = aux.reset_index(drop=True)
        nova_linha = aux.iloc[0].copy()
        
        for index, row in aux.iterrows():  
            if index==len(aux)-1 or aux['Título'].iloc[index+1] != row['Título']:                
                trabalhos = trabalhos.append(nova_linha, ignore_index=True)
                
                if index != len(aux)-1:
                    nova_linha = aux.iloc[index+1].copy()
            
        
trabalhos.to_csv("trabalhos_conclusao.tsv", sep="\t", index=False)

        

