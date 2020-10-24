import MyUtil
from collections import defaultdict

PATH = '/home/joaomello/Documentos/USP/IC - Analise de Dados/Arquitetura/dados_arquitetura_2017/'
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
            new_periodico = MyUtil.Periodico(*cells[:32])
            new_periodico.add_authors(*cells[32:-1])
            periodicos.append(new_periodico)
    del periodicos[0]
    return periodicos


def read_conferencias():
    conferencias = list()
    with open(PATH + 'conferencias.tsv') as file:
        for row in file:
            cells = str(row).split('\t')
            new_conferencia = MyUtil.Conferencias(*cells[:32])
            new_conferencia.add_authors(*cells[32:-1])
            conferencias.append(new_conferencia)
    del conferencias[0]
    return conferencias


def read_qualis():
    with open('qualis-2017-2018.tsv') as file:
        qualis = [MyUtil.Quali(*str(row).split('\t')) for row in file]
    del qualis[0]
    return qualis


def read_programas():
    registers = MyUtil.read_file('relatorio.xlsx')
    programas = {row[0]: f'{row[3]}-{row[6]}' for row in registers}
    return programas


def read_docentes():
    registers = MyUtil.read_file('docentes.xlsx', path=PATH)
    docentes = defaultdict(lambda: list())

    for row in registers:
        docentes[row[3]].append({
            'name': row[8],
            'category': row[12]
        })

    return docentes


def get_average(docentes):
    names_categories = dict()

    for docente in docentes:
        if docente['name'] not in names_categories.keys():  # primeira vez que o docente é registrado
            names_categories[docente['name']] = docente['category']

        elif names_categories[docente['name']] not in ('BOTH', docente['category']):
            # registrado como outra categoria -> pertence a ambas
            names_categories[docente['name']] = 'BOTH'

    average = {'PERMANENTE': 0, 'COLABORADOR': 0}
    for category in names_categories.values():
        if category in ('PERMANENTE', 'COLABORADOR'):
            average[category] += 1
        else:  # ambas as categorias
            average['PERMANENTE'] += 0.5
            average['COLABORADOR'] += 0.5

    return average


def get_all_averages(all_docentes):
    averages = dict()

    for code in all_docentes.keys():
        average = get_average(all_docentes[code])
        averages[code] = {
            'PERMANENTE': average['PERMANENTE'],
            'COLABORADOR': average['COLABORADOR'],
            'total': average['PERMANENTE'] + average['COLABORADOR']
        }

    return averages


def get_publicacoes_qualis(publicacoes, qualis):
    publicacoes_qualis = defaultdict(lambda: new_quali_dict())
    dict_qualis = {quali.issn: quali.estrato for quali in qualis}

    for publicacao in publicacoes:
        cod_programa = publicacao.codigo_ppg
        issn = publicacao.get_issn()
        quali_programa = dict_qualis[issn] if issn in dict_qualis.keys() else 'NA'  # caso nao haja issn
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


def sort_data(to_sort, programas):
    grouped = defaultdict(lambda: new_quali_dict())
    for code in to_sort.keys():
        if code in programas.keys():
            sigla = programas[code]
            for quali in TIPO_QUALIS:
                grouped[sigla][quali] += to_sort[code][quali]
            grouped[sigla]['total'] += to_sort[code]['total']

    sorted_data = list()

    for key in grouped.keys():  # converte o dicionario em lista de dicionarios
        sorted_data.append({k: v for k, v in grouped[key].items()})
        sorted_data[-1]['code'] = key

    for i in range(len(sorted_data)):
        j = i
        new_value = sorted_data[i]

        while j > 0 and sorted_data[j - 1]['total'] > new_value['total']:
            sorted_data[j] = sorted_data[j - 1]
            j -= 1

        sorted_data[j] = new_value

    return sorted_data


# dados lidos
list_programas = read_programas()
list_periodicos = read_periodicos()
list_conferencias = read_conferencias()
list_qualis = read_qualis()
list_docentes = read_docentes()

# dados processados
docente_programa = get_all_averages(list_docentes)

periodicos_qualis = get_publicacoes_qualis(list_periodicos, list_qualis)
periodicos_docente = get_publicacoes_docente(periodicos_qualis, docente_programa)
periodicos_permanente = get_publicacoes_permanente(periodicos_qualis, docente_programa)

conferencias_qualis = get_publicacoes_qualis(list_conferencias, list_qualis)
conferencias_docente = get_publicacoes_docente(conferencias_qualis, docente_programa)
conferencias_permanente = get_publicacoes_permanente(conferencias_qualis, docente_programa)
