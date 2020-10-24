import MyUtil
from collections import defaultdict, OrderedDict

FILE_NAME = 'docentes.xlsx'
PATH = '/home/joaomello/Documentos/USP/IC - Analise de Dados/Arquitetura/dados_arquitetura_2017/'


def read_trabalhos():
    registers = MyUtil.read_file('trabalhos_conclusao.xlsx', PATH)
    trabalhos = defaultdict(lambda: defaultdict(lambda: set()))

    for row in registers:
        # [code][tipo] = titulos
        trabalhos[row[3]][row[10]].add(row[9])

    return trabalhos


def get_formandos_by(trabalhos, t_formandos):
    result = defaultdict(lambda: list())
    for code in trabalhos:
        if len(trabalhos[code][t_formandos]) > 0:
            result[code] = [trabalho for trabalho in trabalhos[code][t_formandos]]
    return result


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


def get_docentes_by(d_programas, categoria):
    if categoria in ('PERMANENTE', 'COLABORADOR'):
        return {code: d_programas[code][categoria] for code in d_programas.keys()}
    else:
        return {code: d_programas[code]['total'] for code in d_programas.keys()}


def read_programas():
    registers = MyUtil.read_file('programas.xlsx', path=PATH)
    return {row[3]: row[8] for row in registers}


def read_programas_nivel():
    registers = MyUtil.read_file('relatorio.xlsx')
    return {row[0]: f'{row[3]}-{row[6]}' for row in registers}


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


def sort_data(to_sort):
    codes = list(to_sort.keys())

    for i in range(1, len(codes)):
        j = i
        new_code = codes[i]
        while j > 0 and to_sort[codes[j - 1]] > to_sort[new_code]:
            codes[j] = codes[j - 1]
            j -= 1
        codes[j] = new_code

    sorted_data = OrderedDict()
    for code in codes:
        sorted_data[code] = to_sort[code]
    return sorted_data


list_trabalhos = read_trabalhos()
list_docentes = get_docentes()
docentes_programas = get_docentes_programas(list_docentes)

programas = read_programas()
programas_nivel = read_programas_nivel()

doutores_docente = sort_data(get_formandos_docentes(list_trabalhos, 'TESE', docentes_programas))
doutores_permanente = sort_data(get_formandos_docentes(list_trabalhos, 'TESE', docentes_programas, 'PERMANENTE'))
mestres_docente = sort_data(get_formandos_docentes(list_trabalhos, 'DISSERTAÇÃO', docentes_programas))
mestres_permanente = sort_data(get_formandos_docentes(list_trabalhos, 'DISSERTAÇÃO', docentes_programas, 'PERMANENTE'))
