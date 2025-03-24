import streamlit as st
import requests 
import pandas as pd
import plotly.express as px

def formata_numero(valor,prefixo=''):
    for unidade in ['','mil']:
        if valor<1000:
            return f'{prefixo} {valor:.2f} {unidade}'
        valor /=1000
    return f'{prefixo} {valor:.2f} milhões'

st.title('DASHBOARD DE VENDAS :car:')

arquivo_csv='car_ad.csv'
dados = pd.read_csv(arquivo_csv, encoding="latin1")  

#criando colunas
coluna1,coluna2=st.columns(2)
with coluna1:
    st.metric('Receita',formata_numero(dados['price'].sum()))
with coluna2:
    st.metric('Quantidade de vendas',formata_numero(dados.shape[0]))

st.dataframe(dados)


