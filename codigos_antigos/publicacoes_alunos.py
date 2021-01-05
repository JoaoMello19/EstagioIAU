import plotly.offline as py
import plotly.graph_objs as go

import MyUtil

from collections import defaultdict

ANOS = tuple(range(2013, 2020))

FILE_PERIODICOS = 'periodicos.tsv'
FILE_CONFFERENCIAS = 'conferencias.tsv'
FILE_DISCENTES = 'discentes.xlsx'
FILE_PATH = 'dados_arquitetura_'

COLORS = ("#FF0000", "#FF8800", "#FFFF00", "#00FF00", "#0000FF", "#FF00FF")


def read_publicacao(path, file_name):
    with open(path + file_name, encoding='latin-1') as linhas:
        publicacoes = [linha.split('\t') for linha in linhas]
        del publicacoes[0]  # sem os titulos das colunas
        for publicacao in publicacoes:
            del publicacao[-1]
        return publicacoes


def get_num_discentes(publicacao, start):
    return len([publicacao[i] for i in range(start, len(publicacao), 2) if 'Discente' in publicacao[i + 1]])


def get_discentes_periodico(publicacoes):
    discentes_programa = defaultdict(lambda: defaultdict(lambda: 0))
    for publicacao in publicacoes:
        code = publicacao[3]
        n_discentes = get_num_discentes(publicacao, 29)
        discentes_programa[code][n_discentes] += 1
    return discentes_programa


def get_discentes_conferencia(publicacoes):
    discentes_programa = defaultdict(lambda: defaultdict(lambda: 0))
    for publicacao in publicacoes:
        code = publicacao[3]
        n_discentes = get_num_discentes(publicacao, 32)
        discentes_programa[code][n_discentes] += 1
    return discentes_programa


def get_max_discentes_programa(discentes_programa):
    max_d = 0
    for dp in discentes_programa.values():
        max_d = max(max_d, max(dp.keys()))
    return max_d


def set_percentage(disc_prog):
    for k1 in disc_prog.keys():
        total = sum(disc_prog[k1].values())
        for k2 in disc_prog[k1].keys():
            disc_prog[k1][k2] /= total / 100
        # disc_prog[k1]['total'] = total


def set_code(code):
    if code in programas_nivel.keys():
        return programas_nivel[code]
    elif code in nomes_programas.keys():
        return nomes_programas[code]
    return code


def sort_dict(to_sort):
    global MAX_DISCENTES
    to_sort = [(k, to_sort[k]) for k in to_sort.keys()]
    for i in range(MAX_DISCENTES, -1, -1):
        to_sort = sorted(to_sort, key=lambda item: item[1][i], reverse=True)
    to_sort = {set_code(key): value for key, value in to_sort}
    return to_sort


def make_chart(chart_data, chart_title):
    global MAX_DISCENTES
    data = list()
    for i in range(MAX_DISCENTES + 1):
        data.append(go.Bar(x=list(chart_data.keys()),
                           y=[d_prog[i] for d_prog in chart_data.values()],
                           text=[round(d_prog[i], 2) if d_prog[i] > 0 else '' for d_prog in chart_data.values()],
                           textposition='inside',
                           name=f'{i:2} aluno(s)'))

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
                       xaxis={'title': 'Instituição'},
                       barmode='stack')

    fig = go.Figure(data=data, layout=layout)
    py.iplot(fig)


ano = 2019
programas_nivel = MyUtil.read_programas_nivel()
nomes_programas = dict()
periodicos = []
conferencias = []

for ANO in ANOS:
    nomes_programas.update(MyUtil.read_programas(FILE_PATH + str(ANO) + '/'))
    periodicos.extend(read_publicacao(FILE_PATH + str(ANO) + '/', FILE_PERIODICOS))
    conferencias.extend(read_publicacao(FILE_PATH + str(ANO) + '/', FILE_CONFFERENCIAS))

d_periodicos = get_discentes_periodico(periodicos)
MAX_DISCENTES = get_max_discentes_programa(d_periodicos)
set_percentage(d_periodicos)
d_periodicos = sort_dict(d_periodicos)
make_chart(d_periodicos, f"Porcentagem das Publicações em Periódico por Número de Alunos {ANOS}")

d_conferencias = get_discentes_conferencia(conferencias)
MAX_DISCENTES = get_max_discentes_programa(d_conferencias)
print(MAX_DISCENTES)
set_percentage(d_conferencias)
d_conferencias = sort_dict(d_conferencias)
make_chart(d_conferencias, f"Porcentagem das Publicações em Conferência por Número de Alunos {ANOS}")