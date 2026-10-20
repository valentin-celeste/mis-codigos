import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import os

st.set_page_config(
    page_title="Dashboard Exploratorio - RedConecta Telecom",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 1. Carga de datos (usando freq="D" para evitar errores de versión en Pandas)
@st.cache_data
def cargar_datos():
    file_path = "dataset_set_D_telecomunicaciones.xlsx"
    if os.path.exists(file_path):
        df = pd.read_excel(file_path)
    else:
        np.random.seed(42)
        n = 500
        df = pd.DataFrame({
            "fecha": pd.date_range(start="2026-01-01", periods=n, freq="D"),
            "region": np.random.choice(["Norte", "Centro", "Sur", "Metropolitana"], n),
            "tipo_servicio": np.random.choice(["Móvil", "Internet Hogar", "Corporativo"], n),
            "trafico_gb": np.round(np.random.gamma(5, 20, n), 2),
            "incidencias": np.random.poisson(3, n),
            "tickets_soporte": np.random.poisson(5, n),
            "tiempo_resolucion_min": np.round(np.random.exponential(45, n) + 15, 1),
            "latencia_ms": np.round(np.random.normal(35, 12, n), 1),
            "clientes_afectados": np.random.negative_binomial(2, 0.05, n)
        })
        df["cumple_sla"] = (df["latencia_ms"] < 50) & (df["tiempo_resolucion_min"] < 60)
        df["cumple_sla_str"] = df["cumple_sla"].map({True: "Cumple SLA", False: "Fuera de SLA"})
    return df

df = cargar_datos()

# Encabezado
st.title("📡 RedConecta Telecom S.A. — Dashboard Operacional")
st.markdown("Análisis exploratorio de latencia, tickets de soporte y cumplimiento de SLA por región y servicio.")

# Sidebar - Filtros
st.sidebar.header("Filtros de Exploración")
regiones_sel = st.sidebar.multiselect("Seleccionar Región:", df["region"].unique(), default=df["region"].unique())
servicios_sel = st.sidebar.multiselect("Seleccionar Tipo de Servicio:", df["tipo_servicio"].unique(), default=df["tipo_servicio"].unique())

df_filtered = df[(df["region"].isin(regiones_sel)) & (df["tipo_servicio"].isin(servicios_sel))]

# Métricas Principales (KPIs)
col1, col2, col3, col4 = st.columns(4)
col1.metric("Incidencias Totales", f"{df_filtered['incidencias'].sum():,}")
col2.metric("Tickets de Soporte", f"{df_filtered['tickets_soporte'].sum():,}")
col3.metric("Latencia Promedio", f"{df_filtered['latencia_ms'].mean():.1f} ms")
pct_sla = (df_filtered["cumple_sla_str"] == "Cumple SLA").mean() * 100
col4.metric("% Cumplimiento SLA", f"{pct_sla:.1f}%")

st.divider()

# Gráficos
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("⏱️ Tiempos de Resolución por Región")
    fig_res = px.box(
        df_filtered, 
        x="region", 
        y="tiempo_resolucion_min", 
        color="tipo_servicio",
        title="Distribución de Tiempos de Resolución (minutos)"
    )
    st.plotly_chart(fig_res, use_container_width=True)

with col_right:
    st.subheader("⚡ Latencia vs Clientes Afectados")
    fig_lat = px.scatter(
        df_filtered, 
        x="latencia_ms", 
        y="clientes_afectados", 
        color="cumple_sla_str",
        hover_data=["region", "tipo_servicio"],
        color_discrete_map={"Cumple SLA": "#2ecc71", "Fuera de SLA": "#e74c3c"},
        title="Impacto Técnico en Experiencia del Cliente"
    )
    st.plotly_chart(fig_lat, use_container_width=True)

# Sección de Salidas para Áreas
st.divider()
st.subheader("📂 Generación de Data Marts por Área")

c1, c2 = st.columns(2)
with c1:
    st.markdown("**Área de Soporte Técnico**")
    cols_soporte = ["fecha", "region", "tipo_servicio", "incidencias", "tickets_soporte", "tiempo_resolucion_min"]
    st.dataframe(df_filtered[cols_soporte].head(5), use_container_width=True)
    csv_soporte = df_filtered[cols_soporte].to_csv(index=False).encode('utf-8')
    st.download_button("Descargar Reporte Soporte Técnico (CSV)", csv_soporte, "reporte_soporte_tecnico.csv", "text/csv")

with c2:
    st.markdown("**Área de Experiencia de Clientes (CX)**")
    cols_cx = ["fecha", "tipo_servicio", "clientes_afectados", "latencia_ms", "cumple_sla_str"]
    st.dataframe(df_filtered[cols_cx].head(5), use_container_width=True)
    csv_cx = df_filtered[cols_cx].to_csv(index=False).encode('utf-8')
    st.download_button("Descargar Reporte CX (CSV)", csv_cx, "reporte_experiencia_cliente.csv", "text/csv")