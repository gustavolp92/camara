import pandas as pd

def process_deputados():
    from src.io import read_json
    deputados_raw = read_json(domain='raw', source_name='deputados')
    deputados = pd.json_normalize(deputados_raw['dados'])
    deputados = deputados.loc[deputados['siglaUf']=='ES'] # TEMP
    deputados.set_index('id', inplace=True)
    deputados.to_parquet('data/cleansed/deputados.parquet') #TODO put in config




def process_despesas():
    import json
    import glob
    import os
    dfs = []
    for path_deputado in glob.glob(os.path.join("data","raw","despesas", "*")):
        id_deputado = path_deputado.split("\\")[-1]
        data_deputado = []
        for file_path in glob.glob(os.path.join(path_deputado, "*", "*.json")):
            with open(file_path, "r") as json_file:
                data_deputado.extend(json.load(json_file))
        df_deputado = pd.json_normalize(data_deputado)
        df_deputado['id_deputado'] = id_deputado
        dfs.append(df_deputado)

    despesas = pd.concat(dfs)    
    despesas['dataDocumento'] = pd.to_datetime(despesas['dataDocumento'])
    despesas['id_deputado'] = despesas['id_deputado'].astype(int)
    despesas.sort_values('dataDocumento', inplace=True)
    despesas.reset_index(drop=True, inplace=True)
    despesas['ano_mes'] = despesas.apply(lambda row: f"{row['ano']}_{str(row['mes']).zfill(2)}", axis=1)

    despesas.to_parquet('data/cleansed/despesas.parquet') #TODO path in config
