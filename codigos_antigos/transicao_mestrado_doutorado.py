import MyUtil
from collections import defaultdict
import plotly.graph_objs as go
import numpy as np

PATH = 'dados_arquitetura_'
ANOS = ['2013','2014','2015', '2016']

def read_mestres(filepath):
    registers = MyUtil.read_file('trabalhos_conclusao.xlsx', filepath)
    trabalhos = defaultdict(lambda:set())

    for row in registers:
        if row[10] == 'DISSERTAÇÃO':
            trabalhos[row[3]].add(row[9])

    return trabalhos


def read_discentes(filepath, discentes):
    registers = MyUtil.read_file('discentes.xlsx', filepath)

    for row in registers:
        if row[11] == 'Doutorado' and row[12] == 'MATRICULADO':
            discentes[row[8]] = row[3]

def get_qtd_transicao_mestrado_doutorado(mestres, discentes):
    res = defaultdict()
    
    for programa in mestres.keys():
        for mestre in mestres[programa]:
            if mestre in discentes.keys():
                transicao = programa+'-'+discentes[mestre]
                if transicao not in res.keys():
                    res[transicao] = 1
                else:
                    res[transicao] += 1
        
    return res

def get_graph_data(qtd_transicoes):
    data = {
        'label':[],
        'color':[],
        'source': [],
        'target': [],
        'value': [],
        'link_color': []
    }
    
    label_origem = []
    label_destino = []
    color_origem = []
    color_destino = []
    
    for transicao in qtd_transicoes.keys():
        pgs = transicao.split('-')
        
        programa_origem = pgs[0]
        if pgs[0] in programas_nivel.keys():
            programa_origem = programas_nivel[pgs[0]]
        elif pgs[0] in programas.keys():
            programa_origem = programas[pgs[0]]
            
        programa_destino = pgs[1]
        if pgs[1] in programas_nivel.keys():
            programa_destino = programas_nivel[pgs[1]]
        elif pgs[1] in programas.keys():
            programa_destino = programas[pgs[1]]
            
            
        if programa_origem not in label_origem:
            label_origem.append(programa_origem)
            if programa_origem in label_destino:
                i = label_destino.index(programa_origem)
                rgb = color_destino[i]
            else:
                cor_diferente = False
                while not cor_diferente:
                    color = (int(np.random.rand()*256), int(np.random.rand()*256), int(np.random.rand()*256))
                    rgb = 'rgb'+str(color)
                    cor_diferente = rgb not in color_destino and rgb not in color_origem
                
            color_origem.append(rgb)
            
        if programa_destino not in label_destino:
            label_destino.append(programa_destino)
            if programa_destino in label_origem:
                i = label_origem.index(programa_destino)
                rgb = color_origem[i]
            else:
                cor_diferente = False
                while not cor_diferente:
                    color = (int(np.random.rand()*256), int(np.random.rand()*256), int(np.random.rand()*256))
                    rgb = 'rgb'+str(color)
                    cor_diferente = rgb not in color_destino and rgb not in color_origem
                
            color_destino.append(rgb)
        
        i_o = label_origem.index(programa_origem)
        i_d = label_destino.index(programa_destino)
        
        data['source'].append(i_o)
        data['link_color'].append(color_origem[i_o])
        data['target'].append(i_d)
        data['value'].append(qtd_transicoes[transicao])
            
    for i in range(0, len(data['target'])):
        data['target'][i] = data['target'][i]+len(label_origem)
    
    data['label'] = label_origem 
    data['color'] = color_origem
    for label in label_destino:
        data['label'].append(label)
        
    for color in color_destino:
        data['color'].append(color)
    
    return data


def make_chart(chart_data):
    fig = go.Figure(data=[go.Sankey(
    arrangement = 'perpendicular',
    node = dict( 
      pad = 40,
      thickness = 50,
      line = dict(width = 0.5),
      label = chart_data['label'],
      color = chart_data['color']
    ),
    link = dict(
      source = chart_data['source'],
      target = chart_data['target'],
      value = chart_data['value'],
      color=chart_data['link_color']
    ))])

    fig.update_layout(title_text=f'Alunos que concluiram o mestrado e onde se matricularam no doutorado ({", ".join(ANOS)})', font_size=10, height=1500)
    fig.show()

list_mestres=dict()
list_docentes=dict()
discentes=dict()
programas=dict()

for ano in ANOS:        
    list_mestres_add = read_mestres(PATH+ano+'/')
    for programa in list_mestres_add:
        if programa in list_mestres:
            list_mestres[programa].update(list_mestres_add[programa])
        else:
            list_mestres[programa] = list_mestres_add[programa]
    programas.update(MyUtil.read_programas(PATH+ano+'/'))
    read_discentes(PATH+ano+'/', discentes)
    
programas_nivel = MyUtil.read_programas_nivel()
res = get_qtd_transicao_mestrado_doutorado(list_mestres, discentes)
data = get_graph_data(res)



make_chart(data)
