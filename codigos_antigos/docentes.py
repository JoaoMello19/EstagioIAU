# para o processamento dos dados
import MyUtil
from collections import defaultdict

FILE_NAME = 'docentes.xlsx'
PATH = 'dados_arquitetura_'
ANOS = ['2017']


def get_docentes(filepath):
    """
    Função que recupera e processa os dados de interesse
    :return: um dicionario, com os dados de interesse
    """
    registers = MyUtil.read_file(FILE_NAME, filepath)

    docentes = defaultdict(lambda: list())
    for row in registers:
        docente = {
            'name': row[8],
            'category': row[12]
        }
        
        if docente not in docentes[row[3]]:
            docentes[row[3]].append(docente)
        

    return docentes

#método antigo de calcular a media
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
##

#método alternativo para calcular a média considerando mais de dois anos
def get_docentes_programa_alt(p_code):
    docentes_programa = {'PERMANENTE': 0, 'COLABORADOR': 0, 'total': 0}
    for docente in p_code: 
        if docente['category'] in ['PERMANENTE', 'COLABORADOR']:
            docentes_programa[docente['category']] += 1
        
    docentes_programa['total'] = docentes_programa['PERMANENTE'] + docentes_programa['COLABORADOR']

    return docentes_programa

def get_media_docentes_programas(docentes):

    codes = {code for code in docentes.keys()}
    doc_prog = defaultdict(lambda: {
        'PERMANENTE': 0,
        'COLABORADOR': 0,
        'total': 0
    })

    for code in codes:
        d_programa = get_docentes_programa_alt(docentes[code])

        new_code = code
        if code in programas_nivel.keys():
            new_code = programas_nivel[code]
        elif code in programas.keys():
            new_code = programas[code]

        doc_prog[new_code]['PERMANENTE'] = d_programa['PERMANENTE']/len(ANOS)
        doc_prog[new_code]['COLABORADOR'] = d_programa['COLABORADOR']/len(ANOS)
        doc_prog[new_code]['total'] = d_programa['PERMANENTE'] + d_programa['COLABORADOR']

    return doc_prog
###

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
                        text=['<b>'+'{0:.2f}'.format(f_d['PERMANENTE'])+'</b>' for f_d in chart_data.values()],
                        textposition='inside',
                        name='PERMANENTE',
                        marker={'color': '#FF0000'})

    trace_colab = go.Bar(x=list(chart_data.keys()),
                         y=[f_d['COLABORADOR'] for f_d in chart_data.values()],
                         text=['<b>'+'{0:.2f}'.format(f_d['COLABORADOR'])+'</b>' for f_d in chart_data.values()],
                         textposition='outside',
                         name='COLABORADOR',
                         marker={'color': '#0000FF'})

    data = [trace_perm, trace_colab]

    title = {
        'text': f'Médias de Docentes Permanentes e Colaboradores ({", ".join(ANOS)})',
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
                       legend=subtitle,
                       height=1000,
                       width=2300)
    fig = go.Figure(data=data, layout=layout)
    py.iplot(fig)


def sort_dict(dict_to_sort):
    sorted_dict = {value[0]: value[1] for value in sorted(dict_to_sort.items(), key=lambda item: item[1]['PERMANENTE'])}
    return {value[0]: value[1] for value in sorted(sorted_dict.items(), key=lambda item: item[1]['total'])}


all_registers = dict()
list_docentes = dict()
programas = dict()

# all_registers.update(MyUtil.read_file(FILE_NAME, PATH+ano+'/'))
for ano in ANOS: 
    list_docentes_add = get_docentes(PATH+ano+'/')
    for programa in list_docentes_add:
        if programa in list_docentes:
            list_docentes[programa].extend(list_docentes_add[programa])
        else:
            list_docentes[programa] = list_docentes_add[programa]
    programas.update(MyUtil.read_programas(PATH+ano+'/'))

programas_nivel = MyUtil.read_programas_nivel()
#antigo
#docentes_programas = sort_dict(get_docentes_programas(list_docentes))
#novo
docentes_programas = sort_dict(get_media_docentes_programas(list_docentes))

make_chart(docentes_programas)
