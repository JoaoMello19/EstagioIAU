# -*- coding: utf-8 -*-
"""
Created on Thu Aug 27 14:42:55 2020

@author: Leila Gomes
"""
import pandas as pd
import plotnine as p

def grafico_media_docentes():
    docentes = pd.read_csv("docentes.tsv", sep='\t')
    programas = pd.read_csv("progs.tsv", sep='\t')
    
    
    res = pd.DataFrame(columns=['Sigla', 'Categoria', 'Quantidade', 'Sum'])
    for index, row in programas.iterrows():
        uni = docentes[(docentes['Programa'] == row['Programa'])]
        if len(uni.index) > 0:
            colaboradores = uni[(uni['Categoria'] == 'COLABORADOR')]
            permanentes = uni[(uni['Categoria'] == 'PERMANENTE')]
            qtdC = round(len(colaboradores.index)/3, 2)
            qtdP = round(len(permanentes.index)/3, 2)
            
            verifica = res.index[(res['Sigla'] == row['Sigla'])]
            if len(verifica) == 0:
                nova_linha = pd.DataFrame([(row['Sigla'],'PERMANENTE', qtdP, qtdP+qtdC)], columns=['Sigla', 'Categoria', 'Quantidade', 'Sum'])
                res = res.append(nova_linha, ignore_index=True)
                nova_linha = pd.DataFrame([(row['Sigla'],'COLABORADOR', qtdC, qtdP+qtdC)], columns=['Sigla', 'Categoria', 'Quantidade', 'Sum'])
                res = res.append(nova_linha, ignore_index=True)
            else:
                res.at[verifica[0], 'Quantidade'] += qtdP
                res.at[verifica[0], 'Sum'] += qtdP+qtdC
                res.at[verifica[1], 'Quantidade'] += qtdC
                res.at[verifica[1], 'Sum'] += qtdP+qtdC
                
    res = res.sort_values(by=['Sum'], ignore_index=True, kind='mergesort')
    lista  = res['Sigla'].tolist()
    
    g= (
        p.ggplot(res, p.aes(x = 'Sigla', y = 'Quantidade', fill = 'Categoria', label = 'Quantidade'))
        + p.geom_bar(stat = "identity", width=1.2)
        + p.geom_text(size = 5, position = p.position_stack(vjust = 0.5), fontweight="bold")
        + p.theme_classic()
        + p.theme(axis_text_x = p.element_text(angle=85), figure_size=(15, 10))
        + p.ylab(" ")
        + p.xlab("Instituição")
        + p.scale_x_discrete(limits=lista)
      )
    
    g.draw()
    
