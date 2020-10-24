import pandas as pd
import os

caminhos = [os.path.join("data", nome) for nome in os.listdir("data")]
periodicos = pd.DataFrame()
conferencias = pd.DataFrame()
for path in caminhos:
    if "producoes" in path and "$" not in path:
        print(path)
        aux = pd.read_excel(path)
        del aux['Calendário']
        del aux['Data-Hora do Envio']
        del aux['Ano do Calendário']
        aux  = aux.rename(columns={"Código do PPG": "Programa"})
        nova_linha = aux.iloc[0].copy()
        for index, row in aux.iterrows():
            if row['Subtipo da Produção'] == 'ARTIGO EM PERIÓDICO' or row['Subtipo da Produção'] == 'TRABALHO EM ANAIS':
                if index<len(aux)-1 and aux['Título da Produção'].iloc[index+1] == row['Título da Produção']:
                    if not pd.isnull(row['Número de Ordem Autor']):
                        nome_coluna = "Autor%02d" % row['Número de Ordem Autor']
                        nova_linha[nome_coluna] = row['Nome do Autor']
                        nova_linha[nome_coluna+'-Cat'] = row['Categoria do Autor']
                    else:
                        nova_linha[row['Nome do Detalhamento']] = row['Valor do Detalhamento']
                else:
                    nome_coluna = "Autor%02d" % row['Número de Ordem Autor']
                    nova_linha[nome_coluna] = row['Nome do Autor']
                    nova_linha[nome_coluna+'-Cat'] = row['Categoria do Autor']
                    del nova_linha['Nome do Autor']
                    del nova_linha['Número de Ordem Autor']
                    del nova_linha['Categoria do Autor']
                    del nova_linha['Nome do Detalhamento']
                    del nova_linha['Valor do Detalhamento']
                    if row['Subtipo da Produção'] == 'ARTIGO EM PERIÓDICO':
                        periodicos = periodicos.append(nova_linha, ignore_index=True)
                    elif row['Subtipo da Produção'] == 'TRABALHO EM ANAIS':
                        conferencias = conferencias.append(nova_linha, ignore_index=True)
                    if index != len(aux)-1:
                        nova_linha = aux.iloc[index+1].copy()
            else:
                if index != len(aux)-1:
                        nova_linha = aux.iloc[index+1].copy()
        

print("aqui") 
periodicos = periodicos.reindex(sorted(periodicos.columns), axis=1)
conferencias = conferencias.reindex(sorted(conferencias.columns), axis=1)
periodicos.to_csv("periodicos.tsv", sep="\t", index=False)
conferencias.to_csv("conferencias.tsv", sep="\t", index=False)    

        

