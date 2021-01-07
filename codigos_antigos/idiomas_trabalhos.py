import plotly.offline as py
import plotly.graph_objs as go
import MyUtil
from collections import defaultdict

PATH = 'dados_arquitetura_'
ANOS = ['2013', '2014', '2014', '2015']

def read_idioma_trabalhos(filepath, idiomas):
    registers = MyUtil.read_file('trabalhos_conclusao.tsv', filepath)
    trabalhos = defaultdict(lambda: defaultdict())
    for row in registers:
        i_programa = 16
        i_idioma = 7
        
        #tratamento de casos especificos
        while len(row[i_programa]) != 13:
            i_programa+=1
        
        while not row[i_idioma].isupper():
            i_idioma+=1
            
        # [code][idioma] = quantidade
        if row[i_programa] in trabalhos:
            if row[i_idioma] in trabalhos[row[i_programa]]:
                trabalhos[row[i_programa]][row[i_idioma]] += 1
            else:
                trabalhos[row[i_programa]][row[i_idioma]] = 1
            trabalhos[row[i_programa]]['total'] += 1
        else:
            trabalhos[row[i_programa]]['total'] = 1
            trabalhos[row[i_programa]][row[i_idioma]] = 1
            
        if row[i_idioma] not in idiomas:
            idiomas.append(row[i_idioma])


    return trabalhos

def contar_porcentagens_idiomas(trabalhos, idiomas):
    for programa in trabalhos.values():
        for idioma in idiomas:
            if idioma not in programa:
                programa[idioma] = 0
            programa[idioma+' %'] = 100*programa[idioma]/programa['total']
        #print(programa)

    return programa

def atualizar_cod_programa(trabalhos):
    trabalhos_novo = defaultdict(lambda: defaultdict())

    for code in trabalhos.keys():
        new_code = code
        if code in programas_nivel.keys():
            new_code = programas_nivel[code]
        elif code in programas.keys():
            new_code = programas[code]

        trabalhos_novo[new_code] = trabalhos[code]

    return trabalhos_novo

def make_chart(chart_data):
    fig = go.Figure()
    i = 0
    colors = ['#9b59b6', '#1abc9c', '#3498db', '#ff7675', '#fd79a8', '#fdcb6e']
    for idioma in idiomas:
        fig.add_trace(go.Bar(x=list(chart_data.keys()),
                        y=[f_d[idioma+' %'] for f_d in chart_data.values()],
                        name= idioma+' %',
                        text=['<b>'+'{0:.2f}'.format(f_d[idioma+' %'])+'</b>' for f_d in chart_data.values()],
                        textposition='inside',
                        insidetextanchor = 'middle',
                        textfont_size=20,
                        marker={'color': colors[i]}))
        i += 1

    title = {
        'text': f'Idiomas de trabalhos de conclusão ({", ".join(ANOS)})',
        'x': 0.5,
        'xanchor': 'center',
        'font': {
            'color': '#000000',
            'size': 50
        }
    }

    subtitle = {
        'font': {'color': '#000000', 'size': 30},
        'orientation': 'h',
        'x': 0,
        'y': 1
    }

    layout = go.Layout(title=title,
                       xaxis={'title': 'Instituição'},
                       barmode='stack',
                       legend=subtitle,
                       font_size=40,
                       height=2300,
                       width=5000)
    fig.update_layout(layout)
    py.iplot(fig)

def sort_dict(dict_to_sort):
    return dict(sorted(dict_to_sort.items(), key=lambda item: item[1]['PORTUGUES %']))


list_trabalhos=dict()
list_docentes=dict()
programas=dict()
idiomas = list()

for ano in ANOS:     
    list_trabalhos_add = read_idioma_trabalhos(PATH+ano+'/', idiomas)
    for programa in list_trabalhos_add.keys():
        if programa in list_trabalhos.keys():
            idiomas_programa = list_trabalhos_add[programa]
            for idioma in idiomas_programa.keys():
                if idioma in list_trabalhos[programa]:
                    list_trabalhos[programa][idioma] += idiomas_programa[idioma]
                else:
                    list_trabalhos[programa][idioma] = idiomas_programa[idioma]
        else:
            list_trabalhos[programa] = list_trabalhos_add[programa]
    programas.update(MyUtil.read_programas(PATH+ano+'/'))

programas_nivel = MyUtil.read_programas_nivel()
contar_porcentagens_idiomas(list_trabalhos, idiomas)
list_trabalhos = atualizar_cod_programa(list_trabalhos)
#print(list_trabalhos)
list_trabalhos = sort_dict(list_trabalhos)
idiomas.sort(key = 'PORTUGUES'.__eq__)
make_chart(list_trabalhos)