def grafico_concluintes_por_docente(dado, titulo):
    docentes = pd.read_csv("docentes.tsv", sep='\t')
    programas = pd.read_csv("progs.tsv", sep='\t')
    trabalhos = pd.read_csv("trabalhos_conclusao.tsv", sep='\t')
    
    res = pd.DataFrame(columns=['Instituição', 'dpd', 'dpdp', 'mpd', 'mpdp', 'qtdDoutores', 'qtdMestres', 'qtdDocentes', 'qtdDocentesP'])
    
    for index, row in programas.iterrows():
        uni = docentes[(docentes['Programa'] == row['Programa'])]
        if len(uni.index) > 0:
            colaboradores = uni[(uni['Categoria'] == 'COLABORADOR')]
            permanentes = uni[(uni['Categoria'] == 'PERMANENTE')]
            qtdC = len(colaboradores.index)
            qtdP = len(permanentes.index)
            tcc = trabalhos[(trabalhos['Programa'] == row['Programa'])]
            verifica = res.index[(res['Instituição'] == row['Sigla'])]
            if len(verifica) == 0:
                if len(tcc.index) > 0:
                    doutorados = tcc[(tcc['Tipo de Trabalho de Conclusão'] == 'TESE')]
                    mestrados = tcc[(tcc['Tipo de Trabalho de Conclusão'] == 'DISSERTAÇÃO')]
                    nova_linha = pd.DataFrame([(row['Sigla'], round(len(doutorados.index)/(qtdP+qtdC),2), round(len(doutorados.index)/qtdP,2),round(len(mestrados.index)/(qtdP+qtdC),2), round(len(mestrados.index)/qtdP,2), len(doutorados.index), len(mestrados.index), qtdC+qtdP, qtdP)], columns=['Instituição', 'dpd', 'dpdp', 'mpd', 'mpdp', 'qtdDoutores', 'qtdMestres', 'qtdDocentes', 'qtdDocentesP'])
                else:
                    nova_linha = pd.DataFrame([(row['Sigla'], 0, 0, 0, 0, 0, 0, qtdC+qtdP, qtdP)], columns=['Instituição', 'dpd', 'dpdp', 'mpd', 'mpdp', 'qtdDoutores', 'qtdMestres', 'qtdDocentes', 'qtdDocentesP'])
                res = res.append(nova_linha, ignore_index=True)
            else:
                doutorados = tcc[(tcc['Tipo de Trabalho de Conclusão'] == 'TESE')]
                mestrados = tcc[(tcc['Tipo de Trabalho de Conclusão'] == 'DISSERTAÇÃO')]
                qtdDoutores = res['qtdDoutores'].iloc[verifica[0]] + len(doutorados.index) 
                qtdMestres = res['qtdMestres'].iloc[verifica[0]] + len(mestrados.index) 
                qtdDocentes = res['qtdDocentes'].iloc[verifica[0]] + qtdP+qtdC
                qtdDocentesP = res['qtdDocentesP'].iloc[verifica[0]] + qtdP
                res.at[verifica[0],'qtdDoutores'] = qtdDoutores
                res.at[verifica[0],'qtdMestres'] = qtdMestres   
                res.at[verifica[0],'qtdDocentes'] = qtdDocentes
                res.at[verifica[0],'qtdDocentesP'] = qtdDocentesP
                res.at[verifica[0],'dpd'] = round(qtdDoutores/qtdDocentes,2)
                res.at[verifica[0],'dpdp'] = round(qtdDoutores/qtdDocentesP,2)
                res.at[verifica[0],'mpd'] = round(qtdMestres/qtdDocentes,2)
                res.at[verifica[0],'mpdp'] = round(qtdMestres/qtdDocentesP,2)
                
    
    res = res.sort_values(by=[dado],ignore_index=True, kind='mergesort')
    lista  = res['Instituição'].tolist()
    print(res.head(10))
    position = p.position_dodge(width = 1)
    width = .75
        
    g= (
        p.ggplot(res, p.aes(x = 'Instituição', y = dado, label = dado))
        + p.geom_col(fill='darkblue', width=width, position=position)
        + p.geom_text(size = 6, fontweight="bold",position = p.position_nudge(y=0.005))
        + p.theme_classic()
        + p.theme(axis_text_x = p.element_text(angle=85), figure_size=(15, 10))
        + p.xlab("Instituição")
        + p.ylab(" ")
        + p.ggtitle(titulo)
        + p.scale_x_discrete(limits=lista)
      )
    
    g.draw()

def grafico_tcc_por_idioma(tipo):
    trabalhos = pd.read_csv("trabalhos_conclusao.tsv", sep='\t')
    programas = pd.read_csv("progs.tsv", sep='\t')
    
    
    res = pd.DataFrame(columns=['Instituição', 'Idioma', 'Nome'])
    for index, row in programas.iterrows():
        uni = trabalhos[(trabalhos['Programa'] == row['Programa'])]
        uni = uni[(uni['Tipo de Trabalho de Conclusão'] == tipo)]
        for index2, row2 in uni.iterrows(): 
            nova_linha = pd.DataFrame([(row['Sigla'],row2['Idioma'], row2['Título'])], columns=['Instituição', 'Idioma', 'Nome'])
            res = res.append(nova_linha, ignore_index=True)
    
    if tipo=='TESE':
        titulo = "Teses por idioma"
    else:
        titulo = "Dissertações por idioma"            
        
    g= (
        p.ggplot(res, p.aes(x = 'Instituição', fill = 'Idioma'))
        + p.geom_bar(position="fill")
        + p.geom_text(p.aes(label='stat(count)'), stat='count', position='fill', fontweight='bold')
        + p.theme_classic()
        + p.theme(axis_text_x = p.element_text(angle=85), figure_size=(15, 10))
        + p.ylab(" ")
        + p.xlab("Instituição")
        + p.ggtitle(titulo)
      )
    
    g.draw()

