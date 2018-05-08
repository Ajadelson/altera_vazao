import xlrd
import pandas as pd
from datetime import date, timedelta

def xlread(arq_xls):
	"""Função que ler arquivos .xls"""
	xls = xlrd.open_workbook(arq_xls)
	plan = xls.sheets()[0]

	for i in range(plan.nrows):
		yield plan.row_values(i)

def ons_dataframe():
	arq = "Vazões_Diárias_1931_2015.xls"
	data = []
	dado = []
	flag = False
	for linha in xlread(arq):
		if linha[0] == '1/jan/1931':
			flag = True
			x = date(1931,1,1)
		if flag:
			data.append(x)
			x = x + timedelta(days=1)
			dado.append(linha[150])
	dicio = {"Dia" : data, "Vazao" : dado}
	df = pd.DataFrame(dicio)
	#df=df.set_index('Dia')
	return df

def chesf_dataframe():
	aux=''
	arq="defluencia_db.xls"
	data=[]
	dado=[]
	for linha in xlread(arq):
		if linha[1]!=aux:
			d=1
			org=linha[1].split("/")
			x=date(int(org[1]), int(org[0]), d)
			data.append(x)
			aux=linha[1]
			dado.append(linha[2])

		else:
			if linha[2]=='':
				d+=1
				org=linha[1].split("/")
				x=date(int(org[1]), int(org[0]), d)
				data.append(x)
				dado.append(None)

			else:
				d+=1
				org=linha[1].split("/")
				x=date(int(org[1]), int(org[0]), d)
				data.append(x)
				dado.append(linha[2])
	dicio = {'Dia' : data, 'Vazao' : dado}
	df = pd.DataFrame(dicio)
	#df=df.set_index('Dia')
	return df

def uni():
	arq = "Vazões_Diárias_1931_2015.xls"
	data = []
	dado = []
	dado2 = []
	flag = False
	flag2 = False
	df_chesf = chesf_dataframe()
	x = None
	for linha in xlread(arq):
		if linha[0] == '1/jan/1931':
			flag = True
			x = date(1931,1,1)
		if x == date(1995, 1, 1):
			flag2 = True
		if flag:
			data.append(x)
			x = x + timedelta(days=1)
			dado.append(linha[150])
			if flag2 == True:
				try:
					dado2.append(df_chesf[df_chesf['Dia'] == x].iloc[0]['Vazao'])
				except:
					dado2.append(None)
			else:
				dado2.append(None)
	dicio = {'Dia': data, 'ONS': dado, 'CHESF': dado2}
	df = pd.DataFrame(dicio)
	#df = df.set_index('Dia')
	return df



#main
#print(retorna_dataframe())
