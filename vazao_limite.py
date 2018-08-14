import pandas as pd
#import cufflinks as cf
import plotly.plotly as py
import plotly
import plotly.tools as tls
from plotly.graph_objs import *
import numpy as np
#from plotly.offline import iplot
from datetime import date, timedelta
from dadoframe import chesf_dataframe, ons_dataframe, uni

#cf.set_config_file(offline=True)

class Base():
    """seleção de dados por ano hidrologico e vazão limite."""

    def __init__(self, nome_arquivo = 'padrao'):
        """Inicializa os atributos."""
        self.arquivo = nome_arquivo
        self.chesf = chesf_dataframe()
        self.ons = ons_dataframe()
        self.result = uni()

    def grafico(self, nivel_ons=None, nivel_chesf=None):
        """Plota os graficos """
        #cf.go_offline()
        if nivel_ons == None:
            quartil_ons = np.percentile(self.ons['Vazao'], 75)
        else:
            quartil_ons = nivel_ons
        if nivel_chesf == None:
            quartil_chesf = np.percentile(self.chesf['Vazao'], 75)

        else:
            quartil_chesf = nivel_chesf
        lin_quartil_ons = Scatter(x=self.result['Dia'],
        y=[quartil_ons for h in self.result.iterrows()], name='Cheia ONS')

        lin_quartil_chesf = Scatter(x=self.chesf['Dia'],
        y=[quartil_chesf for h in self.chesf.iterrows()], name='Cheia CHESF')

        ons = Scatter(x=self.result['Dia'], y=self.result['ONS'],
        name='Dados ONS')

        chesf = Scatter(x=self.result['Dia'], y=self.result['CHESF'],
        name='Dados CHESF')

        data = Data([ons, chesf, lin_quartil_ons, lin_quartil_chesf])
        layout = dict(title='Vazão limite', xaxis=dict(title='Dias'),
        yaxis=dict(title='Vazão [m³/dia]'))

        plotly.offline.plot(dict(data=data, layout=layout), filename='grafico com nivel')
        #self.result.iplot(kind='spread')