def grafico_docentes_formados(tipo_docente):

    autores = pd.read_csv("autores.tsv", sep='\t')
    programas = pd.read_csv("progs.tsv", sep='\t')
    trabalhos = pd.read_csv("trabalhos_conclusao.tsv", sep='\t')
    
    
    autores_pos_p= {}
    autores_pos_c= {}    
    
    res = pd.DataFrame(columns=['Instituição', 'Categoria', 'Qtd', 'Total'])
    for index, row in autores.iterrows():
        if row['Tipo'] == 'ARTIGO EM PERIÓDICO':
            if row['Nome'] not in autores_pos_p or autores_pos_p[row['Nome']] > row['Posicao']:
                autores_pos_p[row['Nome']] = row['Posicao']
        else:
            if row['Nome'] not in autores_pos_c or autores_pos_c[row['Nome']] > row['Posicao']:
                autores_pos_c[row['Nome']] = row['Posicao']
        
    if tipo_docente == 'Doutor':
        tipo_trabalho = 'TESE'
    else:
        tipo_trabalho = 'DISSERTAÇÃO'
    for index, row in programas.iterrows():
        uni = autores[(autores['Programa'] == row['Programa'])]
        if len(uni) > 0:
            tcc = trabalhos[(trabalhos['Programa'] == row['Programa'])]
            if len(tcc) > 0:
                doutorados = tcc[(tcc['Tipo de Trabalho de Conclusão'] == tipo_trabalho)]
                if len(doutorados) > 0:
                    qtd_publicacoes = 0
                    qtd_periodicos = 0
                    qtd_periodico_primeiro_autor = 0
                    for index2, aluno in doutorados.iterrows():
                        publicou = False
                        publicou_periodico = False
                        if aluno['Autor'] in autores_pos_c:
                            if not publicou:
                                qtd_publicacoes += 1
                                publicou = True
                        if aluno['Autor'] in autores_pos_p:
                            if not publicou:
                                qtd_publicacoes+=1
                                publicou = True
                            if not publicou_periodico:
                                qtd_periodicos += 1
                                if autores_pos_p[aluno['Autor']] == 1:
                                    qtd_periodico_primeiro_autor+=1
                                publicou_periodico = True
                    verifica = res.index[(res['Instituição'] == row['Sigla'])]
                    if len(verifica) == 0:
                        nova_linha = pd.DataFrame([(row['Sigla'], tipo_docente + ' com publicação em periodico como primeiro autor', float(qtd_periodico_primeiro_autor), float(len(doutorados)))], columns=['Instituição', 'Categoria','Qtd','Total'])
                        res = res.append(nova_linha, ignore_index=True)
                        nova_linha = pd.DataFrame([(row['Sigla'], tipo_docente, float(len(doutorados)), float(len(doutorados)))], columns=['Instituição', 'Categoria','Qtd','Total'])
                        res = res.append(nova_linha, ignore_index=True)
                        nova_linha = pd.DataFrame([(row['Sigla'], tipo_docente + ' com publicação',float(qtd_publicacoes),float(len(doutorados)))], columns=['Instituição', 'Categoria','Qtd','Total'])
                        res = res.append(nova_linha, ignore_index=True)
                        nova_linha = pd.DataFrame([(row['Sigla'], tipo_docente + ' com publicação em periodico', float(qtd_periodicos), float(len(doutorados)))], columns=['Instituição', 'Categoria','Qtd','Total'])
                        res = res.append(nova_linha, ignore_index=True)
                        
                    else:
                        res.at[verifica[0], 'Qtd'] += qtd_periodico_primeiro_autor
                        res.at[verifica[0], 'Total'] += len(doutorados)
                        res.at[verifica[1], 'Qtd'] += len(doutorados)
                        res.at[verifica[1], 'Total'] += len(doutorados)
                        res.at[verifica[2], 'Qtd'] += qtd_publicacoes
                        res.at[verifica[2], 'Total'] += len(doutorados)
                        res.at[verifica[3], 'Qtd'] += qtd_periodicos
                        res.at[verifica[3], 'Total'] += len(doutorados)
                        
                
    res = res.sort_values(by='Total', ignore_index=True, kind='mergesort')
    lista  = res['Instituição'].tolist()
        
    g= (
        p.ggplot(res, p.aes(x = 'Instituição', y = 'Qtd', fill = 'Categoria', label='Qtd'))
        + p.geom_bar(stat = "identity", width=2, position=p.position_dodge())
        + p.theme_classic()
        + p.geom_text(size = 5, position = p.position_dodge(1.5), fontweight="bold")
        + p.theme(axis_text_x = p.element_text(angle=85), figure_size=(30,15))
        + p.ylab(" ")
        + p.xlab("Instituição")
        + p.scale_x_discrete(limits=lista)
      )
    
    g.draw()

