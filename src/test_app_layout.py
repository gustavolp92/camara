import streamlit as st
st.set_page_config(layout="wide")


import streamlit as st

# Funções para cada página
def home():
    st.title("Página Inicial")
    st.write("Bem-vindo à Página Inicial!")

    # Filtros no painel lateral
    st.sidebar.title("Filtros")
    option = st.sidebar.selectbox(
        'Escolha uma opção',
        ('Opção 1', 'Opção 2', 'Opção 3')
    )
    
    slider_value = st.sidebar.slider(
        'Escolha um valor',
        0, 100, 50
    )

    multiselect_values = st.sidebar.multiselect(
        'Escolha múltiplas opções',
        ['Opção A', 'Opção B', 'Opção C']
    )


def page1():
    st.title("Página 1")
    st.write("Conteúdo da Página 1")

    # Filtros no painel lateral
    st.sidebar.title("Filtros")
    option = st.sidebar.selectbox(
        'Escolha uma opção',
        ('Opção 1', 'Opção 2', 'Opção 3')
    )
    slider_value = st.sidebar.slider(
        'Escolha um valor',
        0, 100, 50
    )
    
    # Criando duas abas
    tab1, tab2 = st.tabs(["Aba 1", "Aba 2"])

    with tab1:
        st.header("Conteúdo da Aba 1")
        st.write("Aqui está o conteúdo da Aba 1")

    with tab2:
        st.header("Conteúdo da Aba 2")
        st.write("Aqui está o conteúdo da Aba 2")


def page2():
    import plotly.express as px
    import numpy as np

    st.title("Página 2")
    st.write("Conteúdo da Página 2")

    # Exemplo de gráfico
    x = np.linspace(0, 10, 100)
    y = np.sin(x)
    fig = px.bar(x=x, y=y)
    st.plotly_chart(fig)


# Sidebar para navegação
st.sidebar.title("Navegação")
selection = st.sidebar.radio("Ir para:", ["Página Inicial", "Página 1", "Página 2"])

# Lógica para exibir a página selecionada
if selection == "Página Inicial":
    home()
elif selection == "Página 1":
    page1()
elif selection == "Página 2":
    page2()
