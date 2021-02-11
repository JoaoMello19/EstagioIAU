import MyUtil
import plotly.offline as py
import plotly.graph_objs as go
from collections import defaultdict


ANOS = range(2013, 2020)


def read_nomes_programas():
    nomes = dict()
    for ano in ANOS:
        nomes.update(MyUtil.read_programas(f'dados_arquitetura_{ano}/'))
    return nomes


def read_files(file_name):
    for ano in ANOS:
        with open(f'dados_arquitetura_{ano}/{file_name}', encoding='Latin-1') as file:
            file = (row for row in file)
            next(file)  # ignora a primeira linha
            for row in file:
                yield row.split('\t')


def get_titles(rows):
    titles = defaultdict(lambda: list())
    for row in rows:
        titles[row[9]].append(row[3])
    return titles


def get_publicacoes_conjunto(titles):
    conjuntos = defaultdict(lambda: defaultdict(lambda: 0))
    for t in titles.values():
        if len(t) > 1:
            if t[0] < t[1]:
                conjuntos[t[0]][t[1]] += 1
            else:
                conjuntos[t[1]][t[0]] += 1

    conjuntos = {
        set_code(key): {
            set_code(k): v for k, v in value.items()
        } for key, value in conjuntos.items()
    }

    return conjuntos


def set_code(code):
    if code in programas_nivel.keys():
        return programas_nivel[code]
    elif code in nomes_programas.keys():
        return nomes_programas[code]
    return code


def prepare_data(chart_data):
    x_all, y_all, v_all = [], [], []

    for code in chart_data.keys():
        x_all.extend((code for i in range(len(chart_data[code].keys()))))
        y_all.extend((k for k in chart_data[code].keys()))
        v_all.extend((v for v in chart_data[code].values()))

    return x_all, y_all, v_all


def make_chart(chart_data, chart_title):
    title = {
        'text': chart_title,
        'x': 0.5,
        'xanchor': 'center',
        'font': {
            'color': '#000000',
            'size': 20
        }
    }
    fig = go.Figure(layout=go.Layout(title=title, legend={}))

    x_all, y_all, v_all = prepare_data(chart_data)

    fig.add_trace(go.Scatter(
        x=x_all,
        y=y_all,
        text=v_all,
        mode='markers',
        marker={
            'size': [10 + v / 10 for v in v_all],
            'color': v_all,
            'showscale': True
        }
    ))

    py.iplot(fig)


programas_nivel = MyUtil.read_programas_nivel()
nomes_programas = read_nomes_programas()

periodicos = read_files('periodicos.tsv')
titles_periodicos = get_titles(periodicos)
periodicos_conj = get_publicacoes_conjunto(titles_periodicos)
make_chart(periodicos_conj, f'Artigos em Periódico Publicado em Conjunto {tuple(ANOS)}')

conferencias = read_files('conferencias.tsv')
titles_conferencias = get_titles(conferencias)
conferencias_conj = get_publicacoes_conjunto(titles_conferencias)
make_chart(conferencias_conj, f'Artigos em Conferências Publicado em Conjunto {tuple(ANOS)}')