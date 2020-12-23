import plotly.offline as py
import plotly.graph_objs as go

import MyUtil
from collections import defaultdict

FILE_NAME = 'periodicos.tsv'
FILE_PATH = 'dados_arquitetura_'
ANOS = range(2013, 2020)


def read_publicacao(path, file_name):
    with open(path + file_name, encoding='latin-1') as linhas:
        publicacoes = [linha.split('\t') for linha in linhas]
        del publicacoes[0]  # sem os titulos das colunas
        for publicacao in publicacoes:
            del publicacao[-1]
        return publicacoes


def get_autores_programas(publicacoes):
    autores = defaultdict(lambda: [])
    for p in publicacoes:
        for i in range(29, len(p), 2):
            if p[i + 1] == 'Docente':
                autores[p[3]].append(p[i])
    return autores


def sort_dict(to_sort):
    aux = [(k, v) for k, v in to_sort.items()]  # transfora em tuplas (chave, valor)
    aux = sorted(aux, key=lambda t: t[1])       # ordena pelo indice 1
    aux = {v[0]: v[1] for v in aux}             # retorna para dicionario, ordenado pelo valor
    return aux


def get_gini_programa(autores_programa):
    freq_nome = defaultdict(lambda: 0)  # frequencia de aparição de cada nome
    for nome in autores_programa:
        freq_nome[nome] += 1
    freq_nome = list(sort_dict(freq_nome).values())

    X = [0]
    X.extend([n / len(freq_nome) for n in range(len(freq_nome))])   # freq acumulada de populacao

    total = sum(freq_nome)
    Y = [0]
    for i in range(len(freq_nome)):
        Y.append(Y[i] + freq_nome[i] / total)               # freq acumulada de ocorrencia

    gini = 1
    for i in range(len(freq_nome)):
        gini -= (X[i + 1] - X[i]) * (Y[i + 1] - Y[i])

    return round(gini, 2)


def set_code(code):
    if code in programas_nivel.keys():
        return programas_nivel[code]
    elif code in nomes_programas.keys():
        return nomes_programas[code]
    return code


def make_chart(chart_data, chart_title):
    data = [go.Bar(x=[code for code in chart_data.keys()],
                   y=[value for value in chart_data.values()],
                   text=list(chart_data.values()),
                   textposition='outside',
                   marker={'color': '#0000FF'})]

    title = {
        'text': chart_title,
        'x': 0.5,
        'xanchor': 'center',
        'font': {
            'color': '#000000',
            'size': 20
        }
    }

    layout = go.Layout(title=title,
                       xaxis={'title': 'Instituição'})
    fig = go.Figure(data=data, layout=layout)
    py.iplot(fig)


for ANO in ANOS:
    nomes_programas = MyUtil.read_programas(FILE_PATH + str(ANO) + '/')
    programas_nivel = MyUtil.read_programas_nivel()

    periodicos = read_publicacao(FILE_PATH + str(ANO) + '/', FILE_NAME)
    autores_programas = get_autores_programas(periodicos)
    ginis = {set_code(ap[0]): get_gini_programa(ap[1]) for ap in autores_programas.items()}
    ginis = sort_dict(ginis)

    make_chart(ginis, f"Coeficiente Gini {ANO}")
