import pandas as pd
import plotly.plotly as py
import plotly
import plotly.tools as tls
import cufflinks as cf
import plotly.graph_objs as go
from plotly.graph_objs import *
from datetime import date, timedelta
from calendario_anual import *
from dadoframe import chesf_dataframe, ons_dataframe, uni

class Grafics():
    """Plotando os graficos"""

    def __init__(self):
        self.chesf = transform(chesf_dataframe())
        self.ons = transform(ons_dataframe())

    def hidr_anual(self, posto='chesf'):
        if posto == 'chesf':
            self.dp = self.chesf
        else:
            self.dp = self.ons

        x = [date(2007,9,2)+timedelta(days=i) for i in self.dp.index]
        #print(x)
        x = [i.strftime("%d %b") for i in x]

        #self.dp = pd.DataFrame(self.dp, index=x)
        layout = go.Layout(title="Hidrograma %s"%posto,
        yaxis=dict(title='Vazão [m³/s]', range=[0, 19000]), showlegend=False)
        data=[]

        for ano in self.dp.columns:
            data.append(go.Scatter(x=x,y=self.dp[ano],name=ano,
            marker=dict(cmax=len(self.dp.columns),cmin=0, size=5, color=[ano]*366,
            colorbar=dict(title='Anos'),
            colorscale='Jet'), mode='markers'))
        fig = go.Figure(data=data, layout=layout)
        plotly.offline.plot(fig, filename='hidrogama %s'%posto)


    def max_anual(self, posto='ons'):
        """Grafico da Serie de Maximas"""
        #df_max = pd.DataFrame()
        if posto=='ons':
            self.max = self.ons
        else:
            self.max = self.chesf
        ano=[]
        valor=[]
        for i in self.max.columns:
            x = self.max[i].max().item()
            ano.append(i)
            valor.append(x)
        maxi={"ano":ano, "valor":valor}
        maxi=pd.DataFrame(maxi)
        layout = go.Layout(title='Maxima anual %s' %posto,
        yaxis=dict(title='Vazão [m³/s]'),
        xaxis=dict(title='Ano hidrológico'))
        data = [go.Scatter(x=maxi["ano"], y=maxi['valor'], mode='lines', name='max')]
        fig = go.Figure(data=data, layout=layout)
        plotly.offline.plot(fig, filename='grafico de max %s'%posto)
