import MyUtil
from collections import defaultdict

PATH = '/home/joaomello/Documentos/USP/IC - Analise de Dados/Arquitetura/dados_arquitetura_2017/'
COLORS = {'total': '#0000ff', 'publicacao': '#00FF00', 'periodico': '#FF0000', 'primeiro_autor': '#FFFF00'}
TITLES = {'total': '', 'publicacao': 'com Publicação',
          'periodico': 'com Periódico', 'primeiro_autor': 'com Periódico como Primeiro Autor'}


def read_programas():
    registers = MyUtil.read_file('relatorio.xlsx')
    return {row[0]: f'{row[3]}-{row[6]}' for row in registers}


def read_trabalhos():
    registers = MyUtil.read_file('trabalhos_conclusao.xlsx', PATH)
    trabalhos = defaultdict(lambda: defaultdict(lambda: set()))

    for row in registers:
        trabalhos[row[3]][row[10]].add(row[9])

    return trabalhos


def read_producao(file_name):
    producoes = list()
    with open(PATH + file_name) as file:
        for row in file:
            cells = str(row).split('\t')
            producao = MyUtil.Periodico(*cells[:32]) if 'periodicos' in file_name \
                else MyUtil.Conferencias(*cells[:32])
            producao.add_authors(*cells[32:-1])
            producoes.append(producao)
    del producoes[0]
    return producoes


def get_by_type(trabalhos, tipo):
    result = defaultdict(lambda: list())
    for code in trabalhos:
        if len(trabalhos[code][tipo]) > 0:
            result[code] = [trabalho for trabalho in trabalhos[code][tipo]]
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


def get_formandos(trabalhos, tipo):
    # lista dos formandos
    formandos = get_by_type(trabalhos, 'TESE' if tipo == 'doutores' else 'DISSERTAÇÃO')     # {code: nomes}

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
        tipos_formandos[programas[code]]['total'] += count_formandos[code]
        tipos_formandos[programas[code]]['publicacao'] += formandos_publicacao[code]
        tipos_formandos[programas[code]]['periodico'] += formandos_periodico[code]
        tipos_formandos[programas[code]]['primeiro_autor'] += formandos_periodico_primeiro[code]

    return tipos_formandos


def sort_data(to_sort):
    sorted_data = list()
    for code in to_sort:
        sorted_data.append({key: value for key, value in to_sort[code].items()})
        sorted_data[-1]['code'] = code

    for i in range(1, len(sorted_data)):
        j = i
        new_value = sorted_data[i]

        while j > 0 and sorted_data[j - 1]['total'] > new_value['total']:
            sorted_data[j] = sorted_data[j - 1]
            j -= 1

        sorted_data[j] = new_value

    return sorted_data


# porgrmas
programas = read_programas()

# trabalhos de conclusao
list_trabalhos = read_trabalhos()

# publicacoes
conferencias = read_producao('conferencias.tsv')
periodicos = read_producao('periodicos.tsv')

# autores das publicacoes
autores_conferencias = get_autores(conferencias)
autores_periodicos = get_autores(periodicos)

# apenas os primeiros autores
primeiros_autores_periodicos = get_primeiros_autores(periodicos)

# dados agrupados
doutores_formandos = sort_data(get_formandos(list_trabalhos, 'doutores'))
mestres_formandos = sort_data(get_formandos(list_trabalhos, 'mestres'))
