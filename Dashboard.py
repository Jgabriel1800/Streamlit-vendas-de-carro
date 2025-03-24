import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(layout='wide')

def formata_numero(valor, prefixo=''):
    for unidade in ['', 'mil']:
        if valor < 1000:
            return f'{prefixo} {valor:.2f} {unidade}'
        valor /= 1000
    return f'{prefixo} {valor:.2f} milhões'

st.title('DASHBOARD DE VENDAS 🚗')

arquivo_csv = 'car_ad.csv'
dados = pd.read_csv(arquivo_csv, encoding="latin1")

regioes_eua = {
    "Norte": ["CT", "ME", "MA", "NH", "RI", "VT", "IA", "MI", "MN", "MT", "ND", "SD", "WI"],
    "Sul": ["AL", "AR", "DE", "FL", "GA", "KY", "LA", "MD", "MS", "NC", "OK", "SC", "TN", "TX", "VA", "WV"],
    "Leste": ["NJ", "NY", "PA", "OH", "IN", "IL", "MA", "VT", "NH", "RI", "CT"],
    "Oeste": ["AK", "AZ", "CA", "CO", "HI", "ID", "NM", "NV", "OR", "UT", "WA", "WY"]
}



estados_eua_coords = {
    "AL": (32.806671, -86.791130),
    "AK": (61.370716, -149.493686),
    "AZ": (33.729759, -111.431221),
    "AR": (34.969704, -92.373123),
    "CA": (36.116203, -119.681564),
    "CO": (39.059811, -105.311104),
    "CT": (41.597782, -72.755371),
    "DE": (38.665721, -75.755137),
    "FL": (27.766279, -81.686783),
    "GA": (33.040619, -83.643074),
    "HI": (21.094318, -157.498337),
    "ID": (44.299782, -114.742040),
    "IL": (40.298904, -87.431140),
    "IN": (36.278726, -86.302264),
    "IA": (42.019842, -93.210526),
    "KS": (38.526600, -96.726486),
    "KY": (37.668140, -84.670067),
    "LA": (31.169546, -91.867805),
    "ME": (44.693947, -69.381927),
    "MD": (39.063946, -76.802101),
    "MA": (42.230171, -71.530106),
    "MI": (42.874721, -86.251989),
    "MN": (44.299782, -93.774173),
    "MS": (32.321384, -89.251388),
    "MO": (36.116203, -89.831988),
    "MT": (46.116203, -112.869665),
    "NE": (41.125370, -98.268082),
    "NV": (38.313515, -117.055374),
    "NH": (43.452492, -71.563896),
    "NJ": (40.298904, -74.521011),
    "NM": (34.423698, -106.445356),
    "NY": (40.298904, -74.521011),
    "NC": (35.630066, -79.806419),
    "ND": (47.528912, -99.784012),
    "OH": (40.388783, -82.764915),
    "OK": (36.820746, -95.929594),
    "OR": (33.004106, -116.418468),
    "PA": (40.590752, -77.209755),
    "RI": (41.680893, -71.511780),
    "SC": (33.856892, -80.945007),
    "SD": (44.299782, -99.438828),
    "TN": (35.747845, -86.692345),
    "TX": (31.054487, -97.563461),
    "UT": (40.150032, -111.862434),
    "VT": (44.045876, -72.710686),
    "VA": (38.003385, -79.458786),
    "WA": (47.731157, -120.805472),
    "WV": (38.491226, -80.954522),
    "WI": (43.351915, -88.825217),
    "WY": (42.755966, -107.302490)
}
np.random.seed(42)  
num_linhas = dados.shape[0]
dados["local da compra"] = np.random.choice(list(estados_eua_coords.keys()), num_linhas)
np.random.seed(42)  
num_linhas = dados.shape[0]

def get_regiao(estado):
    for regiao, estados in regioes_eua.items():
        if estado in estados:
            return regiao
    return "Desconhecido"

dados["regioes"] = dados["local da compra"].apply(get_regiao)

dados["Latitude"] = dados["local da compra"].map(lambda estado: estados_eua_coords[estado][0])
dados["Longitude"] = dados["local da compra"].map(lambda estado: estados_eua_coords[estado][1])

datas_iniciais = pd.Timestamp("2020-01-01")
datas_finais = pd.Timestamp("2024-12-31")

dados["data da compra"] = pd.to_datetime(
    np.random.randint(datas_iniciais.timestamp(), datas_finais.timestamp(), num_linhas), unit="s"
)


#TABELAS
#Tabelas de receita
receita_estados=dados.groupby('local da compra')[['price']].sum()
receita_estados=dados.drop_duplicates(subset='local da compra')[['local da compra','Latitude','Longitude']].merge(receita_estados,left_on='local da compra',right_index=True).sort_values('price',ascending=False)

receita_mensal=dados.set_index('data da compra').groupby(pd.Grouper(freq='M'))[['price']].sum().reset_index()
receita_mensal['Ano']=receita_mensal['data da compra'].dt.year
receita_mensal['Mes']=receita_mensal['data da compra'].dt.month_name()

receita_car= dados.groupby('car')[['price']].sum().sort_values('price',ascending=False)
#Tabelas de quantidade de vendas

#Tabelas marcas de carro
marcas_carro=pd.DataFrame(dados.groupby('model')['price'].agg(['sum','count']))

