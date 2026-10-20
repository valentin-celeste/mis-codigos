import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="RedConecta Telecom - Dashboard Operacional", layout="wide")

@st.cache_data
def load_data():
    return pd.read_excel('dataset_set_D_telecomunicaciones.xlsx')

df = load_data()

st.title("📡 RedConecta Telecom S.A. - Control Operacional y SLA")
st.markdown("---")

# Filtros laterales
st.sidebar.header("Filtros de Exploración")
region_filter = st.sidebar.multiselect("Seleccionar Región:", df['region'].unique(), default=df['region'].unique())
servicio_filter = st.sidebar.multiselect("Tipo de Servicio:", df['tipo_servicio'].unique(), default=df['tipo_servicio'].unique())

df_filtered = df[(df['region'].isin(region_filter)) & (df['tipo_servicio'].isin(servicio_filter))]

# KPIs principales
kpi1, kpi2, kpi3, kpi4 = st.columns(4)
kpi1.metric("Total Incidencias", int(df_filtered['incidencias_reportadas'].sum()))
kpi2.metric("Promedio Latencia (ms)", f"{df_filtered['latencia_ms'].mean():.1f} ms")
kpi3.metric("Tiempo Resol. Promedio", f"{df_filtered['tiempo_resolucion_hr'].mean():.1f} hrs")
sla_compliance_rate = (df_filtered['cumplimiento_sla'] == 'Cumple').mean() * 100
kpi4.metric("% Cumplimiento SLA", f"{sla_compliance_rate:.1f}%")

st.markdown("---")

# Visualizaciones
col1, col2 = st.columns(2)

with col1:
    st.subheader("Tiempo de Resolución vs. Tickets por Región")
    fig_bar = px.bar(
        df_filtered, x='region', y='tiempo_resolucion_hr', color='tipo_servicio',
        barmode='group', title="Tiempos de Resolución por Región y Servicio"
    )
    st.plotly_chart(fig_bar, use_container_width=True)

with col2:
    st.subheader("Relación Latencia vs. Clientes Afectados por SLA")
    fig_scatter = px.scatter(
        df_filtered, x='latencia_ms', y='clientes_afectados', color='cumplimiento_sla',
        size='tickets_soporte', hover_data=['region', 'tipo_servicio'],
        title="Impacto de Latencia y Afectación en Cumplimiento de SLA"
    )
    st.plotly_chart(fig_scatter, use_container_width=True)