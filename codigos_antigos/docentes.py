import MyUtil
from collections import defaultdict

FILE_NAME = 'docentes.xlsx'
PATH = '/home/joaomello/Documentos/USP/IC - Analise de Dados/Arquitetura/dados_arquitetura_2017/'


def read_programas():
    registers = MyUtil.read_file('programas.xlsx', path=PATH)
    return {row[3]: row[8] for row in registers}


def read_programas_nivel():
    registers = MyUtil.read_file('relatorio.xlsx')
    return {row[0]: f'{row[3]}-{row[6]}' for row in registers}


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
    for category in names_categories.values():
        if category in ('PERMANENTE', 'COLABORADOR'):
            docentes_programa[category] += 1
        else:  # ambas as categorias
            docentes_programa['PERMANENTE'] += 0.5
            docentes_programa['COLABORADOR'] += 0.5
        docentes_programa['total'] += 0

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


def sort_data(to_sort):
    """
    Função que ordena dados com base em um campo
    :param to_sort: o dicionário a der ordenado
    :return: o dicionŕaio ordenado
    """
    codes = list(to_sort.keys())

    for i in range(1, len(codes)):
        j = i
        new_code = codes[i]
        while j > 0 and (to_sort[codes[j - 1]]['total'] > to_sort[new_code]['total'] or
                         (to_sort[codes[j - 1]]['total'] == to_sort[new_code]['total'] and
                          to_sort[codes[j - 1]]['PERMANENTE'] > to_sort[new_code]['PERMANENTE'])):
            codes[j] = codes[j - 1]
            j -= 1
        codes[j] = new_code

    sorted_data = [{key: value for key, value in to_sort[code].items()} for code in codes]
    for i in range(len(sorted_data)):
        sorted_data[i]['code'] = codes[i]

    return sorted_data


all_registers = MyUtil.read_file(FILE_NAME, PATH)
list_docentes = get_docentes()

programas_nivel = read_programas_nivel()
programas = read_programas()

docentes_programas = get_docentes_programas(list_docentes)
final_data = sort_data(docentes_programas)
