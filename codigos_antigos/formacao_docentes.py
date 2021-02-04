import MyUtil
from collections import defaultdict
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go


FILE_NAME = 'docentes.tsv'
PATH = 'dados_arquitetura_'
ANOS = ['2017', '2018', '2019']


def read_docentes(filepath, docentes):
    registers = MyUtil.read_file(FILE_NAME, filepath)
    for row in registers:
        i_categoria = 14
        
        if row[i_categoria] in {'PERMANENTE', 'COLABORADOR'}:
            i_programa = 0
            i_nome = 1
            i_ano = 8
            i_pais = 10
            i_inst = 11

            docente = {
                'nome': row[i_nome],
                'pais': row[i_pais],
                'instituicao': row[i_inst],
                'ano': row[i_ano]
            }

            if docente not in docentes[row[i_programa]]:
                docentes[row[i_programa]].append(docente)


    return docentes

def read_programas(path):
    registers = MyUtil.read_file('programas.xlsx', path=path)
    return {row[3]: [f'{row[8]}-{MyUtil.get_initials(row[4])}', row[9]] for row in registers}

def get_formacao_docentes_df(docentes):
    res = pd.DataFrame(columns=["Programa","Docente", "Categoria", "Ano"])
    
    for programa in docentes.keys():
        new_code = programa
        if programa in programas_nivel.keys():
            new_code = programas_nivel[programa]
        elif programa in programas.keys():
            new_code = programas[programa][0]
            
        for docente in docentes[programa]:
            if docente['pais'] != 'Brasil':
                categoria = 'Instituição Estrangeira'
            elif docente['instituicao'] != programas[programa][1]:
                categoria = 'Instituição Brasileira'
            else:
                categoria = 'Mesma Instituição'
            
            nova_linha = {"Programa":new_code, "Docente": docente['nome'], "Categoria": categoria, "Ano": docente['ano']}
            res = res.append(nova_linha, ignore_index=True)
        
    return res



def make_chart(chart_data):
    fig = px.strip(chart_data, x="Programa", y="Ano", color="Categoria", stripmode="overlay")

    title = {
            'text': f'Formação dos Docentes(Permanente e Colaboradores) ({", ".join(ANOS)})',
            'x': 0.5,
            'xanchor': 'center',
            'font': {
                'color': '#000000',
                'size': 20
            }
    }

    layout = go.Layout(title=title,
                           font_size=15,
                           height=1000,
                           width=2500)
    
    fig.update_layout(layout)

    fig.show()

    
list_docentes = defaultdict(lambda: list())
programas = dict()

for ano in ANOS:
    read_docentes(PATH+ano+'/', list_docentes)
    programas.update(read_programas(PATH+ano+'/'))
    
programas_nivel = MyUtil.read_programas_nivel()
df = get_formacao_docentes_df(list_docentes)
make_chart(df)
