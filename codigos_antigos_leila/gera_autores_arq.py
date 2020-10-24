import pandas as pd

periodicos = pd.read_csv("periodicos.tsv", sep='\t')
conferencias = pd.read_csv("conferencias.tsv",sep='\t')

autores = pd.DataFrame(columns=["Nome",	"Categoria", "Programa", "Posicao",	"Tipo"])

for index, row in periodicos.iterrows():
    print(index)
    for i in range(1,46):
        nome_coluna = "Autor%02d" % i
        if not pd.isnull(row[nome_coluna]):
            nova_linha = pd.DataFrame([(row[nome_coluna], row[nome_coluna+"-Cat"], row["Programa"], i, row['Subtipo da Produção'])], columns=["Nome",	"Categoria", "Programa", "Posicao",	"Tipo"])
            autores = autores.append(nova_linha, ignore_index=True)
        else:
            break
          
print("Acabou periodicos")
            
for index, row in conferencias.iterrows():
    print(index)
    for i in range(1,16):
        nome_coluna = "Autor%02d" % i
        if not pd.isnull(row[nome_coluna]):
            nova_linha = pd.DataFrame([(row[nome_coluna], row[nome_coluna+"-Cat"], row["Programa"], i, row['Subtipo da Produção'])], columns=["Nome",	"Categoria", "Programa", "Posicao",	"Tipo"])
            autores = autores.append(nova_linha, ignore_index=True)
        else:
            break
            

            
autores.to_csv("autores.tsv", index=False, sep="\t")
        


