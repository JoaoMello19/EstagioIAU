import plotly.offline as py
import plotly.graph_objs as go

import MyUtil, MyClasses
from collections import defaultdict

ANOS = ['2013']
PATH = 'dados_arquitetura_'


def read_periodicos(filepath):
    # leitura dos periodicos
    periodicos = list()
    with open(filepath + 'periodicos.tsv', encoding='Latin-1') as file:
        for row in file:
            cells = str(row).split('\t')
            new_periodico = MyClasses.Periodico(*cells[:29])
            new_periodico.add_authors(*cells[29:-1])
            periodicos.append(new_periodico)
    del periodicos[0]
    return periodicos


def read_conferencias(filepath):
    conferencias = list()
    with open(filepath + 'conferencias.tsv', encoding='Latin-1') as file:
        for row in file:
            cells = str(row).split('\t')
            new_conferencia = MyClasses.Conferencias(*cells[:32])
            new_conferencia.add_authors(*cells[32:-1])
            conferencias.append(new_conferencia)
    del conferencias[0]
    return conferencias

def get_autores(producoes):
    authors = set()
    for producao in producoes:
        for author in producao.authors:
            if "Discente" in author['categoria']:
                print(author)
            authors.add(author['nome'])
    return authors

def get_by_type(trabalhos, tipo):
    result = defaultdict(lambda: list())
    for code in trabalhos:
        if len(trabalhos[code][tipo]) > 0:
            result[code] = [autor for autor in trabalhos[code][tipo]]
    return result

def read_trabalhos(filepath):
    registers = MyUtil.read_file('trabalhos_conclusao.xlsx', filepath)
    trabalhos = defaultdict(lambda: defaultdict(lambda: set()))

    for row in registers:
        # trabalhos[code][tipo].add(autor)
        trabalhos[row[3]][row[10]].add(row[9])

    return trabalhos

def get_publicacoes_discente(producoes, trabalhos, tipo):
    qtd_formandos = get_qtd_formandos(trabalhos, tipo)
    qtd_publicacoes_discentes = get_qtd_publicacoes_discente(producoes, tipo)
    #print("qtd de formandos por programa")
    #print(qtd_formandos)
    #print("qtd de publicacoes por discente")
    #print(qtd_publicacoes_discentes)
    
    result = defaultdict()
    for code in qtd_publicacoes_discentes.keys():
        if code in qtd_formandos.keys():
            result[code] = qtd_publicacoes_discentes[code]/qtd_formandos[code]
        
    return result
    

def get_qtd_formandos(trabalhos, tipo):
    # lista dos formandos
    formandos = get_by_type(trabalhos, 'TESE' if tipo == 'doutores' else 'DISSERTAÇÃO')     # {code: nomes}

    # calculos dos tipos de agrupamento de dados
    count_formandos = {code: len(formandos) for code, formandos in formandos.items()}
    result = defaultdict()
    for code in formandos.keys():
        new_code = code
        if code in programas_nivel.keys():
            new_code = programas_nivel[code]
        elif code in programas.keys():
            new_code = programas[code]

        result[new_code] = count_formandos[code]

    return result

def get_qtd_publicacoes_discente(producoes, tipo):
    # lista dos formandos
    publicacoes_discentes = defaultdict()
    for producao in producoes:
        for author in producao.authors:
            if "Discente" in author['categoria']:
                if (tipo=='mestres' and 'Mestrado' in author['categoria']) or (tipo=='doutores' and 'Doutorado' in author['categoria']):
                    if producao.codigo_ppg in publicacoes_discentes.keys(): 
                        publicacoes_discentes[producao.codigo_ppg] += 1
                    else:
                        publicacoes_discentes[producao.codigo_ppg] = 1
                        
    result = defaultdict()                   
    for code in publicacoes_discentes.keys():
        new_code = code
        if code in programas_nivel.keys():
            new_code = programas_nivel[code]
        elif code in programas.keys():
            new_code = programas[code]

        result[new_code] = publicacoes_discentes[code]

    return result


def get_code(code):
    new_code = code
    if code in programas_nivel.keys():
        new_code = programas_nivel[code]
    elif code in programas.keys():
        new_code = programas[code]
    return new_code


def sort_dict(dict_to_sort):
    return dict(sorted(dict_to_sort.items(), key=lambda item: item[1]))


def make_chart(chart_data, chart_title):
    data = [go.Bar(x=[code for code in chart_data.keys()],
                   y=[value for value in chart_data.values()],
                   text=['{0:.2f}'.format(value) for value in chart_data.values()],
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
                       xaxis={'title': 'Instituição'},
                       barmode='stack')
    fig = go.Figure(data=data, layout=layout)
    py.iplot(fig)

list_periodicos=[]
list_conferencias=[]
list_trabalhos=dict()
programas=dict()

# dados lidos
for ano in ANOS:
    programas.update(MyUtil.read_programas(PATH+ano+'/'))
    list_periodicos.extend(read_periodicos(PATH+ano+'/'))
    list_conferencias.extend(read_conferencias(PATH+ano+'/'))
    list_trabalhos_add = read_trabalhos(PATH+ano+'/')
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

programas_nivel = MyUtil.read_programas_nivel()
publicacoes_discente_mestrado = sort_dict(get_publicacoes_discente(list_periodicos, list_trabalhos, "mestres"))
publicacoes_discente_doutorado = sort_dict(get_publicacoes_discente(list_periodicos, list_trabalhos, "doutores"))


make_chart(publicacoes_discente_mestrado, 'Periódicos por formandos mestrado - '+','.join(ANOS))
make_chart(publicacoes_discente_doutorado, 'Periódicos por formandos doutorado - '+','.join(ANOS))