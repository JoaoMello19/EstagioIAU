import csv
import zipfile
from bs4 import BeautifulSoup
from collections import defaultdict, OrderedDict
from openpyxl import load_workbook


class Producao:
    def __init__(self, *args):
        self.calendario, self.ano_calendario, self.data_hora_envio, self.codigo_ppg, self.nome_ppg, \
            self.area_avaliacao, self.sigla_ies, self.nome_ies, self.ano_producao, self.titulo_producao, \
            self.producao_glosada, self.tipo_producao, self.subtipo_producao, self.area_concentracao, \
            self.linha_pesquisa, self.projeto_pesquisa = args

        self.calendario = convert_ascii(self.calendario)
        self.nome_ppg = convert_ascii(self.nome_ppg)
        self.area_avaliacao = convert_ascii(self.area_avaliacao)
        self.nome_ies = convert_ascii(self.nome_ies)
        self.titulo_producao = convert_ascii(self.titulo_producao)
        self.producao_glosada = convert_ascii(self.producao_glosada)
        self.tipo_producao = convert_ascii(self.tipo_producao)
        self.subtipo_producao = convert_ascii(self.subtipo_producao)
        self.area_concentracao = convert_ascii(self.area_concentracao)
        self.linha_pesquisa = convert_ascii(self.linha_pesquisa)
        self.projeto_pesquisa = convert_ascii(self.projeto_pesquisa)

        self.detalhamentos = defaultdict(lambda: '')  # nome_detalhamento: detalhamento
        self.autores = OrderedDict()  # nome_autor: ordem_autor (mantem a ordem)

    def add_detalhamento(self, nome, valor):
        self.detalhamentos[convert_ascii(nome)] = convert_ascii(valor)

    def add_autor(self, nome, categoria, ordem):
        self.autores[convert_ascii(nome)] = {
            'categoria': convert_ascii(categoria),
            'ordem': int(ordem)
        }

    def get_attributes(self):
        return self.calendario, self.ano_calendario, self.data_hora_envio, self.codigo_ppg, self.nome_ppg, \
               self.area_avaliacao, self.sigla_ies, self.nome_ies, self.ano_producao, self.titulo_producao, \
               self.producao_glosada, self.tipo_producao, self.subtipo_producao, self.area_concentracao, \
               self.linha_pesquisa, self.projeto_pesquisa

    def to_string(self):
        return f'''calendario = {self.calendario} 
ano_calendario = {self.ano_calendario} 
data_hora_envio = {self.data_hora_envio} 
codigo_ppg = {self.codigo_ppg} 
nome_ppg = {self.nome_ppg} 
area_avaliacao = {self.area_avaliacao} 
sigla_ies = {self.sigla_ies} 
nome_ies = {self.nome_ies} 
ano_producao = {self.ano_producao} 
titulo_producao = {self.titulo_producao} 
producao_glosada = {self.producao_glosada} 
tipo_producao = {self.tipo_producao} 
subtipo_producao = {self.subtipo_producao} 
area_concentracao = {self.area_concentracao} 
linha_pesquisa = {self.linha_pesquisa} 
projeto_pesquisa = {self.projeto_pesquisa}
detalhamentos = {self.detalhamentos}
autores = {self.autores}\n'''


class Periodico:
    def __init__(self, *args):
        self.calendario, self.ano_calendario, self.data_hora_envio, self.codigo_ppg, self.nome_ppg, \
            self.area_avaliacao, self.sigla_ies, self.nome_ies, self.ano_producao, self.titulo_producao, \
            self.producao_glosada, self.tipo_producao, self.subtipo_producao, self.area_concentracao, \
            self.linha_pesquisa, self.projeto_pesquisa, self.cidade, self.doi, self.divulgacao, self.fasciculo, \
            self.issn_titulo_periodico, self.idioma, self.natureza, self.nome_editora, self.numero_pagina_final, \
            self.numero_pagina_incial, self.numero_doi, self.observacao, self.serie, self.url, self.url_doi, \
            self.volume = args
        self.authors = list()

    def add_authors(self, *authors):
        self.authors = [{'nome': authors[i], 'categoria': authors[i + 1]} for i in range(0, len(authors), 2)]

    def get_issn(self):
        return str(self.issn_titulo_periodico).split(' ')[0]


