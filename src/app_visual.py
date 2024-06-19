import pandas as pd

def calc_avg_spend_from_period(df):
    spend = df.groupby('ano_mes')['Valor'].mean().mean()
    return f"R$ {round(spend)}"


def biggest_spenders_per_type(dataset):
    mais_gastou_por_tipo = dict()
    tmp = dataset.groupby(['nome', 'tipoDespesa'])['Valor'].sum().reset_index().copy()
    for tipo, tmpdf in tmp.groupby('tipoDespesa'):
        result_tipo = tmpdf.loc[tmpdf['Valor']==tmpdf['Valor'].max(), :].copy()
        mais_gastou_por_tipo[tipo] = dict(Deputado=result_tipo['nome'].values[0], 
                                            Valor = result_tipo['Valor'].values[0])

    mais_gastou_por_tipo = pd.DataFrame(mais_gastou_por_tipo).T.sort_values('Valor', ascending=False)
    mais_gastou_por_tipo['Valor'] = mais_gastou_por_tipo['Valor'].apply(lambda x: round(x))
    return mais_gastou_por_tipo