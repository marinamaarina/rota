import streamlit as st
import pandas as pd
import numpy as np
import folium
from folium.plugins import MarkerCluster
import matplotlib.pyplot as plt
import seaborn as sns
from geopy.distance import geodesic

# Função para calcular distância entre duas coordenadas geográficas
def calcular_distancia(lat1, lon1, lat2, lon2):
    return geodesic((lat1, lon1), (lat2, lon2)).km

# Título do aplicativo
st.title('Análise Logística de Entregas - Melhorado')

# Descrição
st.markdown("""
Este projeto tem como objetivo analisar e otimizar a logística de entrega dos sacos de lixo em Uberlândia.
Com base nas zonas de entrega, podemos analisar o tempo de entrega, calcular as rotas otimizadas, e estimar custos logísticos.
""")

# Dados Exemplo: Pode ser substituído por dados reais ou API
dados = {
    'Zona': ['Centro', 'Santa Mônica', 'Tibery', 'Planalto', 'Osvaldo Rezende'],
    'Tempo de Entrega (min)': [30, 40, 50, 45, 35],
    'Distância (km)': [5, 7, 10, 8, 6],
    'Eficiência da Rota': [80, 75, 70, 80, 85],
    'Latitude': [-18.9181, -18.9200, -18.9000, -18.9300, -18.9100],
    'Longitude': [-48.2750, -48.2800, -48.2900, -48.2850, -48.2700]
}

# Criação do DataFrame
df = pd.DataFrame(dados)

# Exibição da tabela de dados
st.subheader('Tabela de Dados de Logística')
st.dataframe(df)

# Filtro interativo para selecionar zonas
zonas_selecionadas = st.multiselect('Selecione as Zonas para Análise:', df['Zona'])

if zonas_selecionadas:
    df_filtrado = df[df['Zona'].isin(zonas_selecionadas)]
    st.dataframe(df_filtrado)

# Análise Gráfica de Tempo de Entrega por Zona
st.subheader('Tempo de Entrega por Zona')
plt.figure(figsize=(10, 6))
sns.barplot(x='Zona', y='Tempo de Entrega (min)', data=df_filtrado)
plt.title('Tempo de Entrega por Zona')
plt.xlabel('Zona')
plt.ylabel('Tempo de Entrega (min)')
st.pyplot()

# Mapa interativo das Zonas de Entrega com Folium
st.subheader('Mapa Interativo das Zonas de Entrega')

# Definir o mapa centrado em Uberlândia
mapa = folium.Map(location=[-18.9181, -48.2750], zoom_start=12)

# Adicionar marcadores para cada zona
marker_cluster = MarkerCluster().add_to(mapa)

for _, row in df_filtrado.iterrows():
    folium.Marker(
        location=[row['Latitude'], row['Longitude']],
        popup=f"Zona: {row['Zona']}<br>Tempo de Entrega: {row['Tempo de Entrega (min)']} min<br>Distância: {row['Distância (km)']} km"
    ).add_to(marker_cluster)

# Exibir o mapa
st.map(mapa)

# Análise de Eficiência da Rota
st.subheader('Eficiência das Rotas')
plt.figure(figsize=(10, 6))
sns.barplot(x='Zona', y='Eficiência da Rota', data=df_filtrado, palette="Blues_d")
plt.title('Eficiência das Rotas por Zona')
plt.xlabel('Zona')
plt.ylabel('Eficiência (%)')
st.pyplot()

# Cálculo de Custo de Transporte
st.subheader('Cálculo de Custo de Transporte')

# Parâmetros para o cálculo
custo_por_km = st.number_input('Custo por km (em R$):', min_value=0.0, value=3.0, step=0.1)
consumo_combustivel = st.number_input('Consumo do veículo (km/L):', min_value=0.0, value=8.0, step=0.1)
preco_combustivel = st.number_input('Preço do combustível (R$/L):', min_value=0.0, value=5.0, step=0.1)

# Calcular custo de transporte por zona
df_filtrado['Custo de Transporte (R$)'] = (df_filtrado['Distância (km)'] / consumo_combustivel) * preco_combustivel * custo_por_km

# Exibir custos de transporte
st.write("Custo de transporte por zona (R$):")
st.dataframe(df_filtrado[['Zona', 'Custo de Transporte (R$)']])

# Caixa de Texto para Análise de Dados
st.subheader('Análise de Dados')
zona = st.selectbox('Selecione a Zona para Análise Detalhada:', df_filtrado['Zona'])

if zona:
    zona_data = df_filtrado[df_filtrado['Zona'] == zona].iloc[0]
    st.write(f"**Zona Selecionada:** {zona}")
    st.write(f"**Tempo de Entrega:** {zona_data['Tempo de Entrega (min)']} minutos")
    st.write(f"**Distância:** {zona_data['Distância (km)']} km")
    st.write(f"**Eficiência da Rota:** {zona_data['Eficiência da Rota']}%")
    st.write(f"**Custo de Transporte:** R${zona_data['Custo de Transporte (R$)']:.2f}")

