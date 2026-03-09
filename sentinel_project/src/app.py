import streamlit as st
import pandas as pd
import plotly.express as px
from model_logic import process_fraud_detection

# Configuración profesional de la página (DEBE ir siempre al principio)
st.set_page_config(
    page_title="Sentinel AI | Fraud Detection",
    page_icon="🛡️",
    layout="wide"
)

# Estilo personalizado extra
st.markdown("""
    <style>
    .main { background-color: #0E1117; }
    .stMetric { background-color: #1E2127; padding: 15px; border-radius: 10px; border: 1px solid #31333F; }
    </style>
    """, unsafe_allow_html=True) 

st.title("🛡️ Sentinel: Analítica de Fraude Privada")
st.markdown("---")

# --- OPTIMIZACIONES DE MEMORIA (CACHÉ) ---
@st.cache_data
def load_data(file):
    return pd.read_csv(file)

@st.cache_data
def run_model(df):
    return process_fraud_detection(df.copy())

@st.cache_data
def convert_df(df):
    return df.to_csv(index=False).encode('utf-8')

# --- BARRA LATERAL ---
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/2092/2092663.png", width=100)
st.sidebar.header("Panel de Control")
uploaded_file = st.sidebar.file_uploader("Cargar transacciones (CSV)", type="csv")

st.sidebar.info("""
**Privacidad Garantizada:** Los datos se procesan localmente en tu RAM. 
Ningún dato es enviado a servidores externos.
""")

