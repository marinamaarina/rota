import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static

# Dados das zonas, bairros e principais vias
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
        'Av. João Naves de Ávila, Av. Rondon Pacheco, Rua Getúlio Vargas',
        'Av. João Naves de Ávila, Av. Três Moinhos, Rua da Balsa',
        'Av. João Naves de Ávila, Av. Jundiaí, Av. Rio Branco',
        'Av. Getúlio Vargas, Av. Ester Furquim, Av. Cesário Alvim',
        'Av. Cesário Alvim, Av. Paulo Gracindo, Av. JK',
        'Av. Luizote de Freitas, Av. Mário Palmério, Av. Anselmo Alves dos Santos'
    ],
    'Latitude': [-18.9186, -18.8762, -18.9395, -18.9183, -18.9375, -18.9450],
    'Longitude': [-48.2769, -48.2792, -48.2820, -48.2551, -48.3210, -48.2307]
}

df = pd.DataFrame(data)

# PONTOS DE ESTOQUE
pontos_estoque = {
    "📍 Santa Mônica (Estoque)": (-18.9395, -48.2820),
    "📍 Madalena (Estoque)": (-18.9100, -48.3000)
}

# --- LAYOUT DO STREAMLIT ---
st.set_page_config(page_title="Logística Uberlândia", layout="wide")

st.markdown("""
<style>
    .title { font-size: 36px; font-weight: bold; text-align: center; color: #333333; }
    .subtitle { font-size: 24px; font-weight: bold; color: #444444; margin-top: 20px; }
    .info { font-size: 18px; color: #555555; }
    .table { font-size: 16px; text-align: center; }
</style>
""", unsafe_allow_html=True)

# --- TÍTULO ---
st.markdown('<p class="title">📦 Gestão de Logística - Uberlândia</p>', unsafe_allow_html=True)

st.markdown('<p class="info">🚚 Selecione uma zona para visualizar bairros, vias principais e pontos de estoque.</p>', unsafe_allow_html=True)

# --- SELEÇÃO DE ZONA ---
zona_selecionada = st.selectbox('🔍 Escolha uma Zona:', df['Zona'].unique())

# --- EXIBIÇÃO DE DADOS ---
if zona_selecionada:
    bairros = df[df['Zona'] == zona_selecionada]['Bairros'].values[0]
    vias = df[df['Zona'] == zona_selecionada]['Principais Vias'].values[0]

    st.markdown(f'<p class="subtitle">📌 Bairros da {zona_selecionada}</p>', unsafe_allow_html=True)
    st.write(f"✅ {bairros.replace(', ', '\n✅ ')}")  # Exibe cada bairro como um item de lista

    st.markdown(f'<p class="subtitle">🚦 Principais Vias</p>', unsafe_allow_html=True)
    st.write(f"🛣 {vias.replace(', ', '\n🛣 ')}")  # Exibe cada via como um item de lista

# --- MAPA INTERATIVO ---
st.markdown('<p class="subtitle">🗺️ Mapa de Estoques e Zonas</p>', unsafe_allow_html=True)

mapa = folium.Map(location=[-18.9186, -48.2769], zoom_start=12)

# Marcar zonas
for _, row in df.iterrows():
    folium.Marker(
        location=[row['Latitude'], row['Longitude']],
        popup=f"{row['Zona']}",
        tooltip=row['Zona'],
        icon=folium.Icon(color="blue", icon="info-sign")
    ).add_to(mapa)

# Marcar pontos de estoque
for nome, coord in pontos_estoque.items():
    folium.Marker(
        location=coord,
        popup=nome,
        tooltip=nome,
        icon=folium.Icon(color="green", icon="cloud")  # Estoque agora verde
    ).add_to(mapa)

folium_static(mapa)
