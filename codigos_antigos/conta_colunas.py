from collections import defaultdict


anos = range(2013, 2020)
ocorrencia = defaultdict(lambda: list())
for ano in anos:
	with open(f'dados_arquitetura_{ano}/periodicos.tsv') as file:
		titulos = list(file)[0].split('\t')
		print(len(titulos), end='\n')
		for t in titulos:
			ocorrencia[t].append(ano)
print()
for k in titulos:
	if len(ocorrencia[k]) != 7:
		print(f'{len(ocorrencia[k])} : {ocorrencia[k]} : {k}')