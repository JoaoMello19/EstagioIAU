import MyUtil
import MyClasses


def join_same_productions(registers):
    all_prod = list()  # armazena as producoes completas
    same_prod = list()  # armazena os registros relativos ao mesmo
    for register in registers:
        if len(same_prod) > 0:
            if register[9:16] == same_prod[0][9:16]:
                same_prod.append(register)
            else:
                all_prod.append(same_prod[:])
                same_prod.clear()
        else:
            same_prod.append(register)

    return all_prod


def convert_to_object(to_convert):
    obj_productions = list()
    for production in to_convert:
        new_prod = MyClasses.Producao(*production[0][:16])

        for prod in production:
            if prod[16] != '':  # detalhamento
                new_prod.add_detalhamento(prod[16], prod[17])
            elif prod[18] != '':
                new_prod.add_autor(prod[18], prod[19], prod[20])

        obj_productions.append(new_prod)

    return obj_productions


def get_productions(productions):
    conf = list()
    peri = list()
    for obj in productions:
        if obj.subtipo_producao == 'TRABALHO EM ANAIS':
            conf.append(obj)
        elif obj.subtipo_producao == 'ARTIGO EM PERIÓDICO':
            peri.append(obj)

    return conf, peri


def get_detalhamentos(productions):
    details = set()  # lista de todos os detalhamentos
    for c in productions:
        for d in c.detalhamentos.keys():
            details.add(d)
    return details


def get_authors(production):
    authors = list()
    for author in production.autores:
        authors.append({
            'name': author,
            'category': production.autores[author]['categoria']
        })
    return authors


def write_arq(file_name, titles, details, productions):
    result_file = open(file_name, 'w')  # arquivo para a saída de dados

    for t in titles:  # primeira linha com os títulos gerais
        result_file.write(f'{t}\t')

    for t in details:  # continuação -> titulos dos detalhamentos
        result_file.write(f'{t}\t')

    MAX_AUTHORS = 15 if 'conferencias' in file_name else 46
    for i in range(MAX_AUTHORS):
        result_file.write(f'Autor {i + 1}\tCategoria Autor {i + 1}\t')
    result_file.write('\n')  # quabra de linha

    for prod in productions:  # todas as conferencias
        for attrib in prod.get_attributes():    # dadsos comuns
            result_file.write(f'{attrib}\t')

        for attrib in details:                  # detalhamentos
            result_file.write(f'{prod.detalhamentos[attrib]}\t')

        authors = get_authors(prod)
        for author in authors:
            result_file.write(f"{author['name']}\t{author['category']}\t")

        result_file.write('\n')

    result_file.close()


# inicio do programa principal
FILE_NAME = 'producoes_intelectuais.xlsx'
SHEET_NAME = 'Produção Intelectual'
PATH = 'dados_arquitetura_2017/'

all_registers = MyUtil.open_large_xls(FILE_NAME, SHEET_NAME, PATH)      # abrindo o arquivo

original_titles = [MyUtil.convert_ascii(t) for t in all_registers[0][:16]]       # comprehension
del all_registers[0]    # remove os titulos dos registros

text_productions = join_same_productions(all_registers)     # une os registros da mesma produção (arrays)
list_productions = convert_to_object(text_productions)      # lista com as produções formatadas (objetos)

# processo de separação das conferências e periódicos
conferencias, periodicos = get_productions(list_productions)
list_productions.clear()    # libera a lista com todos os registros

det_conf = sorted(get_detalhamentos(conferencias))  # detalhamentos das conferencias
write_arq(PATH + 'conferencias.tsv', original_titles, det_conf, conferencias)  # escreve as conferencias

det_peri = sorted(get_detalhamentos(periodicos))
write_arq(PATH + 'periodicos.tsv', original_titles, det_peri, periodicos)
