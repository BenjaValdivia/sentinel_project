import streamlit as st
import pandas as pd
import plotly.express as px
from model_logic import process_fraud_detection # Importamos el cerebro

st.set_page_config(page_title="Sentinel AI", layout="wide")

st.title("Sentinel: Detección de Fraude Local")
st.markdown("""
Esta herramienta analiza transacciones financieras en tiempo real buscando patrones anómalos 
**sin enviar datos a la nube**, garantizando privacidad bancaria total.
""")

# Barra lateral para subir archivos
st.sidebar.header("Configuración")
uploaded_file = st.sidebar.file_uploader("Cargar CSV de transacciones", type="csv")

if uploaded_file:
    # Leer datos
    df_raw = pd.read_csv(uploaded_file)
    
    with st.spinner('Analizando patrones de riesgo localmente...'):
        # Llamar a la lógica del Socio A
        df_processed = process_fraud_detection(df_raw)
    
    # --- DASHBOARD ---
    col1, col2 = st.columns(2)
    
    with col1:
        total_anomalies = df_processed['is_fraud'].sum()
        st.metric("Transacciones Sospechosas", total_anomalies, delta_color="inverse")
        
    with col2:
        total_amount = df_processed[df_processed['is_fraud'] == 1]['Amount'].sum()
        st.metric("Capital en Riesgo", f"${total_amount:,.2f}")

    # Gráfico de Dispersión
    st.subheader("Mapa de Riesgo de Transacciones")
    fig = px.scatter(df_processed, 
                     x="Amount", 
                     y="V1", # V1 es una variable anonimizada del dataset
                     color="is_fraud",
                     color_discrete_map={0: "#00CC96", 1: "#EF553B"},
                     hover_data=['Amount'],
                     title="Distribución de Anomalías Detectadas")
    st.plotly_chart(fig, use_container_width=True)

    # Mostrar tabla de sospechosos
    st.subheader("Detalle de registros de alto riesgo")
    st.dataframe(df_processed[df_processed['is_fraud'] == 1].head(10))

else:
    st.info("Por favor, sube el archivo 'creditcard.csv' para comenzar el análisis.")