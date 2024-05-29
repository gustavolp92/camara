import streamlit as st
import pandas as pd

# Title of the app
st.title('First App')


# Read data
deputados = pd.read_parquet('data/cleansed/deputados.parquet')
despesas = pd.read_parquet('data/cleansed/despesas.parquet')
df = pd.merge(despesas, deputados, how='left', left_on='id_deputado', right_index=True)
st.dataframe(df.head(100))  # Interactive table


# Text input
name = st.text_input('Enter your name')

# Number input
age = st.number_input('Enter your age', min_value=0, max_value=100)

# Button
if st.button('Submit'):
    if name and age:
        st.write(f'Hello {name}, you are {age} years old.')
    else:
        st.write('Please enter both your name and age.')
