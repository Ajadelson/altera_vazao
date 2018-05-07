import pandas as pd
import cufflinks as cf
from plotly.offline import iplot
from dadoframe import chesf_dataframe, ons_dataframe

class Base():
    """seleção de dados por ano hidrologico e vazão limite."""

    def __init__(self, nome_arquivo = 'padrao'):
        """Inicializa os atributos."""
        self.arquivo = nome_arquivo
        self.chesf = chesf_dataframe()
        self.ons = ons_dataframe()
