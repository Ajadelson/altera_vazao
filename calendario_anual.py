from dadoframe import *

def transform(dp):
    ano = 0
    new = {0:[]}
    year = dp[dp.index==0].Dia.item().year
    for index, i in dp.iterrows():
        if i.Dia == date(year,9,2):
            ano += 1
            year +=1
            new[ano] = []
        new[ano].append(i.Vazao)

    for col in new.keys():
        while len(new[col])<366:
            new[col].append(None)
    del new[0]
    del new[col]
    new_df = pd.DataFrame(new)
    return(new_df)
