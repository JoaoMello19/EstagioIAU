import MyUtil
from collections import defaultdict
from datetime import datetime

import plotly.offline as py
import plotly.graph_objs as go

ANOS = range(2013, 2020)


def list_to_dict(lista):
    dicionario = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: 0)))
    for item in lista:
        dicionario[item['programa']][item['nivel']][item['nome']] = datetime.strptime(item['data'], '%d/%m/%Y')
    return dicionario


def get_intervalos(discs, trabs):
    tempos = defaultdict(lambda: defaultdict(lambda: []))
    for codigo in discs.keys():                             # para cada programa
        for nivel in discs[codigo].keys():                  # para cada nível
            for nome in discs[codigo][nivel].keys():        # para cada nome
                if nome in trabs[codigo][nivel].keys():     # se ha registro de incio E fim
                    t_delta = trabs[codigo][nivel][nome] - discs[codigo][nivel][nome]
                    tempos[nivel][codigo].append(t_delta.days / 365)
    return tempos


def get_code(code):
    new_code = code
    if code in programas_nivel.keys():
        new_code = programas_nivel[code]
    elif code in programas.keys():
        new_code = programas[code]
    return new_code


def sort_dict(dict_to_sort):
    return {get_code(value[0]): value[1] for value in sorted(dict_to_sort.items(),
                                                             key=lambda item: sum(item[1]) / len(item[1]))}


def make_chart(chart_data, chart_title):
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

    fig = go.Figure(layout=layout)
    for codigo in chart_data.keys():
        fig.add_trace(go.Box(y=chart_data[codigo],
                             name=codigo,
                             jitter=0.3,
                             pointpos=0,
                             boxpoints='all'))
    py.iplot(fig)


programas_nivel = MyUtil.read_programas_nivel()
programas = dict()

file_discentes = []
trabalhos_conclusao = []

for ano in ANOS:
    programas.update(MyUtil.read_programas(f'dados_arquitetura_{ano}/'))
    file_discentes.extend(MyUtil.read_file('discentes.xlsx', f'dados_arquitetura_{ano}/'))
    with open(f'dados_arquitetura_{ano}/trabalhos_conclusao.tsv') as file:
        trabalhos_conclusao.extend([row.split('\t') for row in file][1:])

discentes = list_to_dict([{
    'nome': row[8],
    'nivel': row[11],
    'programa': row[3],
    'data': row[13]
} for row in file_discentes])
file_discentes.clear()

trabalhos = list_to_dict([{
    'nome': row[1],
    'nivel': 'Mestrado' if row[22] == 'DISSERTAÇÃO' else 'Doutorado',
    'programa': row[16],
    'data': row[4]
} for row in trabalhos_conclusao])
trabalhos_conclusao.clear()

intervalos = get_intervalos(discentes, trabalhos)
intervalos['Mestrado'] = sort_dict(intervalos['Mestrado'])
intervalos['Doutorado'] = sort_dict(intervalos['Doutorado'])

'''for item in intervalos['Mestrado'].items():
    print(f'{item[0]} = {sum(item[1]) / len(item[1])}')'''

make_chart(sort_dict(intervalos['Mestrado']), f'Tempo até a Defesa da Dissertação {tuple(ANOS)}')
