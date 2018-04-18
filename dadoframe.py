import xlrd
import pandas as pd
from datetime import date

def xlread(arq_xls):
	"""Função que ler arquivos .xls"""
	xls = xlrd.open_workbook(arq_xls)
	plan = xls.sheets()[0]

	for i in range(plan.nrows):
		yield plan.row_values(i)

def retorna_dataframe():
	aux=''
	arq="defluencia_db.xls"
	data=[]
	dado=[]
	for linha in xlread(arq):
		if linha[1]!=aux:
			d=1
			org=linha[1].split("/")
			x=date(int(org[1]), int(org[0]), d)
			data.append(x.strftime("%d/%m/%Y"))
			aux=linha[1]
			dado.append(linha[2])

		else:
			if linha[2]=='':
				d+=1
				org=linha[1].split("/")
				x=date(int(org[1]), int(org[0]), d)
				data.append(x.strftime("%d/%m/%Y"))
				dado.append(None)

			else:
				d+=1
				org=linha[1].split("/")
				x=date(int(org[1]), int(org[0]), d)
				data.append(x.strftime("%d/%m/%Y"))
				dado.append(linha[2])
	dicio = {'Dia' : data, 'Vazao' : dado}
	df = pd.DataFrame(dicio)
	return df

#main
#print(retorna_dataframe())