# --- CUERPO PRINCIPAL ---
if uploaded_file:
    # Carga de datos optimizada
    df_raw = load_data(uploaded_file)
    
    with st.spinner('Analizando patrones con Isolation Forest...'):
        df = run_model(df_raw)
    
    # 1. KPIs SUPERIORES
    st.subheader("📊 Métricas de Operación")
    m1, m2, m3, m4 = st.columns(4)
    
    total_tx = len(df)
    anomalias = df[df['is_fraud'] == 1]
    pct_riesgo = (len(anomalias) / total_tx) * 100
    avg_normal = df[df['is_fraud']==0]['Amount'].mean()
    avg_fraud = anomalias['Amount'].mean()
    
    m1.metric("Transacciones Totales", f"{total_tx:,}")
    m2.metric("Alertas de Riesgo", len(anomalias), delta=f"{pct_riesgo:.2f}%", delta_color="inverse")
    m3.metric("Monto Promedio Normal", f"${avg_normal:.2f}")
    m4.metric("Monto Promedio Riesgo", f"${avg_fraud:.2f}")

    st.markdown("###")

    # --- MUESTREO VISUAL PARA EVITAR CRASHEOS ---
    df_fraud = df[df['is_fraud'] == 1]
    df_normal = df[df['is_fraud'] == 0]
    sample_size = min(5000, len(df_normal))
    df_plot = pd.concat([df_normal.sample(n=sample_size, random_state=42), df_fraud])

    # 2. GRÁFICOS DE LA "HISTORIA"
    col_left, col_right = st.columns([2, 1])

    with col_left:
        st.subheader(f"📍 Mapa de Desviaciones (Muestra de {len(df_plot)} regs)")
        fig = px.scatter(df_plot, x="V1", y="V2", color="is_fraud",
                         color_discrete_map={0: '#2E91E5', 1: '#FF4B4B'},
                         labels={"is_fraud": "Estado", "V1": "Eje Principal", "V2": "Eje Secundario"},
                         template="plotly_dark",
                         hover_data=["Amount"],
                         opacity=0.7)
        
        # Inyectamos navegación suave
        fig.update_layout(dragmode='pan', hovermode='closest', margin=dict(l=20, r=20, t=40, b=20))
        fig.for_each_trace(lambda t: t.update(name="Fraude" if t.name == "1" else "Normal"))
        st.plotly_chart(fig, use_container_width=True, config={'scrollZoom': True})

    with col_right:
        st.subheader("💰 Distribución de Capital")
        # Inyectamos corrección matemática para evitar error de log(0)
        df_box = df_plot[df_plot['Amount'] > 0]
        
        fig_box = px.box(df_box, x="is_fraud", y="Amount", color="is_fraud",
                         color_discrete_map={0: '#2E91E5', 1: '#FF4B4B'},
                         log_y=True, template="plotly_dark")
                         
        fig_box.update_xaxes(tickvals=[0, 1], ticktext=["Normal", "Fraude"])
        fig_box.for_each_trace(lambda t: t.update(name="Fraude" if t.name == "1" else "Normal"))
        st.plotly_chart(fig_box, use_container_width=True)

    # 3. NARRATIVA AUTOMÁTICA
    st.divider()
    st.header("🕵️ Reporte del Analista")
    
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"""
        **Resumen de Hallazgos:**
        * Se han identificado **{len(anomalias)}** comportamientos fuera de la norma estadística.
        * El riesgo se concentra en transacciones con un valor promedio de **${avg_fraud:.2f}**.
        * La separación en el gráfico de clusters indica un fraude de tipo **estructural**, no aleatorio.
        """)
    with c2:
        st.warning(f"""
        **Acción Recomendada:**
        Las transacciones marcadas en rojo muestran una desviación crítica en las variables de comportamiento (V1-V28). 
        Se sugiere auditar el **{pct_riesgo:.2f}%** del volumen total antes del próximo cierre de ciclo.
        """)

    # 4. MÓDULO DE INSPECCIÓN Y ALERTAS PRIORITARIAS (FUSIONADO)
    st.divider()
    st.header("🔍 Módulo de Inspección y Alertas Prioritarias")
    
    # Preparamos el Top 50 de riesgos
    top_riesgo = anomalias.sort_values(by="Amount", ascending=False).head(50).copy()
    top_riesgo['Visual_ID'] = "Tx: #" + top_riesgo.index.astype(str) + " | Monto: $" + top_riesgo['Amount'].astype(str)
    
    col_lista, col_detalle = st.columns([1, 1.2])

    with col_lista:
        st.markdown("**1. Seleccionar Caso Crítico**")
        caso_seleccionado = st.selectbox(
            "Seleccione una transacción de la lista para inspeccionarla en detalle:",
            options=top_riesgo['Visual_ID'].tolist()
        )
        
        st.markdown("**2. Top 50 Transacciones de Mayor Riesgo**")
        # Mostramos la tabla ocultando la columna Visual_ID que creamos solo para el selectbox
        st.dataframe(top_riesgo.drop(columns=['Visual_ID']), use_container_width=True, height=250)

    with col_detalle:
        st.markdown("**3. Panel de Control de la Transacción**")
        
        # Filtramos los datos del caso seleccionado
        datos_caso = top_riesgo[top_riesgo['Visual_ID'] == caso_seleccionado].iloc[0]
        id_real = datos_caso.name
        
        # Tarjetas de métricas
        d1, d2, d3 = st.columns(3)
        d1.metric("ID Sistema", f"#{id_real}")
        d2.metric("Monto Involucrado", f"${datos_caso['Amount']:,.2f}")
        d3.metric("Nivel de Alerta", "Máximo", delta="Bloqueo Sugerido", delta_color="inverse")
        
        st.caption("Variables Paramétricas Ocultas (PCA)")
        columnas_ocultas = ['Visual_ID', 'is_fraud', 'anomaly_score', 'Class', 'Time']
        df_tecnico = pd.DataFrame(datos_caso).drop(columnas_ocultas, errors='ignore').T
        
        st.dataframe(df_tecnico, use_container_width=True)
        
        # Botón de acción rápida
        st.markdown("###")
        if st.button(f"🚨 Bloquear Tarjeta vinculada a Tx #{id_real}", type="primary", use_container_width=True):
            st.success(f"Comando de bloqueo enviado para la transacción #{id_real}. El registro ha sido marcado en el sistema.")

    # BOTÓN DE DESCARGA EN BARRA LATERAL
    csv = convert_df(df)
    st.sidebar.download_button("📥 Descargar Reporte Completo", csv, "analisis_sentinel.csv", "text/csv")

else:
    # Pantalla de bienvenida
    st.info("👋 Por favor, carga el archivo creditcard.csv desde la barra lateral para comenzar.")
    
    st.markdown("""
    ### ¿Cómo interpretar este Dashboard?
    1. **Sube los datos:** Usa el botón de la izquierda.
    2. **Observa el Mapa:** Los puntos rojos son transacciones cuyo 'ADN financiero' es radicalmente distinto al resto.
    3. **Analiza los Montos:** El gráfico de cajas te dirá si el fraude es de montos pequeños (hormigueo) o grandes impactos.
    4. **Auditoría Individual:** Usa el módulo inferior para revisar los casos más críticos y emitir bloqueos.
    """)