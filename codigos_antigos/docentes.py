# para o processamento dos dados
import MyUtil
from collections import defaultdict

FILE_NAME = 'docentes.xlsx'
PATH = '/home/joaomello/Documentos/USP/IC - Analise de Dados/Arquitetura/dados_arquitetura_2017/'


def get_docentes():
    """
    Função que recupera e processa os dados de interesse
    :return: um dicionario, com os dados de interesse
    """
    registers = MyUtil.read_file(FILE_NAME, PATH)

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
    for category in names_categories.values():  # ignora os nomes, apenas considera as categorias
        if category in ('PERMANENTE', 'COLABORADOR'):
            docentes_programa[category] += 1
        else:  # ambas as categorias
            docentes_programa['PERMANENTE'] += 0.5
            docentes_programa['COLABORADOR'] += 0.5

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

        new_code = code
        if code in programas_nivel.keys():
            new_code = programas_nivel[code]
        elif code in programas.keys():
            new_code = programas[code]

        doc_prog[new_code]['PERMANENTE'] += d_programa['PERMANENTE']
        doc_prog[new_code]['COLABORADOR'] += d_programa['COLABORADOR']
        doc_prog[new_code]['total'] += d_programa['PERMANENTE'] + d_programa['COLABORADOR']

    return doc_prog


def make_chart(chart_data):
    """
    Monta o gráfico com base nos dados
    :param chart_data: dadaos para a elaboraçõa do gráfico
    :return: none
    """
    import plotly.offline as py
    import plotly.graph_objs as go

    trace_perm = go.Bar(x=list(chart_data.keys()),
                        y=[f_d['PERMANENTE'] for f_d in chart_data.values()],
                        name='PERMANENTE',
                        marker={'color': '#FF0000'})

    trace_colab = go.Bar(x=list(chart_data.keys()),
                         y=[f_d['COLABORADOR'] for f_d in chart_data.values()],
                         name='COLABORADOR',
                         marker={'color': '#0000FF'})

    data = [trace_perm, trace_colab]

    title = {
        'text': 'Médias de Docentes Permanentes e Colaboradores',
        'x': 0.5,
        'xanchor': 'center',
        'font': {
            'color': '#000000',
            'size': 20
        }
    }

    subtitle = {
        'font': {'color': '#000000'},
        'orientation': 'h',
        'x': 0,
        'y': 1
    }

    layout = go.Layout(title=title,
                       xaxis={'title': 'Instituição'},
                       barmode='stack',
                       legend=subtitle)
    fig = go.Figure(data=data, layout=layout)
    py.iplot(fig)


def sort_dict(dict_to_sort):
    sorted_dict = {value[0]: value[1] for value in sorted(dict_to_sort.items(), key=lambda item: item[1]['PERMANENTE'])}
    return {value[0]: value[1] for value in sorted(sorted_dict.items(), key=lambda item: item[1]['total'])}


all_registers = MyUtil.read_file(FILE_NAME, PATH)
list_docentes = get_docentes()

programas_nivel = MyUtil.read_programas_nivel()
programas = MyUtil.read_programas(PATH)

docentes_programas = sort_dict(get_docentes_programas(list_docentes))
make_chart(docentes_programas)