#graficos
fig_mapa_receita= px.scatter_geo(receita_estados,lat='Latitude',lon='Longitude',
  scope='usa',size='price',template='seaborn',hover_name='local da compra',
  hover_data={'Latitude':False,'Longitude':False},
  title='Receita por Estado')

fig_receita_mensal=px.line(receita_mensal,x='Mes',y='price',markers=True,
                           range_y=(0, receita_mensal.max()),
                           color='Ano',line_dash='Ano',
                           title='Receita mensal')
fig_receita_mensal.update_layout(yaxis_title='Receita')                           

fig_receita_estado=px.bar(receita_estados.head(),
                          x='local da compra',y='price',
                          text_auto=True,title='Top estados (receita)')
fig_receita_mensal.update_layout(yaxis_title='Receita') 

fig_receita_carros=px.bar(receita_car,text_auto=True,
                          title='Receita por marca de carro')
fig_receita_mensal.update_layout(yaxis_title='Receita') 

# visualização streamlit

aba1,aba2,aba3=st.tabs(['Receita','Quantidade de vendas','marcas de carro'])

with aba1:
    coluna1, coluna2 = st.columns(2)
    with coluna1:
        st.metric('Receita', formata_numero(dados['price'].sum()))
        st.plotly_chart(fig_mapa_receita,use_container_width=True)
        st.plotly_chart(fig_receita_estado,use_container_width=True)
    with coluna2:
        st.metric('Quantidade de vendas', formata_numero(dados.shape[0]))
        st.plotly_chart(fig_receita_mensal,use_container_width=True)
        st.plotly_chart(fig_receita_carros,use_container_width=True)

with aba2:
    coluna1, coluna2 = st.columns(2)
    
    with coluna1:
        st.metric('Quantidade de vendas por estado', formata_numero(dados.shape[0]))

        estados_selecionados = st.multiselect(
            'Selecione os estados para visualizar a quantidade de vendas',
            options=dados['local da compra'].unique(),
            default=dados['local da compra'].unique()[:5] 
        )
        
        vendas_estados = dados[dados['local da compra'].isin(estados_selecionados)]
        vendas_estados = vendas_estados.groupby('local da compra')['price'].count().reset_index().sort_values('price', ascending=False)
        
        fig_vendas_estados = px.bar(
            vendas_estados,
            x='local da compra', y='price',
            text_auto=True, title='Quantidade de Vendas por Estado',
            labels={'price': 'Quantidade de Vendas', 'local da compra': 'Estado'}
        )
        fig_vendas_estados.update_layout(
            xaxis_title='Estado',
            yaxis_title='Quantidade de Vendas'
        )
        st.plotly_chart(fig_vendas_estados, use_container_width=True)
    
    with coluna2:
        st.metric('Quantidade de vendas por marca de carro', formata_numero(dados.shape[0]))
        
        marcas_selecionadas = st.multiselect(
            'Selecione as marcas de carro para visualizar a quantidade de vendas',
            options=dados['model'].unique(),
            default=dados['model'].unique()[:5] 
        )
        

        vendas_marcas_carro = dados[dados['model'].isin(marcas_selecionadas)]
        vendas_marcas_carro = vendas_marcas_carro.groupby('model')['price'].count().reset_index().sort_values('price', ascending=False)
        
        fig_vendas_marcas_carro = px.bar(
            vendas_marcas_carro,
            x='model', y='price',
            text_auto=True, title='Quantidade de Vendas por Marca de Carro',
            labels={'price': 'Quantidade de Vendas', 'model': 'Marca de Carro'}
        )
        fig_vendas_marcas_carro.update_layout(
            xaxis_title='Marca de Carro',
            yaxis_title='Quantidade de Vendas'
        )
        st.plotly_chart(fig_vendas_marcas_carro, use_container_width=True)
        
with aba3:
    qtd_marcas_carro = st.number_input('Quantidade de marcas de carro', 2, 10, 5)
    coluna1, coluna2 = st.columns(2)
    with coluna1:
        st.metric('Receita', formata_numero(dados['price'].sum()))
        fig_receita_marcas_carro = px.bar(
            marcas_carro[['sum']].sort_values('sum', ascending=False).head(qtd_marcas_carro),
            x='sum', y=marcas_carro[['sum']].sort_values('sum', ascending=False).head(qtd_marcas_carro).index,
            text_auto=True, title=f'Top {qtd_marcas_carro} marcas de carro (receita)'
        )
        fig_receita_marcas_carro.update_layout(
            xaxis_title='Receita (R$)',  
            yaxis_title='Marca de Carro'  
        )
        st.plotly_chart(fig_receita_marcas_carro, use_container_width=True)
    with coluna2:
        st.metric('Quantidade de vendas', formata_numero(dados.shape[0]))
        fig_vendas_marcas_carro = px.bar(
            marcas_carro[['count']].sort_values('count', ascending=False).head(qtd_marcas_carro),
            x='count', y=marcas_carro[['count']].sort_values('count', ascending=False).head(qtd_marcas_carro).index,
            text_auto=True, title=f'Top {qtd_marcas_carro} marcas de carro (quantidade de vendas)'
        )
        fig_vendas_marcas_carro.update_layout(
            xaxis_title='Quantidade de Vendas',  
            yaxis_title='Marca de Carro' 
        )
        st.plotly_chart(fig_vendas_marcas_carro, use_container_width=True)

st.write(dados)