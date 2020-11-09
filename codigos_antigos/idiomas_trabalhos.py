import MyUtil
from collections import defaultdict

PATH = '/home/joaomello/Documentos/USP/IC - Analise de Dados/Arquitetura/dados_arquitetura_2017/'


def read_programas():
    registers = MyUtil.read_file('relatorio.xlsx')
    programas = {row[0]: f'{row[3]}-{row[6]}' for row in registers}
    return programas


def group_trabalhos():
    registers = MyUtil.read_file('trabalhos_conclusao.xlsx', PATH)
    grouped = list()
    same_tcc = list()
    for row in registers:
        if len(same_tcc) > 0:
            if row[8:12] == same_tcc[0][8:12]:  # trabalhos iguais
                same_tcc.append(row)
            else:                               # trabalhos diferentes
                grouped.append(same_tcc[:])
                same_tcc.clear()
        else:
            same_tcc.append(row)
    
    return grouped


def convert_to_object(to_convert):
    trabalho = MyUtil.TrabalhoConclusao(*to_convert[0][:13])
    # print(trabalho.nome_trabalho_conclusao)
    for row in to_convert:
        # print(f'{row} : {len(row)}')
        if row[13] != '':  # nome do orientador
            trabalho.nome_orientador = row[13]
            trabalho.principal = row[14]
        elif row[15] != '':    # nome banca
            trabalho.membros_banca.append({
                'nome': row[15],
                'categoria': row[16]
            })
        else:
            trabalho.tipo_documento, trabalho.numero_documento, trabalho.nome_financiador, \
                trabalho.quantidade_meses = row[17:]
    return trabalho


def get_trabalhos_idiomas(trabalhos):
    trabalhos_idiomas = defaultdict(lambda: {

    })


list_programas = read_programas()
list_tcc = group_trabalhos()
list_trabalhos = [convert_to_object(trabalho) for trabalho in list_tcc]
