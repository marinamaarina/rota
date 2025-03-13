import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
from geopy.distance import geodesic
from folium import PolyLine, GeoJson
import json

# Carregar dados das zonas e bairros
data = {
    'Zona': ['Zona Central', 'Zona Norte', 'Zona Sul', 'Zona Leste', 'Zona Oeste', 'Zona Periférica'],
    'Bairros': [
        'Centro, Brasil, Morada da Colina, Fundinho, Lídice, Osvaldo Resende, Segismundo Pereira',
        'Tibery, Jardim Canadá, Bairro Santa Rosa, Jardim Ipanema, São Jorge, Industrial',
        'Santa Mônica, Jardim Patrícia, Parque do Sabiá, Alvorada, Universitário, Marta Helena',
        'Chácaras Tubalina, Martins, São Sebastião, Chácara do Sol, Rosalvo, Luizote de Freitas',
        'Jardim Europa, Jardim Brasília, Jardim Novo Mundo, Jardim das Palmeiras, Leste Industrial',
        'Cidade Jardim, São Vicente, Luizote de Freitas, Dom Almir, Jardim Sorrilândia, Boa Vista'
    ],
    'Latitude': [-18.9186, -18.8762, -18.9395, -18.9183, -18.9375, -18.9450],
    'Longitude': [-48.2769, -48.2792, -48.2820, -48.2551, -48.3210, -48.2307]
}

df = pd.DataFrame(data)

# Definir pontos de estoque
pontos_estoque = {
    "Rua Professor Maria Castilho, 295": (-18.9234969, -48.2331072),
    "Rua Rio Grande do Sul, 1963, Marta Helena": (-18.8932489, -48.2712858)
}

# Carregar o arquivo GeoJSON com os bairros
def carregar_geojson():
    try:
        with open('bairros_uberlandia.geojson', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        st.error("Arquivo 'bairros_uberlandia.geojson' não encontrado. Certifique-se de que ele está no mesmo diretório do script.")
        return None

bairros_geojson = carregar_geojson()

# Título
title = '📦 Gestão de Logística - Uberlândia'
st.title(title)

st.write("""
🚚 **Análise de Estoque e Entrega em Uberlândia**  
🔍 Escolha uma zona para ver os bairros, as principais vias de entrega e otimize sua logística.
""")

# Campo de seleção de zona
zona_selecionada = st.selectbox('🎯 Selecione a Zona:', df['Zona'].unique())

# Exibir bairros correspondentes
if zona_selecionada:
    bairros = df[df['Zona'] == zona_selecionada]['Bairros'].values[0]
    st.write(f"📌 **Bairros da {zona_selecionada}:**")
    st.write(bairros)

# Criar o mapa
st.subheader('🗺️ Mapa de Uberlândia com Estoques e Rotas de Entrega')
mapa = folium.Map(location=[-18.9186, -48.2769], zoom_start=12)

# Marcar zonas
for _, row in df.iterrows():
    folium.Marker(
        location=[row['Latitude'], row['Longitude']],
        popup=row['Zona'],
        tooltip=row['Zona'],
        icon=folium.Icon(color="blue", icon="info-sign")
    ).add_to(mapa)

# Marcar pontos de estoque e desenhar rotas até a zona selecionada
coordenadas_zona = df[df['Zona'] == zona_selecionada][['Latitude', 'Longitude']].values[0]
for nome, coord in pontos_estoque.items():
    distancia = geodesic(coord, coordenadas_zona).km
    folium.Marker(
        location=coord,
        popup=f"{nome} - Distância: {distancia:.2f} km",
        tooltip=f"{nome} - {distancia:.2f} km",
        icon=folium.Icon(color="green", icon="cloud")
    ).add_to(mapa)
    PolyLine([coord, coordenadas_zona], color="blue", weight=2.5, opacity=1).add_to(mapa)

# Destacar a zona selecionada no mapa
if bairros_geojson:
    def estilo_bairro(feature):
        if feature['properties'].get('Zona') == zona_selecionada:
            return {'fillColor': 'blue', 'color': 'black', 'weight': 1, 'fillOpacity': 0.3}
        return {'fillColor': 'gray', 'color': 'black', 'weight': 1, 'fillOpacity': 0.1}
    
    GeoJson(bairros_geojson, style_function=estilo_bairro).add_to(mapa)

# Exibir o mapa
folium_static(mapa)


