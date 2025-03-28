import streamlit as st
import pandas as pd
import requests
import numpy as np
import time

@st.cache_data
def converter_csv(df):
    return df.to_csv(index=False).encode('utf-8')

def mensagem_concluido():
    sucesso=st.success('Arquivo salvo com sucesso!',icon='✅')
    time.sleep(4)
    sucesso.empty()

st.title('dados  Brutos')

arquivo_csv = 'dados_filtrados_temp.csv' 
dados_filtrados = pd.read_csv(arquivo_csv,encoding='utf-8')

np.random.seed(42)  
num_linhas = dados_filtrados.shape[0]

datas_iniciais = pd.Timestamp("2020-01-01")
datas_finais = pd.Timestamp("2024-12-31")

dados_filtrados["data da compra"] = pd.to_datetime(
    np.random.randint(datas_iniciais.timestamp(), datas_finais.timestamp(), num_linhas), unit="s"
)
dados_filtrados['Ano de compra'] = dados_filtrados['data da compra'].dt.year
dados_filtrados["engV"] = dados_filtrados["engV"].fillna(0)

with st.expander('Colunas'):
    colunas = st.multiselect('Selecione as colunas',list(dados_filtrados.columns),list(dados_filtrados.columns))

st.sidebar.title('Filtros')

with st.sidebar.expander('Nome da marca de carro'):
    produtos=st.multiselect('Selecione as marcas de carro',dados_filtrados['car'].unique(),dados_filtrados['car'].unique())

with st.sidebar.expander('Preço do produto'):
    preco=st.slider('Selecione o preço',0,100000,(0,100000))

with st.sidebar.expander('Data de compra'):
    data_compra = st.date_input('Selecione a data', 
                                (dados_filtrados["data da compra"].min(),
                                 dados_filtrados["data da compra"].max()),
                                key="data_compra")
with st.sidebar.expander('body'):
    body=st.multiselect('Selecione o tipo de carro',dados_filtrados['body'].unique(),dados_filtrados['body'].unique())

with st.sidebar.expander('mileage'):
    mileage=st.slider('Selecione a kilometragem',0,10000,(0,10000)) 

with st.sidebar.expander('engType'):
    engType=st.multiselect('Selecione o tipo de motor',dados_filtrados['engType'].unique(),dados_filtrados['engType'].unique())

with st.sidebar.expander('engV'):
    engV=st.slider('Selecione o tamanho do motor',0,10,(0,10))

with st.sidebar.expander('registration'):
    registration=st.multiselect('Selecione o tipo de registro',dados_filtrados['registration'].unique(),dados_filtrados['registration'].unique())
with st.sidebar.expander('year'):
    ano = st.slider('Selecione o ano', 
                    int(dados_filtrados['year'].min()), 
                    int(dados_filtrados['year'].max()), 
                    (int(dados_filtrados['year'].min()), int(dados_filtrados['year'].max())),
                    key="ano")

with st.sidebar.expander('model'):
    model=st.multiselect('Selecione o modelo',dados_filtrados['model'].unique(),dados_filtrados['model'].unique())

with st.sidebar.expander('drive'):
    drive=st.multiselect('Selecione o tipo de tração',dados_filtrados['drive'].unique(),dados_filtrados['drive'].unique())
with st.sidebar.expander('local da compra'):
    local = st.multiselect('Selecione o local da compra', 
                           dados_filtrados['local da compra'].unique(), 
                           dados_filtrados['local da compra'].unique())
with st.sidebar.expander('regioes'):
    regioes = st.multiselect('Selecione a região', 
                             dados_filtrados['regioes'].unique(), 
                             dados_filtrados['regioes'].unique())

#Fazendo a filtragem 
dados_filtrados = dados_filtrados[
    (dados_filtrados['car'].isin(produtos)) &
    (dados_filtrados['price'] >= preco[0]) &
    (dados_filtrados['price'] <= preco[1]) &
    (dados_filtrados['data da compra'] >= pd.to_datetime(data_compra[0])) &
    (dados_filtrados['data da compra'] <= pd.to_datetime(data_compra[1])) &
    (dados_filtrados['body'].isin(body)) &
    (dados_filtrados['mileage'] >= mileage[0]) &
    (dados_filtrados['mileage'] <= mileage[1]) &
    (dados_filtrados['engType'].isin(engType)) &
    (dados_filtrados['engV'] >= engV[0]) &
    (dados_filtrados['engV'] <= engV[1]) &
    (dados_filtrados['registration'].isin(registration)) &
    (dados_filtrados['year'] >= ano[0]) &
    (dados_filtrados['year'] <= ano[1]) &
    (dados_filtrados['model'].isin(model)) &
    (dados_filtrados['drive'].isin(drive)) &
    (dados_filtrados['local da compra'].isin(local)&
     (dados_filtrados['regioes'].isin(regioes)))
]

dados_filtrados = dados_filtrados[colunas]

st.dataframe(dados_filtrados)

st.markdown(f'A tabela possui :blue[{dados_filtrados.shape[0]}] linhas e :blue[{dados_filtrados.shape[1]}] colunas')

st.markdown('Como deseja que seja o nome desse arquivo')

col1,col2=st.columns(2)
with col1:
    nome_arquivo=st.text_input('',label_visibility='collapsed',value='dados_filtrados.csv')
    nome_arquivo+='.csv'

with col2:
    botao=st.download_button(
        label='Baixar arquivo',
        data=converter_csv(dados_filtrados),
        file_name=nome_arquivo,
        mime='text/csv',
        help='Clique para baixar o arquivo'
    )