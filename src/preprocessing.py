import pandas as pd

def process_deputados():
    from src.io import read_json
    import os

    deputados_raw = read_json(domain='raw', source_name='deputados')
    deputados = pd.json_normalize(deputados_raw['dados'])
    deputados = deputados.loc[deputados['siglaUf']=='ES'] # TEMP
    deputados['id'] = deputados['id'].astype(str)
    deputados.set_index('id', inplace=True)

    from src.utils import ensure_folder_exists
    folder_path = os.path.join('data','cleansed')
    file_name = 'deputados.parquet'
    ensure_folder_exists(folder_path)

    deputados.to_parquet(os.path.join(folder_path, file_name)) #TODO path in config, function to save and ensure folder exists





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
    # despesas['id_deputado'] = despesas['id_deputado'].astype(int)
    despesas[['codDocumento', 'numDocumento', 'cnpjCpfFornecedor', 'codLote']] = despesas[['codDocumento', 'numDocumento', 'cnpjCpfFornecedor', 'codLote']].astype(str)
    despesas.sort_values('dataDocumento', inplace=True)
    despesas.reset_index(drop=True, inplace=True)
    despesas['ano_mes'] = despesas.apply(lambda row: f"{row['ano']}_{str(row['mes']).zfill(2)}", axis=1)

    from src.utils import ensure_folder_exists
    folder_path = os.path.join('data','cleansed')
    file_name = 'despesas.parquet'
    ensure_folder_exists(folder_path)

    despesas.to_parquet(os.path.join(folder_path, file_name)) #TODO path in config, function to save and ensure folder exists



def process_gold_table():
    import os
    deputados = pd.read_parquet('data/cleansed/deputados.parquet')
    despesas = pd.read_parquet('data/cleansed/despesas.parquet')

    df = pd.merge(despesas, deputados, how='left', left_on='id_deputado', right_index=True)
    df['Valor'] = df['valorLiquido'].clip(lower=0)
    print(f"Table 'master_table' shape: {df.shape}")

    from src.utils import ensure_folder_exists
    folder_path = os.path.join('data','gold')
    file_name = 'master_table.parquet'
    ensure_folder_exists(folder_path)
    
    df.to_parquet(os.path.join(folder_path, file_name)) #TODO path in config



def process_gold_monthly_data():
    import os
    df = pd.read_parquet('data/gold/master_table.parquet')
    
    group_mes = df.groupby(['ano_mes', 'id_deputado'])
    df_mes = group_mes[['Valor']].sum()
    df_mes['Deputado'] = group_mes['nome'].max()
    df_mes.reset_index(inplace=True)
    
    print(f"Table 'monthly_data' shape: {df.shape}")

    from src.utils import ensure_folder_exists
    folder_path = os.path.join('data','gold')
    file_name = 'monthly_data.parquet'
    ensure_folder_exists(folder_path)

    df_mes.to_parquet(os.path.join(folder_path, file_name)) #TODO path in config