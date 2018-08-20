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

                    aux = self.ponteirodois - self.ponteiroum
                    aux = aux / 2
                    lista.append(aux)
                    self.ponteiroum = linha[col]

                else:
                    dia = 0
            dic[col] = lista
            reversao[col]=rev
        self.ascensao = pd.Series(dic)
        return(self.ascensao)

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

                    aux = self.ponteirodois - self.ponteiroum
                    aux = aux / 2
                    lista.append(aux)
                    self.ponteiroum = linha[col]
                else:
                    dia = 0
            dic[col] = lista
            reversao[col]=rev
        self.recessao = pd.Series(dic)
        return(self.recessao)

    def numero_reversao(self, posto='chesf'):
        if posto == 'chesf':
            fig = self.chesf
        else:
            fig = self.ons

        reversao = {}
        reversao['quantidade'] = []
        for col in fig.columns:
            dia = 0
            contagem = 0
            for index, linha in fig.iterrows():
                if dia == 0:
                    self.ponteiroum = linha[col]
                    dia+=1
                elif dia == 1:
                    self.ponteirodois = linha[col]
                    aux = self.ponteirodois - self.ponteiroum
                    self.ponteiroum = linha[col]
                    dia+=1
                    if aux>0:
                        flag = True
                    else:
                        flag = False
                else:
                    if flag:
                        self.ponteirodois = linha[col]
                        aux = self.ponteirodois - self.ponteiroum
                        self.ponteiroum = linha[col]
                        if aux < 0:
                            contagem+=1
                            flag = False
                    else:
                        self.ponteirodois = linha[col]
                        aux = self.ponteirodois - self.ponteiroum
                        self.ponteiroum = linha[col]
                        if aux > 0:
                            contagem+=1
                            flag = True
            reversao['quantidade'].append(contagem)
        self.reversao = pd.DataFrame(reversao)
        return (self.reversao)


    def grafico_ascensao(self, posto = 'chesf'):
        if posto == 'chesf':
            fig = self.taxas_ascensao('chesf')
        else:
            fig = self.taxas_ascensao('ons')

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
        title='Box plot por ano hidrológico da taxa de ascensão %s'%posto,
        yaxis=dict(title='taxa [m³/s]')
        )

        fig = go.Figure(data=data, layout=layout)
        plotly.offline.plot(fig, filename='box plot taxa de ascensao %s'%posto)

    def grafico_recessao(self, posto = 'chesf'):
        if posto == 'chesf':
            fig = self.taxas_recessao('chesf')
        else:
            fig = self.taxas_recessao('ons')

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
        yaxis=dict(title='taxa [m³/s]')
        )

        fig = go.Figure(data=data, layout=layout)
        plotly.offline.plot(fig, filename='box plot taxa de recessao %s'%posto)


    def grafico_reversao(self, posto='chesf'):
        if posto == 'chesf':
            fig = self.numero_reversao('chesf')
        else:
            fig = self.numero_reversao('ons')

        layout = go.Layout(
        title='Numero de reversões por ano hidrologico da %s'%posto,
        yaxis= dict(title= 'numero de reversões',range = [0,230]),
        )
        dados = []


        data = [go.Scatter(y=fig['quantidade'], name='nº de reversões totais', mode='lines+markers')]
        fig = go.Figure(data=data, layout=layout)
        plotly.offline.plot(fig, filename='Numero de reversões %s'%posto)
