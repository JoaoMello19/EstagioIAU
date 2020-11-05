import plotly.offline as py
import plotly.graph_objs as go

import MyUtil
from collections import defaultdict

PATH = '/home/joaomello/Documentos/USP/IC - Analise de Dados/Arquitetura/dados_arquitetura_2017/'


def read_trabalhos():
    registers = MyUtil.read_file('trabalhos_conclusao.xlsx', PATH)
    trabalhos = defaultdict(lambda: defaultdict(lambda: set()))

    for row in registers:
        # [code][tipo] = titulos
        trabalhos[row[3]][row[10]].add(row[9])

    return trabalhos


def read_docentes():
    """
    Função que recupera e processa os dados de interesse
    :return: um dicionario, com os dados de interesse
    """
    registers = MyUtil.read_file('docentes.xlsx', PATH)

    docentes = defaultdict(lambda: list())
    for row in registers:
        docentes[row[3]].append({
            'name': row[8],
            'category': row[12]
        })

    return docentes


def get_docentes_programa(p_code):
    """
    Função que avalia e calcula a média de docentes por categoria
    :param p_code: dicionário com chaves equivalentes ao nomes e valores equivalentes a categoria
    :return: a média por codigo
    """
    names_categories = dict()

    for docente in p_code:
        if docente['name'] not in names_categories.keys():  # primeira vez que o docente é registrado
            names_categories[docente['name']] = docente['category']

        elif names_categories[docente['name']] not in ('BOTH', docente['category']):
            # registrado como outra categoria -> pertence a ambas
            names_categories[docente['name']] = 'BOTH'

    docentes_programa = {'PERMANENTE': 0, 'COLABORADOR': 0, 'total': 0}
    for category in names_categories.values():
        if category in ('PERMANENTE', 'COLABORADOR'):
            docentes_programa[category] += 1
        else:  # ambas as categorias
            docentes_programa['PERMANENTE'] += 0.5
            docentes_programa['COLABORADOR'] += 0.5
        docentes_programa['total'] += 1

    return docentes_programa


def get_docentes_programas(docentes):
    """
    Função que calcula todas as médias
    :param docentes: os dados recolhidos
    :return: a média individual de cada programa
    """
    codes = {code for code in docentes.keys()}
    doc_prog = defaultdict(lambda: {
        'PERMANENTE': 0,
        'COLABORADOR': 0,
        'total': 0
    })

    for code in codes:
        d_programa = get_docentes_programa(docentes[code])
        doc_prog[code]['PERMANENTE'] += d_programa['PERMANENTE']
        doc_prog[code]['COLABORADOR'] += d_programa['COLABORADOR']
        doc_prog[code]['total'] += d_programa['total']

    return doc_prog


def get_formandos_by(trabalhos, t_formandos):
    result = defaultdict(lambda: list())
    for code in trabalhos:
        if len(trabalhos[code][t_formandos]) > 0:
            result[code] = [autor for autor in trabalhos[code][t_formandos]]
    return result


def get_docentes_by(d_programas, categoria):
    if categoria in ('PERMANENTE', 'COLABORADOR'):
        return {code: d_programas[code][categoria] for code in d_programas.keys()}
    else:
        return {code: d_programas[code]['total'] for code in d_programas.keys()}


def get_formandos_docentes(trabalhos, t_formandos, docentes, t_docentes='total'):
    formandos = get_formandos_by(trabalhos, 'TESE' if t_formandos == 'doutores' else 'DISSERTAÇÃO')     # {code: nomes}
    count_formandos = {code: len(nomes) for code, nomes in formandos.items()}                           # {code: count}
    docentes_t = get_docentes_by(docentes, t_docentes)

    formandos_docentes = defaultdict(lambda: 0)
    for code in formandos.keys():
        new_code = code
        if code in programas_nivel.keys():
            new_code = programas_nivel[code]
        elif code in programas.keys():
            new_code = programas[code]
        formandos_docentes[new_code] += count_formandos[code] / docentes_t[code]

    return formandos_docentes


def make_chart(chart_data, chart_title):
    data = [go.Bar(x=[code for code in chart_data.keys()],
                   y=[value for value in chart_data.values()],
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
                       xaxis={'title': 'Instituição'},
                       barmode='stack')
    fig = go.Figure(data=data, layout=layout)
    py.iplot(fig)


def sort_dict(dict_to_sort):
    return {value[0]: value[1] for value in sorted(dict_to_sort.items(), key=lambda item: item[1])}


programas = MyUtil.read_programas(PATH)
programas_nivel = MyUtil.read_programas_nivel()

list_trabalhos = read_trabalhos()
list_docentes = read_docentes()
docentes_programas = get_docentes_programas(list_docentes)

doutores_docente = sort_dict(get_formandos_docentes(list_trabalhos, 'doutores', docentes_programas))
doutores_permanente = sort_dict(get_formandos_docentes(list_trabalhos, 'doutores', docentes_programas, 'PERMANENTE'))
mestres_docente = sort_dict(get_formandos_docentes(list_trabalhos, 'mestres', docentes_programas))
mestres_permanente = sort_dict(get_formandos_docentes(list_trabalhos, 'mestres', docentes_programas, 'PERMANENTE'))

make_chart(doutores_docente, 'Doutores por Docente')
make_chart(doutores_permanente, 'Doutores por Docente Permanente')
make_chart(mestres_docente, 'Mestres por Docente')
make_chart(mestres_permanente, 'Mestres por Docente Permanente')
