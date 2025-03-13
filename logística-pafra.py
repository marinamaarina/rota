import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
from geopy.distance import geodesic

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

# Definir pontos de **estoque**
pontos_estoque = {
    "Santa Mônica (Estoque)": (-18.9395, -48.2820),
    "Rua Professor Maria Castilho, 295": (-18.9110, -48.2765),  # Coordenada ajustada
    "Rua Rio Grande do Sul, 1963, Marta Helena": (-18.9245, -48.3060)  # Coordenada ajustada
}

# Título
st.title('📦 Gestão de Logística - Uberlândia')

st.write("""  
🚚 **Análise de Estoque e Entrega em Uberlândia**  
🔍 Escolha uma zona para ver os bairros, as principais vias de entrega e otimize sua logística.
""")

# **Campo de seleção de zona**
zona_selecionada = st.selectbox('🎯 Selecione a Zona:', df['Zona'].unique())

# **Campo de seleção de raio**
raio = st.slider('🔘 Defina o raio de entrega (em km):', min_value=1, max_value=50, value=10)

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

# Marcar pontos de estoque corretamente
for nome, coord in pontos_estoque.items():
    distancia = geodesic(coord, coordenadas_zona).km
    if distancia <= raio:
        folium.Marker(
            location=coord,
            popup=f"{nome} - Distância: {distancia:.2f} km",
            tooltip=f"{nome} - {distancia:.2f} km",
            icon=folium.Icon(color="green", icon="cloud")
        ).add_to(mapa)

        # Traçar linha entre o ponto de estoque e a zona selecionada
        folium.PolyLine(
            locations=[coord, coordenadas_zona],
            color="blue",
            weight=2.5,
            opacity=1
        ).add_to(mapa)

        # Calcular e exibir o tempo estimado de entrega
        velocidade_media = 40  # km/h
        tempo_estimado = distancia / velocidade_media
        st.write(f"⏳ Tempo estimado de entrega de {nome} para a zona: {tempo_estimado:.2f} horas")

# Exibir o mapa interativo
folium_static(mapa)


