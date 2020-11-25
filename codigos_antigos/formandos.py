import plotly.offline as py
import plotly.graph_objs as go
import MyUtil
import MyClasses
from collections import defaultdict

PATH = 'dados_arquitetura_'
ANOS = ['2019']
COLORS = {'total': '#0000ff', 'publicacao': '#00FF00', 'periodico': '#FF0000', 'primeiro_autor': '#FFFF00'}
TITLES = {'total': '', 'publicacao': 'com Publicação', 'periodico': 'com Periódico',
          'primeiro_autor': 'com Periódico como Primeiro Autor'}


def read_trabalhos(filepath):
    registers = MyUtil.read_file('trabalhos_conclusao.xlsx', filepath)
    trabalhos = defaultdict(lambda: defaultdict(lambda: set()))

    for row in registers:
        # trabalhos[code][tipo].add(autor)
        trabalhos[row[3]][row[10]].add(row[9])

    return trabalhos


def read_producao(file_name):
    producoes = list()
    with open(file_name, encoding='Latin-1') as file:    # abre o .tsv
        for row in file:
            cells = str(row).split('\t')
            if 'periodicos' in file_name:
                producao = MyClasses.Periodico(*cells[:29]) 
                producao.add_authors(*cells[29:-1])
            else:
                producao = MyClasses.Conferencias(*cells[:32])
                producao.add_authors(*cells[32:-1])
            
            producoes.append(producao)
    del producoes[0]
    return producoes


def get_by_type(trabalhos, tipo_t):
    result = defaultdict(lambda: list())
    for code in trabalhos:
        if len(trabalhos[code][tipo_t]) > 0:
            result[code] = [autor for autor in trabalhos[code][tipo_t]]
    return result


def get_autores(producoes):
    authors = set()
    for producao in producoes:
        for author in producao.authors:
            authors.add(author['nome'])
    return authors


def get_primeiros_autores(producoes):
    return {producao.authors[0]['nome'] for producao in producoes if len(producao.authors) > 0}


def get_formandos_publicacao(formandos, *autores):
    formandos_publicacao = dict()
    for code in formandos.keys():
        formandos_publicacao[code] = len([formando for formando in formandos[code] if formando in autores])
    return formandos_publicacao


def get_formandos(trabalhos, tipo_t):
    # lista dos formandos
    formandos = get_by_type(trabalhos, 'TESE' if tipo_t == 'doutores' else 'DISSERTAÇÃO')     # {code: nomes}

    # calculos dos tipos de agrupamento de dados
    count_formandos = {code: len(formandos) for code, formandos in formandos.items()}
    formandos_publicacao = get_formandos_publicacao(formandos, *autores_conferencias, *autores_periodicos)
    formandos_periodico = get_formandos_publicacao(formandos, *autores_periodicos)
    formandos_periodico_primeiro = get_formandos_publicacao(formandos, *primeiros_autores_periodicos)

    # estruturas final
    tipos_formandos = defaultdict(lambda: {
        'total': 0,
        'publicacao': 0,
        'periodico': 0,
        'primeiro_autor': 0
    })

    for code in formandos.keys():
        new_code = code
        if code in programas_nivel.keys():
            new_code = programas_nivel[code]
        elif code in programas.keys():
            new_code = programas[code]

        tipos_formandos[new_code]['total'] += count_formandos[code]
        tipos_formandos[new_code]['publicacao'] += formandos_publicacao[code]
        tipos_formandos[new_code]['periodico'] += formandos_periodico[code]
        tipos_formandos[new_code]['primeiro_autor'] += formandos_periodico_primeiro[code]

    return tipos_formandos


def make_chart(chart_data, chart_title):
    data = list()
    aux_label = 'Doutor' if 'Doutores' in chart_title else 'Mestre'
    for dado in ('primeiro_autor', 'periodico', 'publicacao', 'total'):
        data.append(go.Bar(x=list(chart_data.keys()),
                           y=[d_f[dado] for d_f in chart_data.values()],
                           marker_color=COLORS[dado],
                           name=f'{aux_label} {TITLES[dado]}'))

    title = {
        'text': chart_title,
        'x': 0.5,
        'xanchor': 'center',
        'font': {
            'color': '#000000',
            'size': 20
        }
    }

    legend = {
        'font': {'color': '#000000'},
        'orientation': 'v',
        'x': 0,
        'y': 1
    }

    layout = go.Layout(title=title,
                       xaxis={'title': 'Instituição'},
                       legend=legend)

    fig = go.Figure(data=data, layout=layout)
    py.iplot(fig)


def sort_dict(dict_to_sort):
    return {value[0]: value[1] for value in sorted(dict_to_sort.items(), key=lambda item: item[1]['total'])}


list_trabalhos = dict()
periodicos = []
conferencias = []
programas = dict()

for ano in ANOS:             
    list_trabalhos_add = read_trabalhos(PATH + ano + '/')
    for programa in list_trabalhos_add:
        if programa in list_trabalhos:
            list_trabalhos_programa = list_trabalhos_add[programa]
            for tipo in list_trabalhos_programa:
                if tipo in list_trabalhos[programa]:
                    list_trabalhos[programa][tipo].update(list_trabalhos_programa[tipo])
                else:
                    list_trabalhos[programa][tipo] = list_trabalhos_programa[tipo]
        else:
            list_trabalhos[programa] = list_trabalhos_add[programa]
    programas.update(MyUtil.read_programas(PATH + ano + '/'))
    periodicos.extend(read_producao(PATH + ano + '/periodicos.tsv'))
    conferencias.extend(read_producao(PATH + ano + '/conferencias.tsv'))

programas_nivel = MyUtil.read_programas_nivel()

# autores das publicacoes
autores_conferencias = get_autores(conferencias)
autores_periodicos = get_autores(periodicos)

# apenas os primeiros autores
primeiros_autores_periodicos = get_primeiros_autores(periodicos)

# dados agrupados
doutores_formandos = sort_dict(get_formandos(list_trabalhos, 'doutores'))
mestres_formandos = sort_dict(get_formandos(list_trabalhos, 'mestres'))

make_chart(doutores_formandos, f'Doutores Formandos ({", ".join(ANOS)})')
make_chart(mestres_formandos, f'Mestres Formandos ({", ".join(ANOS)})')