def grafico_publicacoes_por_qualis():
    df1 = pd.read_csv("periodicos.tsv", sep='\t', na_values='null', keep_default_na=False)
    df2 = pd.read_csv("progs.tsv", sep='\t')
    
    qualis_op = ['A1', 'A2', 'A3', 'A4','B1', 'B2', 'B3', 'B4', 'C ', 'NA', 'NP']
    
    df3 = pd.DataFrame(columns=['Instituição', 'Qualis', 'Quantidade', 'Soma'])
    for index, row in df2.iterrows():
        uni = df1[(df1['Programa'] == row['Programa'])]
        if len(uni) > 0:
            for op in qualis_op:
                qualis = uni[(uni['Qualis'] == op)]
                if len(qualis) > 0:
                    verifica = df3.index[(df3['Instituição'] == row['Sigla']) & (df3['Qualis'] == op)]
                    if len(verifica) == 0:
                        nova_linha = pd.DataFrame([(row['Sigla'],op, float(len(qualis)))], columns=['Instituição', 'Qualis', 'Quantidade'])
                        df3 = df3.append(nova_linha, ignore_index=True)
                    else:
                        df3.at[verifica[0], 'Quantidade'] += len(qualis)
                        
    df3 = df3.sort_values(by=['Instituição'], ignore_index=True)
    res = df3.copy()
    soma = 0
    for index, row in df3.iterrows():
        soma+=row['Quantidade']
        if index==len(df3)-1 or row['Instituição'] != df3['Instituição'].iloc[index+1]: 
            res.loc[res['Instituição'] == row['Instituição'], ['Soma']] = soma               
            soma = 0
            
    res = res.sort_values(by=['Soma'], ignore_index=True, kind='mergesort')
    lista  = res['Instituição'].tolist()
    lista = list(dict.fromkeys(lista))
    
    g= (
        p.ggplot(res, p.aes(x = 'Instituição', y = 'Quantidade', fill = 'Qualis'))
        + p.geom_col(stat = "identity", width=0.5)
        + p.theme_classic()
        + p.theme(axis_text_x = p.element_text(angle=85), figure_size=(15, 10))
        + p.ylab(" ")
        + p.xlab("Instituicao")
        + p.scale_x_discrete(limits=lista)
      )
        
    g.draw()

def grafico_publicacoes_por_qualis_ponderado():
    df1 = pd.read_csv("periodicos.tsv", sep='\t', na_values='null', keep_default_na=False)
    df2 = pd.read_csv("progs.tsv", sep='\t')
    df4 = pd.read_csv("docentes.tsv", sep='\t')
    
    qualis_op = ['A1', 'A2', 'A3', 'A4','B1', 'B2', 'B3', 'B4', 'C ', 'NA', 'NP']
    pesos={'A1': 1.00, 'A2': 0.875, 'A3' : 0.75, 'A4' : 0.625, 'B1': 0.5, 'B2': 0.2, 'B3' : 0.1, 'B4' : 0.05, 'C ':0, 'NA':0, 'NP':0}
    
    df3 = pd.DataFrame(columns=['Instituição', 'Qualis', 'Quantidade', 'Soma'])
    for index, row in df2.iterrows():
        uni = df1[(df1['Programa'] == row['Programa'])]
        if len(uni) > 0:
            for op in qualis_op:
                qualis = uni[(uni['Qualis'] == op)]
                if len(qualis) > 0:
                    verifica = df3.index[(df3['Instituição'] == row['Sigla']) & (df3['Qualis'] == op)]
                    if len(verifica) == 0:
                        nova_linha = pd.DataFrame([(row['Sigla'],op, len(qualis))], columns=['Instituição', 'Qualis', 'Quantidade'])
                        df3 = df3.append(nova_linha, ignore_index=True)
                    else:
                        df3.at[verifica[0], 'Quantidade'] += len(qualis)
    
    df3 = df3.sort_values(by=['Instituição'], ignore_index=True)
    res = df3.copy()
    soma = 0
    for index, row in df3.iterrows():
        docentes = df4[(df4['IES Sigla'] == row['Instituição'])]
        valor_ponderado = row['Quantidade']*pesos[row['Qualis']]
        soma+= valor_ponderado/len(docentes)
        res.at[index, 'Quantidade'] = valor_ponderado/len(docentes)
        res.at[index, 'Qualis'] = row['Qualis']+'('+str(pesos[row['Qualis']])+')'
        if index==len(df3)-1 or row['Instituição'] != df3['Instituição'].iloc[index+1]:
            res.loc[res['Instituição'] == row['Instituição'], ['Soma']] = soma
            soma = 0
            
    res["Soma"] = pd.to_numeric(res["Soma"])
    res["Quantidade"] = pd.to_numeric(res["Quantidade"])
    res = res.sort_values(by=['Soma'], ignore_index=True, kind='mergesort')
    lista  = res['Instituição'].tolist()
    lista = list(dict.fromkeys(lista))
    
    g= (
        p.ggplot(res, p.aes(x = 'Instituição', y = 'Quantidade', fill='Qualis'))
        + p.geom_col(stat = "identity", width=0.5)
        + p.theme_classic()
        + p.theme(axis_text_x = p.element_text(angle=85), figure_size=(15, 10))
        + p.ylab(" ")
        + p.xlab("Instituicao")
        + p.scale_x_discrete(limits=lista)
      )
        
    g.draw()


    