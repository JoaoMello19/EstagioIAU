import plotly.offline as py
import plotly.graph_objs as go

import MyUtil, MyClasses
from collections import defaultdict

PATH = 'dados_arquitetura_2016/'
TIPO_QUALIS = ('A1', 'A2', 'A3', 'A4', 'B1', 'B2', 'B3', 'B4', 'B5', 'C', 'NA', 'NP')
PESO_QUALIS = {'A1': 1, 'A2': 0.875, 'A3': 0.75, 'A4': 0.625, 'B1': 0.5, 'B2': 0.2, 'B3': 0.1, 'B4': 0.05, 'B5': 0,
               'C': 0, 'NA': 0, 'NP': 0}
COLOR_QUALIS = {'A1': '#000044', 'A2': '#000088', 'A3': '#0000CC', 'A4': '#0000FF',
                'B1': '#003300', 'B2': '#006600', 'B3': '#009900', 'B4': '#00CC00', 'B5': '#00FF00',
                'C': '#880000', 'NA': '#CC0000', 'NP': '#FF0000'}


def new_quali_dict():
    # cria um dicionario padrao para armazenar os qualis
    quali_dict = {quali: 0 for quali in TIPO_QUALIS}
    quali_dict['total'] = 0
    return quali_dict


def read_periodicos():
    # leitura dos periodicos
    periodicos = list()
    with open(PATH + 'periodicos.tsv') as file:
        for row in file:
            cells = str(row).split('\t')
            new_periodico = MyClasses.Periodico(*cells[:32])
            new_periodico.add_authors(*cells[32:-1])
            periodicos.append(new_periodico)
    del periodicos[0]
    return periodicos


def read_conferencias():
    conferencias = list()
    with open(PATH + 'conferencias.tsv') as file:
        for row in file:
            cells = str(row).split('\t')
            new_conferencia = MyClasses.Conferencias(*cells[:32])
            new_conferencia.add_authors(*cells[32:-1])
            conferencias.append(new_conferencia)
    del conferencias[0]
    return conferencias


def read_qualis():
    with open('qualis-2017-2018.tsv') as file:
        qualis = [MyClasses.Quali(*str(row).split('\t')) for row in file]
    del qualis[0]
    return qualis


def read_docentes():
    registers = MyUtil.read_file('docentes.xlsx', path=PATH)
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


def get_publicacoes_qualis(publicacoes, qualis):
    publicacoes_qualis = defaultdict(lambda: new_quali_dict())
    issn_quali = {quali.issn: quali.estrato for quali in qualis}

    for publicacao in publicacoes:
        cod_programa = publicacao.codigo_ppg
        issn = publicacao.get_issn()
        quali_programa = issn_quali[issn] if issn in issn_quali.keys() else 'NA'  # caso nao haja issn
        publicacoes_qualis[cod_programa][quali_programa] += 1
        publicacoes_qualis[cod_programa]['total'] += 1

    return publicacoes_qualis


def get_publicacoes_docente(p_qualis, docentes_programa):
    ponderado = defaultdict(lambda: dict())
    for code in p_qualis.keys():
        for quali in TIPO_QUALIS:
            ponderado[code][quali] = p_qualis[code][quali] * PESO_QUALIS[quali]
            ponderado[code][quali] /= sum([valor for valor in docentes_programa[code].values()])
        ponderado[code]['total'] = sum([valor for valor in ponderado[code].values()])

    return ponderado


def get_publicacoes_permanente(p_qualis, docentes_programa):
    ponderado = defaultdict(lambda: dict())
    for code in p_qualis.keys():
        for quali in TIPO_QUALIS:
            ponderado[code][quali] = p_qualis[code][quali] * PESO_QUALIS[quali]
            ponderado[code][quali] /= docentes_programa[code]['PERMANENTE']
        ponderado[code]['total'] = sum([valor for valor in ponderado[code].values()])

    return ponderado


def get_code(code):
    new_code = code
    if code in programas_nivel.keys():
        new_code = programas_nivel[code]
    elif code in programas.keys():
        new_code = programas[code]
    return new_code


def sort_dict(dict_to_sort):
    return {get_code(value[0]): value[1] for value in sorted(dict_to_sort.items(), key=lambda item: item[1]['total'])}


def make_chart(chart_data, chart_title):
    data = list()
    for i in range(0, len(TIPO_QUALIS)):
        data.append(go.Bar(x=list(chart_data.keys()),
                           y=[p_quali[TIPO_QUALIS[i]] for p_quali in chart_data.values()],
                           marker_color=COLOR_QUALIS[TIPO_QUALIS[i]],
                           name=f'{TIPO_QUALIS[i]} ({PESO_QUALIS[TIPO_QUALIS[i]]})'))

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


# dados lidos
programas = MyUtil.read_programas(PATH)
programas_nivel = MyUtil.read_programas_nivel()
list_periodicos = read_periodicos()
list_conferencias = read_conferencias()
list_qualis = read_qualis()
list_docentes = read_docentes()

# dados processados
docente_programa = get_docentes_programas(list_docentes)

periodicos_qualis = get_publicacoes_qualis(list_periodicos, list_qualis)
periodicos_docente = sort_dict(get_publicacoes_docente(periodicos_qualis, docente_programa))
periodicos_permanente = sort_dict(get_publicacoes_permanente(periodicos_qualis, docente_programa))
periodicos_qualis = sort_dict(periodicos_qualis)  # ordena depois, pois a lista é utilizada em outro método

conferencias_qualis = get_publicacoes_qualis(list_conferencias, list_qualis)
conferencias_docente = sort_dict(get_publicacoes_docente(conferencias_qualis, docente_programa))
conferencias_permanente = sort_dict(get_publicacoes_permanente(conferencias_qualis, docente_programa))
conferencias_qualis = sort_dict(conferencias_qualis)  # ordena depois, pois a lista é utilizada em outro método

make_chart(periodicos_qualis, 'Periódicos por Qualis')
make_chart(periodicos_docente, 'Periódicos por Docentes (Permanentes + Colaboradores)')
make_chart(periodicos_permanente, 'Periódicos por Docentes Permanentes')

make_chart(conferencias_qualis, 'Conferências por Qualis')
make_chart(conferencias_docente, 'Conferências por Docentes (Permanentes + Colaboradores)')
make_chart(conferencias_permanente, 'Conferências por Docentes Permanentes')
