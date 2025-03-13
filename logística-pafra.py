import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static

# Dados das zonas, bairros e principais vias
data = {
    'Zona': ['Zona Central', 'Zona Norte', 'Zona Sul', 'Zona Leste', 'Zona Oeste', 'Zona Periférica'],
    'Bairros': [
        ['Centro', 'Brasil', 'Morada da Colina', 'Fundinho', 'Lídice', 'Osvaldo Resende', 'Segismundo Pereira'],
        ['Tibery', 'Jardim Canadá', 'Santa Rosa', 'Jardim Ipanema', 'São Jorge', 'Industrial'],
        ['Santa Mônica', 'Jardim Patrícia', 'Parque do Sabiá', 'Alvorada', 'Universitário', 'Marta Helena'],
        ['Chácaras Tubalina', 'Martins', 'São Sebastião', 'Chácara do Sol', 'Rosalvo', 'Luizote de Freitas'],
        ['Jardim Europa', 'Jardim Brasília', 'Novo Mundo', 'Jardim das Palmeiras', 'Leste Industrial'],
        ['Cidade Jardim', 'São Vicente', 'Luizote de Freitas', 'Dom Almir', 'Jardim Sorrilândia', 'Boa Vista']
    ],
    'Principais Vias': [
        ['Av. João Naves', 'Av. Rondon Pacheco', 'Rua Getúlio Vargas'],
        ['Av. João Naves', 'Av. Três Moinhos', 'Rua da Balsa'],
        ['Av. João Naves', 'Av. Jundiaí', 'Av. Rio Branco'],
        ['Av. Getúlio Vargas', 'Av. Ester Furquim', 'Av. Cesário Alvim'],
        ['Av. Cesário Alvim', 'Av. Paulo Gracindo', 'Av. JK'],
        ['Av. Luizote', 'Av. Mário Palmério', 'Av. Anselmo Alves']
    ]
}

df = pd.DataFrame(data)

# PONTOS DE ESTOQUE
pontos_estoque = {
    "📍 Santa Mônica (Estoque)": (-18.9395, -48.2820),
    "📍 Madalena (Estoque)": (-18.9100, -48.3000)
}

# --- LAYOUT ---
st.set_page_config(page_title="Logística Uberlândia", layout="wide")

# TÍTULO COM COR FORTE
st.markdown("<h1 style='text-align: center; color: #D72638;'>📦 Gestão de Logística</h1>", unsafe_allow_html=True)
st.markdown("<hr style='border:2px solid #D72638'>", unsafe_allow_html=True)

# --- SELEÇÃO DE ZONA ---
zona_selecionada = st.selectbox('🔍 Escolha uma Zona:', df['Zona'])

# --- EXIBIÇÃO DE DADOS ---
if zona_selecionada:
    zona_info = df[df['Zona'] == zona_selecionada].iloc[0]
    
    st.subheader(f"📌 Bairros na {zona_selecionada}")
    st.write(" | ".join(zona_info['Bairros']))  

    st.subheader("🚦 Principais Vias")
    st.write(" | ".join(zona_info['Principais Vias']))  

# --- MAPA ---
st.subheader("🗺️ Estoques e Zonas no Mapa")

mapa = folium.Map(location=[-18.9186, -48.2769], zoom_start=12)

# Marcar zonas
for _, row in df.iterrows():
    folium.Marker(
        location=[-18.9186, -48.2769],  # Posição centralizada
        popup=row['Zona'],
        tooltip=row['Zona'],
        icon=folium.Icon(color="blue")
    ).add_to(mapa)

# Marcar pontos de estoque
for nome, coord in pontos_estoque.items():
    folium.Marker(
        location=coord,
        popup=nome,
        tooltip=nome,
        icon=folium.Icon(color="green")
    ).add_to(mapa)

folium_static(mapa)

