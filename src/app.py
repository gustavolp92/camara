import streamlit as st
st.set_page_config(layout="wide")

import os
import pandas as pd
import plotly.express as px
from app_visual import (calc_avg_spend_from_period, biggest_spenders_per_type,
                        table_info_deputado)

# RETRIEVE DATA
df = pd.read_parquet(os.path.join('data','gold','master_table.parquet'))
df_mes = pd.read_parquet(os.path.join('data','gold','monthly_data.parquet'))

cols = ['ano_mes', 'nome', 'Valor', 'siglaPartido', 'tipoDespesa', 'dataDocumento', 'nomeFornecedor', 'cnpjCpfFornecedor', 'codDocumento', 'email', 'siglaUf', 'urlDocumento']

tipo_despesa_simplificado = {
        'COMBUSTÍVEIS E LUBRIFICANTES.': 'Combustíveis e lubrif.',
        'TELEFONIA': 'Telefonia',
        'LOCAÇÃO OU FRETAMENTO DE VEÍCULOS AUTOMOTORES': 'Locação de veículos',
        'PASSAGEM AÉREA - SIGEPA': 'Passagem Aérea (SIGEPA)',
        'MANUTENÇÃO DE ESCRITÓRIO DE APOIO À ATIVIDADE PARLAMENTAR': 'Manutenção de escritório',
        'PASSAGEM AÉREA - RPA': 'Passagem Aérea (RPA)',
        'SERVIÇO DE TÁXI, PEDÁGIO E ESTACIONAMENTO': 'Taxi, pedágio, estacion.',
        'HOSPEDAGEM ,EXCETO DO PARLAMENTAR NO DISTRITO FEDERAL.': 'Hospedagem (exceto DF)',
        'FORNECIMENTO DE ALIMENTAÇÃO DO PARLAMENTAR': 'Alimentação',
        'PASSAGEM AÉREA - REEMBOLSO': 'Passagem Aérea Reembolso',
        'DIVULGAÇÃO DA ATIVIDADE PARLAMENTAR.': 'Divulgação',
        'ASSINATURA DE PUBLICAÇÕES': 'Assinatura publicações'
    }


# DEFINE FILTER OPTIONS IN SIDEBAR
filter_deputado = st.sidebar.selectbox('Deputado', [None] + list(df['nome'].unique()))
filter_type_spend = st.sidebar.selectbox('Tipo de gasto', [None] + list(df['tipoDespesa'].unique()))

period_list = list(df['ano_mes'].unique())
period_list.sort(reverse=True)
period = st.sidebar.multiselect('Period', period_list, default=[period_list[0]])


# APPLY FILTERS
df_filt = df.copy()
df_mes_filt = df_mes.copy()
if filter_type_spend:
    df_filt = df_filt.loc[df_filt['tipoDespesa']==filter_type_spend].copy()
if period:
    df_filt = df_filt.loc[df_filt['ano_mes'].isin(period)].copy()
    df_mes_filt = df_mes_filt.loc[df_mes_filt['ano_mes'].isin(period)].copy()
if filter_deputado:
    df_filt = df_filt.loc[df_filt['nome']==filter_deputado].copy()
    df_mes_filt = df_mes_filt.loc[df_mes_filt['Deputado']==filter_deputado].copy()
    df_filt_dep=df_filt.copy()  #deputado filtrado OU de maior gasto
else:
    deputado_maior_gasto = df_mes_filt.groupby('Deputado')['Valor'].sum().idxmax()
    df_filt_dep = df_filt.loc[df_filt['nome']==deputado_maior_gasto].copy()


# TITLE
st.title('Despesas - Câmara dos Deputados')
st.write('**Análise de cota parlamentar dos Deputados Federais**')

# DISPLAY 1st row
with st.container():
    page_col = st.columns([0.65,0.35])
    
    ### LEFT SIDE ###
    page_col[0].metric(label="**Gasto médio mensal por deputado**", value=calc_avg_spend_from_period(df_mes_filt))

    fig = px.bar(df_filt, x='nome', y='Valor', color=df_filt['tipoDespesa'].map(tipo_despesa_simplificado), hover_data=['tipoDespesa'],
                title='Despesas por deputado e tipo')
    fig.update_layout(legend=dict(title_text='Tipo de despesa'))
    page_col[0].plotly_chart(fig)


    ### RIGHT SIDE ###
    # INFO FOR SPECIFIC 'DEPUTADO'
    info_dep, foto_dep = table_info_deputado(df_filt_dep, tipo_despesa_simplificado)
    page_col[1].write(f"**{df_filt_dep['nome'].unique()[0]}**")
    page_col[1].image(foto_dep, width=100, caption=f"Total gasto: R${round(df_filt_dep['Valor'].sum())}")
    page_col[1].dataframe(info_dep)


# DISPLAY 2nd row
with st.container():
    page_col = st.columns([0.65,0.35])

    fig = px.line(df_mes, x='ano_mes', y='Valor', color='Deputado', markers=True, title = 'Histórico de Gastos Mensais por Deputado')
    page_col[0].plotly_chart(fig)

    
    biggest_spenders = biggest_spenders_per_type(df_filt)
    biggest_spenders.index = biggest_spenders.index.map(tipo_despesa_simplificado)
    page_col[1].write("**Maior Gasto por Categoria no período**")
    page_col[1].dataframe(biggest_spenders)


# DISPLAY 3rd row
st.write('**Tabela de despesas**')
st.dataframe(df_filt[cols].head(100), hide_index=True, height=300)
