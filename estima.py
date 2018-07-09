import pandas as pd
import plotly.plotly as py
import plotly
import plotly.tools as tls
import numpy as np

from plotly.graph_objs import *
from datetime import date, timedelta
from dadoframe import chesf_dataframe, ons_dataframe, uni

class Stats():
    """Caracteriza as alterações de cheias anuais quanto à
    frequencia, duração e periodo de ocorrência."""

    def __init__(self):
        """inicia os atributos"""
        self.chesf = chesf_dataframe()
        self.ons = ons_dataframe()
        self.result = uni()

        self.ons_anual = []

        