class Conferencias:
    def __init__(self, *args):
        self.calendario, self.ano_calendario, self.data_hora_envio, self.codigo_ppg, self.nome_ppg, \
            self.area_avaliacao, self.sigla_ies, self.nome_ies, self.ano_producao, self.titulo_producao, \
            self.producao_glosada, self.tipo_producao, self.subtipo_producao, self.area_concentracao, \
            self.linha_pesquisa, self.projeto_pesquisa, self.cidade_evento, self.divulgacao, self.edicao_numero, \
            self.fasciculo, self.isbn_issn, self.idioma, self.natureza, self.nome_evento, self.numero_pagina_final, \
            self.numero_pagina_inicial, self.observacao, self.pais, self.serie, self.titulo_anais, self.url, \
            self.volume, = args
        self.authors = list()

    def add_authors(self, *authors):
        self.authors = [{'nome': authors[i], 'categoria': authors[i + 1]} for i in range(0, len(authors), 2)]

    def get_issn(self):
        return self.isbn_issn if len(self.isbn_issn) == 5 else ''


class Quali:
    def __init__(self, *args):
        self.issn, self.titulo, self.estrato = [str(arg)[1:-1] for arg in args]
        self.estrato = self.estrato[:-1]


class TrabalhoConclusao():
    def __init__(self, *args):
        self.calendario, self.ano_calendario, self.data_hora_envio, self.codigo_ppg, self.nome_ppg, \
            self.area_avaliacao, self.sigla_ies, self.nome_ies, self.nome_trabalho_conclusao, self.nome_autor, \
            self.tipo_trabalho_conclusao, self.data_defesa, self.orientador_principal_banca = args

        self.membros_banca = list()


def format_row(row):
    f_row = list()
    for cell in row:
        if '</t>' in cell:
            f_row.append(cell[cell.find('>') + 1:cell.find('</t>')])
    return f_row


def open_large_xls(file_name, my_sheet, path=''):
    paths = []
    filename = path + file_name
    file = zipfile.ZipFile(filename, "r")

    for name in file.namelist():
        if name == 'xl/workbook.xml':
            data = BeautifulSoup(file.read(name), 'html.parser')
            sheets = data.find_all('sheet')
            for sheet in sheets:
                paths.append([sheet.get('name'), 'xl/worksheets/sheet' + str(sheet.get('sheetid')) + '.xml'])

    all_rows = list()

    for path in paths:
        if path[0] == my_sheet:
            with file.open(path[1]) as reader:
                for row in reader:
                    f_row = format_row(str(row).split('<t'))
                    if len(f_row) > 0:
                        '''if len(f_row) != 21:
                            print(f'{len(f_row)} : {row}')'''
                        all_rows.append(f_row)
            reader.close()

    return all_rows


def convert_ascii(string):
    regex = {'°': '&#176;', 'º': '&#186;', 'À': '&#192;', 'Á': '&#193;', 'Â': '&#194;', 'Ã': '&#195;', 'Ç': '&#199;',
             'É': '&#201;', 'Ê': '&#202;', 'Í': '&#205;', 'Ó': '&#211;', 'Ô': '&#212;', 'Õ': '&#213;', 'Ú': '&#218;',
             'à': '&#224;', 'á': '&#225;', 'â': '&#226;', 'ã': '&#227;', 'ç': '&#231;', 'é': '&#233;', 'ê': '&#234;',
             'í': '&#237;', 'ó': '&#243;', 'ô': '&#244;', 'õ': '&#245;', 'ú': '&#250;'}

    for char in regex:
        if '&#' in string:
            string = string.replace(regex[char], char)
        else:
            break

    return string


def read_file(file_name, path=''):
    extension = file_name.split('.')[-1]
    if extension == 'xlsx':
        return _read_xlsx(file_name, path=path)
    elif extension == 'csv':
        return _read_csv(file_name, path=path)
    else:
        print('Arquivo não suportado...')


def _read_xlsx(file_name, path=''):
    # print(f'Abrindo {path + file_name}')
    work_book = load_workbook(path + file_name)  # abrindo o Workbook test.xlsx
    sheet = work_book.active  # selecionando a planilha ativa

    all_registers = list()  # registros da planilha toda
    for line in sheet:  # iterando em todas as linhas da planilha
        register = list()  # registro de uma linha
        for cell in line:
            register.append(cell.value)
        all_registers.append(register)

    del all_registers[0]  # remove os titulos
    work_book.close()  # fecha o arquivo
    return all_registers


def _read_csv(file_name, path=''):
    # print(f'Abrindo {path + file_name}')
    all_registers = list()
    with open(path + file_name, encoding='ISO-8859-1') as csv_file:
        for row in csv.reader(csv_file):
            register = ''.join(row).replace('"', '').split('\t')
            all_registers.append(register)
        # o arquivo ja e fechado automaticamente

    del all_registers[0]  # remove os titulos
    return all_registers
