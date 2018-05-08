import pandas as pd
#import cufflinks as cf
import plotly.plotly as py
import plotly
import plotly.tools as tls
from plotly.graph_objs import *
import numpy as np
from datetime import date, timedelta
from dadoframe import chesf_dataframe, ons_dataframe, uni

class Base():
    """seleção de dados por ano hidrologico e vazão limite."""

    def __init__(self, nome_arquivo = 'padrao'):
        """Inicializa os atributos."""
        self.arquivo = nome_arquivo
        self.chesf = chesf_dataframe()
        self.ons = ons_dataframe()
        self.result = uni()


    def grafico(self):
        """Plota os graficos """
        #cf.go_offline()
        quartil_ons = np.percentile(self.ons['Vazao'], 75)
        quartil_chesf = np.percentile(self.chesf['Vazao'], 75)
        ons = Scatter(x=self.result['Dia'], y=self.result['ONS'])
        chesf = Scatter(x=self.result['Dia'], y=self.result['CHESF'])
        data = Data([ons, chesf])
        plotly.offline.plot(data)
        #self.result.plot(kind='scatter')
