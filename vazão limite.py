import pandas as pd
from dadoframe import retorna_dataframe

class Base():
    """seleção de dados por ano hidrologico e vazão limite."""

    def __init__(self, nome_arquivo):
        """Inicializa os atributos."""
        self.arquivo = arquivo

        if self.arquivo.upper() == 'CHESF':
            self.df = retorna_dataframe()
        
