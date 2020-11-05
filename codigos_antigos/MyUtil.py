def get_initials(prog_name):
    words = prog_name.split(" ")
    if len(words) > 1:
        return "".join([word[0] for word in words if len(word) > 0])
    return prog_name[0]


def read_programas(path):
    registers = read_file('programas.xlsx', path=path)
    return {row[3]: f'{row[8]}-{get_initials(row[4])}' for row in registers}


def read_programas_nivel():
    registers = read_file('relatorio.xlsx')
    return {row[0]: f'{row[3]}-{get_initials(row[1])}-{row[6]}' for row in registers}


def format_row(row):
    """
    Formata uma linha, separando em clunas
    :param row: a linha, com as tags indicadoras de conteudo
    :return: uma lista, correspondente a cada campo
    """
    f_row = list()
    for cell in row:
        if '</t>' in cell:  # caso seja uma tag de conteudo
            f_row.append(cell[cell.find('>') + 1:cell.find('</t>')])
    # f_row = [cell[cell.find('>') + 1:cell.find('</t>')] for cell in row if '</t> in cell']
    return f_row


def open_large_xls(file_name, my_sheet, path=''):
    """
    Abre arquivos xlsx que são muito grandes
    :param file_name: nome do arquivo
    :param my_sheet: folha da planilha que contem os dados
    :param path: caminho para a planilha
    :return: uma lista contendo as linhas da planilha
    """
    import zipfile
    from bs4 import BeautifulSoup

    paths = []
    file = zipfile.ZipFile(path + file_name, "r")

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
        if '&#' not in string:
            break
        string = string.replace(regex[char], char)

    return string


def read_file(file_name, path=''):
    extension = file_name.split('.')[-1]
    if extension == 'xlsx':
        return read_xlsx(file_name, path=path)
    elif extension == 'csv':
        return read_csv(file_name, path=path)
    else:
        print('Arquivo não suportado...')


def read_xlsx(file_name, path=''):
    from openpyxl import load_workbook

    work_book = load_workbook(path + file_name)     # abrindo o Workbook test.xlsx
    sheet = work_book.active                        # selecionando a planilha ativa

    # para cada linha e para cada valor da linha
    all_registers = [[cell.value for cell in line] for line in sheet]

    del all_registers[0]    # remove os titulos
    work_book.close()       # fecha o arquivo
    return all_registers


def read_csv(file_name, path=''):
    import csv

    all_registers = list()
    with open(path + file_name, encoding='ISO-8859-1') as csv_file:
        for row in csv.reader(csv_file):
            register = ''.join(row).replace('"', '').split('\t')
            all_registers.append(register)
        # o arquivo ja e fechado automaticamente

    del all_registers[0]  # remove os titulos
    return all_registers
