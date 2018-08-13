import pandas as pd
import plotly.plotly as py
import plotly
import plotly.tools as tls
import numpy as np
import plotly.graph_objs as go
from plotly.graph_objs import *
from datetime import date, timedelta
from calendario_anual import *
from dadoframe import chesf_dataframe, ons_dataframe, uni

class Stats():
    """Caracteriza as alterações de cheias anuais quanto à
    frequencia, duração e periodo de ocorrência."""

    def __init__(self):
        """inicia os atributos"""
        self.chesf = transform(chesf_dataframe())
        self.ons = transform(ons_dataframe())
        #self.result = uni()
        self.ascensao = []
        self.recessao = None
        self.reversao = None

    def taxas_ascensao(self, posto = 'chesf'):
        """Calcula as taxas de ascensao, recessao"""
        if posto == 'chesf':
            df = self.chesf
        else:
            df = self.ons

        dic = {}
        reversao = {}
        for col in df.columns:
            dia = 0
            lista = []
            tempo = 1
            flag = False
            rev=0
            for index, linha in df.iterrows():
                if dia == 0:
                    #print("Entra")
                    self.ponteiroum = linha[col]
                    self.ponteirodois = linha[col]
                    dia += 1

                elif linha[col] > self.ponteirodois:
                    #print("Entra")
                    self.ponteirodois = linha[col]
                    flag = True
                    tempo+=1
                elif flag:
                    aux = self.ponteirodois - self.ponteiroum
                    aux = aux / tempo
                    lista.append(aux)
                    flag = False
                    tempo = 1
                    rev+=1
                else:
                    dia = 0
            dic[col] = lista
            reversao[col]=rev
        self.ascensao = pd.Series(dic)
        return(reversao,self.ascensao)

    def taxas_recessao(self, posto = 'chesf'):
        """Calcula as taxas de ascensao, recessao"""
        if posto == 'chesf':
            df = self.chesf
        else:
            df = self.ons

        dic = {}
        reversao = {}
        for col in df.columns:
            dia = 0
            lista = []
            tempo = 1
            flag = False
            rev = 0
            for index, linha in df.iterrows():
                if dia == 0:
                    #print("Entra")
                    self.ponteiroum = linha[col]
                    self.ponteirodois = linha[col]
                    dia += 1

                elif linha[col] < self.ponteirodois:
                    #print("Entra")
                    self.ponteirodois = linha[col]
                    flag = True
                    tempo+=1
                elif flag:
                    aux = self.ponteirodois - self.ponteiroum
                    aux = aux / tempo
                    lista.append(aux)
                    flag = False
                    tempo = 1
                    rev+=1
                else:
                    dia = 0
            dic[col] = lista
            reversao[col]=rev
        self.recessao = pd.Series(dic)
        return(reversao, self.recessao)

    def grafico_ascensao(self, posto = 'chesf'):
        if posto == 'chesf':
            r, fig = self.taxas_ascensao('chesf')
        else:
            r, fig = self.taxas_ascensao('ons')

        data = []
        quant = 0
        dicio = {}
        for col in fig.keys():
            if len(fig[col]) > quant:
                quant = len(fig[col])
        for col in fig.keys():
            dicio[col]=fig[col]
        for key in dicio.keys():
            while len(dicio[key]) < quant:
                dicio[key].append(None)

        new_df = pd.DataFrame(dicio)
        for col in new_df.columns:
            data.append(go.Box(y=new_df[col], name=col))
        data.append(go.Scatter(x=new_df.columns, y=new_df.mean(skipna=True), mode='lines', name='média'))

        layout = go.Layout(
        title='Box plot por ano hidrológico da taxa de recessao %s'%posto,
        yaxis=dict(title='taxa [m³/dia]')
        )

        fig = go.Figure(data=data, layout=layout)
        plotly.offline.plot(fig, filename='box plot taxa de ascensao %s'%posto)

    def grafico_recessao(self, posto = 'chesf'):
        if posto == 'chesf':
            r, fig = self.taxas_recessao('chesf')
        else:
            r, fig = self.taxas_recessao('ons')

        data = []
        quant = 0
        dicio = {}
        for col in fig.keys():
            if len(fig[col]) > quant:
                quant = len(fig[col])
        for col in fig.keys():
            dicio[col]=fig[col]
        for key in dicio.keys():
            while len(dicio[key]) < quant:
                dicio[key].append(None)

        new_df = pd.DataFrame(dicio)
        for col in new_df.columns:
            data.append(go.Box(y=new_df[col], name=col))
        data.append(go.Scatter(x=new_df.columns, y=new_df.mean(skipna=True), mode='lines', name='média'))

        layout = go.Layout(
        title='Box plot por ano hidrológico da taxa de recessao %s'%posto,
        yaxis=dict(title='taxa [m³/dia]')
        )

        fig = go.Figure(data=data, layout=layout)
        plotly.offline.plot(fig, filename='box plot taxa de recessao %s'%posto)

    def grafico_reversao(self, posto='chesf'):
        if posto == 'chesf':
            revum, fig = self.taxas_ascensao('chesf')
            revdois, fig2 = self.taxas_recessao('chesf')
        else:
            revum, fig = self.taxas_ascensao('ons')
            revdois, fig = self.taxas_recessao('ons')

        new_rev = {'quantidade':[]}
        revtoasc = {'quantidade':[]}
        revtorec = {'quantidade':[]}
        for i in revum.keys():
            new_rev['quantidade'].append(revum[i]+revdois[i])
            revtoasc['quantidade'].append(revdois[i])
            revtorec['quantidade'].append(revum[i])
        new_rev = pd.DataFrame(new_rev)
        revtoasc = pd.DataFrame(revtoasc)
        revtorec = pd.DataFrame(revtorec)
        layout = go.Layout(
        title='Numero de reversões por ano hidrologico da %s'%posto,
        )
        data = [go.Scatter(y=new_rev['quantidade'], name='nº de reversões totais', mode='lines+markers'),
        go.Scatter(y=revtoasc['quantidade'], name='reversões para ascensão', mode='lines+markers'),
        go.Scatter(y=revtorec['quantidade'], name='reversões para recessao', mode='lines+markers')]
        fig = go.Figure(data=data, layout=layout)
        plotly.offline.plot(fig, filename='Numero de reversões %s'%posto)
