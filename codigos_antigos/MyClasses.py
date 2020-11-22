from MyUtil import convert_ascii
from collections import defaultdict, OrderedDict


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
        if 'PERIÓDICO' in self.subtipo_producao:
            if nome != 'Cidade' and convert_ascii(nome) != 'Número do DOI' and nome != 'URL do DOI':
                self.detalhamentos[convert_ascii(nome)] = convert_ascii(valor)
        else:
            if nome != 'ISBN':
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
            self.linha_pesquisa, self.projeto_pesquisa, self.doi, self.divulgacao, self.fasciculo, \
            self.issn_titulo_periodico, self.idioma, self.natureza, self.nome_editora, self.numero_pagina_final, \
            self.numero_pagina_incial, self.observacao, self.serie, self.url, \
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
        return self.isbn_issn


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


