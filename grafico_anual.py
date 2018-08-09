import pandas as pd
import plotly.plotly as py
import plotly
import plotly.tools as tls
import cufflinks as cf
from plotly.graph_objs import *
from datetime import date, timedelta
from dadoframe import chesf_dataframe, ons_dataframe, uni

class Grafics():
    """Plotando os graficos"""

    def __init__(self):
        self.chesf = chesf_dataframe()
        self.ons = ons_dataframe()

    def hidr_anual_chesf(self):
        anoinicio = self.chesf[self.chesf.index==0].Dia.item().year
        anofinal = self.chesf["Dia"][self.chesf.index[-1]].year +1

        self.chesf["ano"] = self.chesf["Dia"].values
        self.reorg={}
        for index, i in self.chesf.iterrows():
            i['ano']=i.Dia.year

            try:
                self.reorg[i.ano].append(i.Vazao)
            except:
                self.reorg[i.ano]=[i.Vazao]

        for col in self.reorg.keys():
            while len(self.reorg[col])<366:
                self.reorg[col].append(None)
        self.reor=pd.DataFrame(self.reorg)
        plotly.offline.plot([{
        'y':self.reor[ano],
        'name' : ano,
        } for ano in self.reor.columns])

    def hidr_anual_ons(self):
        anoinicio = self.ons[self.ons.index==0].Dia.item().year
        anofinal = self.ons["Dia"][self.ons.index[-1]].year +1

        self.ons["ano"] = self.ons["Dia"].values
        self.reorg={}
        for index, i in self.ons.iterrows():
            i['ano']=i.Dia.year

            try:
                self.reorg[i.ano].append(i.Vazao)
            except:
                self.reorg[i.ano]=[i.Vazao]

        for col in self.reorg.keys():
            while len(self.reorg[col])<366:
                self.reorg[col].append(None)
        self.reor=pd.DataFrame(self.reorg)
        plotly.offline.plot([{
        'y':self.reor[ano],
        'name' : ano,
        } for ano in self.reor.columns])
