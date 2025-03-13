import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
from geopy.distance import geodesic
from folium import PolyLine
import requests
import json

# Dados das zonas, bairros e coordenadas
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
    'Principais Vias': [
        'Avenida João Naves de Ávila, Avenida Rondon Pacheco, Rua Getúlio Vargas',
        'Avenida João Naves de Ávila, Avenida dos Três Moinhos, Rua da Balsa',
        'Avenida João Naves de Ávila, Avenida Jundiaí, Avenida Rio Branco',
        'Avenida Getúlio Vargas, Avenida Ester Furquim, Avenida Cesário Alvim',
        'Avenida Cesário Alvim, Avenida Paulo Gracindo, Avenida JK',
        'Avenida Luizote de Freitas, Avenida Mário Palmério, Avenida Anselmo Alves dos Santos'
    ],
    'Latitude': [-18.9186, -18.8762, -18.9395, -18.9183, -18.9375, -18.9450],
    'Longitude': [-48.2769, -48.2792, -48.2820, -48.2551, -48.3210, -48.2307]
}

df = pd.DataFrame(data)

# Definir pontos de estoque com as novas coordenadas
pontos_estoque = {
    "Santa Mônica (Estoque)": (-18.9395, -48.2820),
    "Rua Professor Maria Castilho, 295": (-18.9234969, -48.2331072),
    "Rua Rio Grande do Sul, 1963, Marta Helena": (-18.8932489, -48.2712858)
}

# Chave da API OpenRouteService
API_KEY = "5b3ce3597851110001cf62481273387ba4aa44c5a315412263494881"

# Função para calcular a rota usando a API OpenRouteService
def calcular_rota(origem, destino):
    url = "https://api.openrouteservice.org/v2/directions/driving-car"
    headers = {
        "Authorization": API_KEY,
        "Content-Type": "application/json"
    }
    body = {
        "coordinates": [origem, destino],
        "instructions": "false"
    }
    response = requests.post(url, headers=headers, json=body)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Erro ao calcular a rota: {response.status_code}")
        return None

# Título
st.title('📦 Gestão de Logística - Uberlândia')

st.write("""  
🚚 **Análise de Estoque e Entrega em Uberlândia**  
🔍 Escolha uma zona para ver os bairros, as principais vias de entrega e otimize sua logística.
""")

# **Campo de seleção de zona**
zona_selecionada = st.selectbox('🎯 Selecione a Zona:', df['Zona'].unique())

# **Exibir bairros e vias correspondentes**
if zona_selecionada:
    bairros = df[df['Zona'] == zona_selecionada]['Bairros'].values[0]
    vias = df[df['Zona'] == zona_selecionada]['Principais Vias'].values[0]
    
    st.write(f"📌 **Bairros da {zona_selecionada}:**")
    st.write(bairros)

    st.write(f"🚦 **Principais Vias da {zona_selecionada}:**")
    st.write(vias)

# **Mapa das Zonas e Estoques**
st.subheader('🗺️ Mapa de Uberlândia com Estoques e Rotas de Entrega')

# Selecionando coordenadas da zona escolhida
coordenadas_zona = df[df['Zona'] == zona_selecionada][['Latitude', 'Longitude']].values[0]

# Criar o mapa
mapa = folium.Map(location=[-18.9186, -48.2769], zoom_start=12)

# Marcar zonas
for _, row in df.iterrows():
    folium.Marker(
        location=[row['Latitude'], row['Longitude']],
        popup=f"{row['Zona']}",
        tooltip=row['Zona'],
        icon=folium.Icon(color="blue", icon="info-sign")
    ).add_to(mapa)

# Marcar pontos de estoque e calcular rotas
distancias = []
for nome, coord in pontos_estoque.items():
    distancia = geodesic(coord, coordenadas_zona).km
    distancias.append({"Ponto de Estoque": nome, "Distância (km)": f"{distancia:.2f}"})
    
    folium.Marker(
        location=coord,
        popup=f"{nome} - Distância até a Zona: {distancia:.2f} km",
        tooltip=f"{nome} - {distancia:.2f} km",
        icon=folium.Icon(color="green", icon="cloud")
    ).add_to(mapa)
    
    # Calcular rota usando OpenRouteService
    origem = [coord[1], coord[0]]  # OpenRouteService espera [longitude, latitude]
    destino = [coordenadas_zona[1], coordenadas_zona[0]]
    rota_data = calcular_rota(origem, destino)
    
    if rota_data:
        # Extrair coordenadas da rota
        coordenadas_rota = rota_data['routes'][0]['geometry']['coordinates']
        coordenadas_rota = [[lat, lon] for lon, lat in coordenadas_rota]  # Converter para [latitude, longitude]
        
        # Desenhar a rota no mapa
        PolyLine(coordenadas_rota, color="red", weight=2.5, opacity=1).add_to(mapa)

# Exibir o mapa interativo
folium_static(mapa)

# Exibir distâncias em uma tabela
st.subheader("📊 Distâncias entre Pontos de Estoque e a Zona Selecionada")
st.table(pd.DataFrame(distancias))
