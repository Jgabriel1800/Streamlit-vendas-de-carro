import streamlit as st
import requests 
import pandas as pd
import plotly.express as px

st.title('DASHBOARD DE VENDAS :car:')

arquivo_csv='car_ad.csv'


dados = pd.read_csv(arquivo_csv, encoding="latin1")  



